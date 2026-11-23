"""CORE Bloque 28: medición REAL de latencia y tokens del flujo RAG.

Desde la raíz de ProyectoIA:
  python registro_rag.py
  python registro_rag.py --db vectorstore_ejemplo

No crea ni reindexa documentos. Consulta un índice Chroma existente.
"""

import argparse
import json
import os
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

MODELO_EMBEDDING = "models/gemini-embedding-001"
MODELO_GENERACION = "gemini-3.1-flash-lite"
RUTA_REGISTROS = Path("registros_latencia_costo.jsonl")

# Precios de referencia en USD por 1 millón de tokens (API Gemini, plan estándar de pago).
# Son ESTIMACIONES de tarifa, no un extracto de facturación. Verificar si cambian.
PRECIOS = {
    "embedding_entrada": 0.15,
    "generacion_entrada": 0.25,
    "generacion_salida": 1.50,
}

PREGUNTAS_BLOQUE_27 = [
    "¿Cuántos intentos hace el cliente ante un TimeoutError y cuánto espera entre cada uno?",
    "¿Qué ocurre cuando hay un error 401 o 403 de credenciales inválidas y cómo se soluciona?",
    "¿Cuál es el límite de peticiones por minuto y qué pasa si se excede?",
]

PROMPT_TEMPLATE = """Responde la pregunta usando SOLO el contexto que sigue.
Cita la fuente de cada afirmación relevante con [1], [2], etc.
Si falta información, dilo claramente sin inventar.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""


@contextmanager
def medir(tiempos: dict, etapa: str):
    inicio = time.perf_counter()
    try:
        yield
    finally:
        tiempos[etapa] = round((time.perf_counter() - inicio) * 1000, 2)


def buscar_indice(embeddings, ruta_solicitada: str | None):
    candidatos = [ruta_solicitada] if ruta_solicitada else [
        "vectorstore", "vectorstore_ejemplo", "vectorstore_bloque28"
    ]
    revisados = []
    for candidato in candidatos:
        if not candidato:
            continue
        carpeta = Path(candidato)
        # Evitar crear un almacén vacío por accidente.
        if not carpeta.is_dir() or not (carpeta / "chroma.sqlite3").is_file():
            revisados.append(f"{candidato}: sin índice Chroma")
            continue
        store = Chroma(
            collection_name="langchain",
            persist_directory=str(carpeta),
            embedding_function=embeddings,
        )
        total = store._collection.count()
        revisados.append(f"{candidato}: {total} chunks")
        if total > 0:
            return store, str(carpeta), total
    raise RuntimeError(
        "No se encontró un índice Chroma con documentos. "
        + " | ".join(revisados)
        + ". Revisa la carpeta usada en el Bloque 24-25."
    )


def formatear_contexto(documentos):
    segmentos = []
    fuentes = []
    for i, doc in enumerate(documentos, start=1):
        fuente = doc.metadata.get("fuente", "sin_metadata") if doc.metadata else "sin_metadata"
        segmentos.append(f"[{i}] Fuente: {fuente}\n{doc.page_content}")
        fuentes.append({"numero": i, "fuente": fuente, "id": doc.id})
    return "\n\n".join(segmentos), fuentes


def contar_tokens_embedding(cliente, pregunta):
    """Cuenta tokens de la consulta en Google; no estima a partir de caracteres.

    Esta es una llamada adicional para estimar costo. NO se suma a la latencia RAG.
    El API de embeddings a través de LangChain solo devuelve el vector, no usage.
    """
    try:
        respuesta = cliente.models.count_tokens(
            model="gemini-embedding-001", contents=pregunta
        )
        return int(respuesta.total_tokens) if respuesta.total_tokens is not None else None
    except Exception as exc:
        print(f"Aviso: no se pudo contar tokens de embedding ({type(exc).__name__}).")
        return None


def estimar_costos(tokens_generacion, tokens_embedding):
    costos = {
        "embedding_usd_estimado": None,
        "generacion_usd_estimado": None,
        "total_usd_estimado": None,
    }
    if tokens_embedding is not None:
        costos["embedding_usd_estimado"] = round(
            tokens_embedding * PRECIOS["embedding_entrada"] / 1_000_000, 9
        )
    if tokens_generacion and all(
        isinstance(tokens_generacion.get(k), int) for k in ("input_tokens", "output_tokens")
    ):
        costos["generacion_usd_estimado"] = round(
            (tokens_generacion["input_tokens"] * PRECIOS["generacion_entrada"]
             + tokens_generacion["output_tokens"] * PRECIOS["generacion_salida"])
            / 1_000_000, 9
        )
    if all(costos[k] is not None for k in ("embedding_usd_estimado", "generacion_usd_estimado")):
        costos["total_usd_estimado"] = round(
            costos["embedding_usd_estimado"] + costos["generacion_usd_estimado"], 9
        )
    return costos


def registrar_consulta(pregunta, k, store, embeddings, modelo, cliente, directorio):
    tiempos = {}

    # Tres mediciones REALES. Búsqueda recibe el vector ya creado: no embebe de nuevo.
    with medir(tiempos, "embedding"):
        vector = embeddings.embed_query(pregunta)

    with medir(tiempos, "busqueda"):
        documentos = store.similarity_search_by_vector(embedding=vector, k=k)

    if not documentos:
        raise RuntimeError("La búsqueda no recuperó documentos; no se generará una respuesta vacía.")

    contexto, fuentes = formatear_contexto(documentos)
    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pregunta=pregunta)

    with medir(tiempos, "generacion"):
        respuesta = modelo.invoke(prompt)

    uso = dict(respuesta.usage_metadata) if respuesta.usage_metadata else None
    tokens_embedding = contar_tokens_embedding(cliente, pregunta)
    # Este campo compuesto conserva la estructura del ejemplo del curso.
    tiempos["embed_y_busqueda"] = round(tiempos["embedding"] + tiempos["busqueda"], 2)
    total = round(
        tiempos["embedding"] + tiempos["busqueda"] + tiempos["generacion"], 2
    )

    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pregunta": pregunta,
        "k": k,
        "tiempos_ms": tiempos,
        "tiempo_total_ms": total,
        "tokens": uso,
        "tokens_embedding_consulta": tokens_embedding,
        "modelo_generacion": MODELO_GENERACION,
        "modelo_embedding": MODELO_EMBEDDING,
        "persist_directory": directorio,
        "chunks_recuperados": len(documentos),
        "fuentes": fuentes,
        "respuesta": str(respuesta.content),
        "costos": estimar_costos(uso, tokens_embedding),
        "nota_costos": "Estimación según tarifa estándar de pago, no importe facturado.",
    }
    return registro


def main():
    parser = argparse.ArgumentParser(description="Mide el CORE 28 con llamadas reales")
    parser.add_argument("--db", default=None, help="Ruta del índice existente")
    args = parser.parse_args()

    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        raise SystemExit("ERROR: configura GEMINI_API_KEY en .env antes de continuar.")

    embeddings = GoogleGenerativeAIEmbeddings(model=MODELO_EMBEDDING)
    store, directorio, total = buscar_indice(embeddings, args.db)
    print(f"Índice: {directorio} | chunks disponibles: {total}")
    if total < 6:
        raise SystemExit(
            "ERROR: k=6 necesita al menos seis chunks distintos para comparar "
            "el contexto y los tokens de entrada. No se enviaron llamadas a Gemini."
        )

    modelo = ChatGoogleGenerativeAI(
        model=MODELO_GENERACION, temperature=0, max_retries=0
    )
    cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    corridas = [(pregunta, 3) for pregunta in PREGUNTAS_BLOQUE_27]
    corridas.append((PREGUNTAS_BLOQUE_27[0], 6))

    # Abrir en modo append: cada corrida exitosa añade exactamente una línea JSON.
    for n, (pregunta, k) in enumerate(corridas, start=1):
        print(f"\n[{n}/{len(corridas)}] k={k} — {pregunta}")
        registro = registrar_consulta(
            pregunta, k, store, embeddings, modelo, cliente, directorio
        )
        with RUTA_REGISTROS.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
        print(json.dumps({
            "timestamp": registro["timestamp"],
            "pregunta": registro["pregunta"],
            "k": registro["k"],
            "tiempos_ms": registro["tiempos_ms"],
            "tiempo_total_ms": registro["tiempo_total_ms"],
            "tokens": registro["tokens"],
            "chunks_recuperados": registro["chunks_recuperados"],
            "costos": registro["costos"],
        }, indent=2, ensure_ascii=False))
    print(f"\nListo: cuatro registros reales añadidos a {RUTA_REGISTROS}")


if __name__ == "__main__":
    main()

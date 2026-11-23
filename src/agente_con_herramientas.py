"""SIGRA: agente de práctica con herramientas verificables, memoria y trazas.

Ejecutar desde la raíz de ProyectoIA:
    python -m src.agente_con_herramientas
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from src.sigra.herramientas import (
    CONTENIDOS,
    consultar_contenido_logica,
    evaluar_respuesta_logica,
)

load_dotenv()
clave = os.getenv("GEMINI_API_KEY")
modelo_nombre = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
if not clave:
    raise ValueError("Falta GEMINI_API_KEY en .env")


@tool
def consultar_contenido(consulta: str) -> str:
    """Busca un ejercicio de SIGRA. Acepta código 5B, '5 básico', 'quinto básico',
    o una frase como 'quiero practicar fracciones de 5 básico'.
    Devuelve únicamente ejercicios disponibles; no inventes códigos.
    """
    return consultar_contenido_logica(consulta)


@tool
def evaluar_respuesta(codigo: str, respuesta_estudiante: str) -> str:
    """Comprueba la respuesta del ejercicio actual. Código EXACTO 1B..8B;
    recibe respuesta literal: p. ej. '2/3', '4/6', '50,0', 'x=5'.
    Solo úsala si está claro cuál fue el último ejercicio mostrado.
    """
    return evaluar_respuesta_logica(codigo, respuesta_estudiante)


modelo = ChatGoogleGenerativeAI(
    model=modelo_nombre,
    api_key=clave,
    temperature=0,
    timeout=20,
    max_retries=0,
)
herramientas = [consultar_contenido, evaluar_respuesta]

instrucciones = (
    "Eres SIGRA, asistente de práctica matemática para estudiantes de 1° a 8° básico. "
    "Responde en español claro. Usa consultar_contenido para presentar un ejercicio. "
    "Usa evaluar_respuesta para corregir la respuesta dada por el estudiante. "
    "El ÚNICO conjunto de códigos válidos es 1B, 2B, 3B, 4B, 5B, 6B, 7B y 8B. "
    "Nunca inventes códigos ni respuestas correctas. "
    "Para una respuesta breve del estudiante (p. ej. '2/3'), identifica en el historial "
    "cuál fue el último ejercicio mostrado y usa su código al evaluar. "
    "Si no hay un ejercicio previo o el contexto es ambiguo, pregunta cuál ejercicio resolvió. "
    "No reveles la solución antes de recibir la respuesta. "
    "Presenta las observaciones de las herramientas fielmente: si la herramienta "
    "devuelve Error, no declares correcta o incorrecta la respuesta. "
    "No utilices un ejercicio para emitir un diagnóstico definitivo. "
    "No modifiques registros ni calificaciones. "
    "Para saludos, responde directamente sin herramientas."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", instrucciones),
    MessagesPlaceholder("chat_history"),
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad"),
])
agente = create_tool_calling_agent(llm=modelo, tools=herramientas, prompt=prompt)
ejecutor = AgentExecutor(
    agent=agente,
    tools=herramientas,
    return_intermediate_steps=True,
    verbose=False,
    max_iterations=4,
)


def salida_texto(salida):
    """Algunos modelos devuelven una lista de bloques de texto."""
    if isinstance(salida, str):
        return salida
    if isinstance(salida, list):
        return "\n".join(
            bloque.get("text", "") for bloque in salida
            if isinstance(bloque, dict) and bloque.get("type") == "text"
        )
    return str(salida)


normalizar_salida = RunnableLambda(
    lambda dic: {**dic, "output": salida_texto(dic.get("output"))}
)

# La memoria es independiente por session_id. Se pierde al cerrar el proceso.
historiales = {}


def obtener_historial(session_id: str):
    if session_id not in historiales:
        historiales[session_id] = InMemoryChatMessageHistory()
    return historiales[session_id]


agente_con_memoria = RunnableWithMessageHistory(
    ejecutor | normalizar_salida,
    obtener_historial,
    input_messages_key="entrada",
    history_messages_key="chat_history",
    output_messages_key="output",
)


def registrar_traza(session_id, entrada, pasos, respuesta):
    """Solo utilice entradas de prueba: el archivo incluye texto de la conversación."""
    acciones = [
        {
            "herramienta": accion.tool,
            "argumentos": accion.tool_input,
            "observacion": str(observacion),
        }
        for accion, observacion in pasos
    ]
    registro = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "entrada": entrada,
        "acciones": acciones,
        "respuesta_final": str(respuesta),
    }
    with Path("trazas_agente.jsonl").open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")


def probar(entrada: str, session_id="sesion_demo_1"):
    resultado = agente_con_memoria.invoke(
        {"entrada": entrada},
        config={"configurable": {"session_id": session_id}},
    )
    pasos = resultado.get("intermediate_steps", [])
    salida = salida_texto(resultado.get("output"))
    registrar_traza(session_id, entrada, pasos, salida)

    print("\nTRAZA DE HERRAMIENTAS:")
    if not pasos:
        print("No se utilizaron herramientas.")
    for numero, (accion, observacion) in enumerate(pasos, start=1):
        print(f"Paso {numero} | Herramienta: {accion.tool}")
        print("Argumentos:", accion.tool_input)
        print("Observación:", observacion)
    print("\nRESPUESTA FINAL:")
    print(salida)


if __name__ == "__main__":
    print("SIGRA — Herramientas + memoria + trazas (solo pruebas simuladas)")
    print("Contenidos:", ", ".join(f"{k}: {v['nombre']}" for k, v in CONTENIDOS.items()))
    print("Para conservar el contexto, todas las preguntas usan la sesión 'sesion_demo_1'.")
    print("Escribe 'salir' para terminar.")
    while True:
        entrada = input("\nTu pregunta: ").strip()
        if entrada.casefold() == "salir":
            break
        if entrada:
            probar(entrada)

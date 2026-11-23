"""CORE Bloque 28: comprobar el JSONL y comparar k=3 frente a k=6."""

import json
from pathlib import Path

ruta = Path("registros_latencia_costo.jsonl")
if not ruta.is_file():
    raise SystemExit(f"ERROR: no existe {ruta}")

with ruta.open(encoding="utf-8") as archivo:
    registros = [json.loads(linea) for linea in archivo if linea.strip()]

print(f"Registros históricos: {len(registros)}")
recientes = registros[-4:]
for n, r in enumerate(recientes, 1):
    t = r["tiempos_ms"]
    u = r["tokens"] or {}
    print(
        f"{n}. k={r['k']} | recuperados={r.get('chunks_recuperados', '?')} | "
        f"embed={t.get('embedding')} ms | búsqueda={t.get('busqueda')} ms | "
        f"generación={t.get('generacion')} ms | total={r['tiempo_total_ms']} ms | "
        f"entrada={u.get('input_tokens')} | salida={u.get('output_tokens')} | "
        f"costo estimado USD={r.get('costos', {}).get('total_usd_estimado')}"
    )

if len(recientes) != 4:
    raise SystemExit("Faltan corridas: deben ser cuatro (tres preguntas y comparación de k).")

preguntas = {r["pregunta"] for r in recientes}
print("Preguntas distintas:", len(preguntas))
if len(preguntas) < 3:
    raise SystemExit("ERROR: faltan tres preguntas diferentes.")

comparables = [
    r for r in recientes if r["pregunta"] == recientes[0]["pregunta"]
]
por_k = {r["k"]: r for r in comparables}
if 3 not in por_k or 6 not in por_k:
    raise SystemExit("ERROR: falta comparación de la misma pregunta con k=3 y k=6.")

entrada_3 = (por_k[3]["tokens"] or {}).get("input_tokens")
entrada_6 = (por_k[6]["tokens"] or {}).get("input_tokens")
print(f"Comparación de tokens de entrada: k=3 -> {entrada_3}; k=6 -> {entrada_6}")
if entrada_3 is None or entrada_6 is None:
    print("ATENCIÓN: alguna llamada no devolvió usage_metadata; no inventar tokens.")
elif entrada_6 > entrada_3:
    print("OK: aumentar k incrementó el contexto y los tokens de entrada.")
else:
    print("ATENCIÓN: k=6 no aumentó tokens; revisar chunks recuperados y textos del contexto.")

for r in recientes:
    etapas = r["tiempos_ms"]
    lenta = max(("embedding", "busqueda", "generacion"), key=lambda x: etapas[x])
    print(f"k={r['k']}: etapa más lenta = {lenta}")

print("Validación de estructura JSONL y comparación finalizadas.")

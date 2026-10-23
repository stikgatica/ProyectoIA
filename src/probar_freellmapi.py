"""Prueba independiente de FreeLLMAPI para SIGRA.

No modifica src/consumir_gemini.py.
Requiere: pip install requests python-dotenv
"""
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Admite ejecutarse desde src/ o desde la raíz del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parent
if PROJECT_ROOT.name == "src":
    PROJECT_ROOT = PROJECT_ROOT.parent
load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("FREELLMAPI_API_KEY", "").strip()
BASE_URL = os.getenv("FREELLMAPI_BASE_URL", "http://127.0.0.1:3001/v1").rstrip("/")
MODEL = os.getenv("FREELLMAPI_MODEL", "auto").strip()

if not API_KEY:
    raise SystemExit("Falta FREELLMAPI_API_KEY en el archivo .env del proyecto.")

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "Eres un asistente pedagógico de Matemática para educación básica de Chile. Responde en español claro."},
        {"role": "user", "content": "Explica brevemente qué son las fracciones equivalentes y entrega un ejemplo correcto para 6.º básico."},
    ],
    "temperature": 0.2,
    "max_tokens": 350,
}

print(f"Probando FreeLLMAPI en {BASE_URL} | modelo solicitado: {MODEL}")
start = time.perf_counter()
try:
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload,
        timeout=(5, 60),
    )
    response.raise_for_status()
    result = response.json()
    choices = result.get("choices", [])
    answer = choices[0].get("message", {}).get("content", "") if choices else ""
    if not answer:
        raise ValueError("La API respondió sin contenido en choices[0].message.content")
    print("\nRESPUESTA:\n" + str(answer))
    print(f"\nTiempo: {time.perf_counter() - start:.2f} s")
    print("Modelo declarado:", result.get("model", "no informado"))
    print("Proveedor real:", response.headers.get("X-Routed-Via", "no informado"))
    print("Reintentos/fallback:", response.headers.get("X-Fallback-Attempts", "no informado"))
    if result.get("usage"):
        print("Consumo informado:", json.dumps(result["usage"], ensure_ascii=False))
except requests.exceptions.ConnectionError:
    print("ERROR: no se pudo conectar. Verifica que FreeLLMAPI esté abierto y el puerto sea correcto.")
except requests.exceptions.Timeout:
    print("ERROR: la solicitud superó el tiempo de espera.")
except requests.exceptions.HTTPError:
    print(f"ERROR HTTP {response.status_code}: {response.text[:1000]}")
except (requests.exceptions.RequestException, ValueError) as exc:
    print(f"ERROR: {exc}")

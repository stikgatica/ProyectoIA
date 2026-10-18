import os
import requests
from dotenv import load_dotenv

load_dotenv()

MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")


#función para crear la solicitud
def armar_peticion(pregunta):
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"
    body = {
        "contents": [{"parts": [{"text": pregunta}]}]
    }
    return url, body

#función envía petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar al servidor. Verifica tu conexión a internet.")
    except requests.exceptions.Timeout:
        raise RuntimeError("Se agoto el tiempo. Intenta de nuevo en unso momentos.")

    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la solicitud: {respuesta.status_code} - {respuesta.text}")

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servidor no es un JSON válido.")

#funcion procesa y extra dato
def extraer_texto(datos):
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]  
    except (KeyError, IndexError):
        raise RuntimeError("No se pudo extraer el texto de la respuesta.")

def obtener_dato_de_prueba(pregunta):
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    return extraer_texto(datos)


try:
    print(obtener_dato_de_prueba("Confirma mi conexion a Gemini"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)
import os
import requests
from dotenv import load_dotenv

import time

load_dotenv()

MODELO = "gemini-3.1-flash-lite"
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
        raise RuntimeError("Se agoto el tiempo. Intenta de nuevo en unos momentos.")

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

    inicio = time.perf_counter()

    datos = enviar_peticion(url, body) #Respuesta en Json

    fin = time.perf_counter()
    latencia = fin - inicio
    print(f"Latencia de la operación: {latencia:.2f} segundos")

    datos = enviar_peticion(url, body)
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo estimado de la operación: ${costo:.6f} USD")
    return extraer_texto(datos)

def calcular_costo(datos, precio_entrada, precio_salida):
    uso = datos["usageMetadata"]
    '''
    uso = {
        "promptTokenCount": 83,
        "candidatesTokenCount": 471,
        "totalTokenCount": 1377,
        "promptTokensDetails": [
            {
                "modality": "TEXT",
                "tokenCount": 10
            }
        ],
        "thoughtsTokenCount": 896,
        "serviceTier": "standard"
    }
    '''
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0)
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo


try:
    print(obtener_dato_de_prueba("Quiero crear un pequeño prototipo de mi proyecto SIGRA (Sistema Inteligente de Generación de Rutas de Aprendizaje).El objetivo es simular una red de relaciones entre Objetivos de Aprendizaje (OA) de Matemática de 1° a 8° básico. Como comienzo?"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)

'''
Ejecutar 4 veces la misma con 1 modelo
y ante cada se calcule e imprima latencai costo respuesta
Vuelvo a hacer lo mismo con un modelo distitno
3 modelos a comprara
Objetivo: Elijas el mejor modelo para tí

Prompt algo relacionado con tu proyecto

'''





from collections import Counter
import json

from src.pipeline_limpieza import procesar_texto
from src.cliente import consultar_modelo


# ==========================================
# PARTE 1: FUNCIONES
# ==========================================

def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)

    interseccion = conteo_referencia & conteo_respuesta

    return sum(interseccion.values())


def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""

    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {
            "precision": 0.0,
            "cobertura": 0.0,
            "f1": 0.0,
        }

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    return {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }


def calcular_metricas(texto_referencia, texto_respuesta):
    """Procesa los textos y calcula sus métricas."""

    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )


def resumir_metricas(resultados):
    """Calcula los promedios de precisión, cobertura y F1."""

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,
        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,
        "f1_promedio": sum(
            r["f1"] for r in resultados
        ) / n,
    }


# ==========================================
# PARTE 2: EJECUCIÓN DE LAS PRUEBAS
# ==========================================

if __name__ == "__main__":

    casos = [
        (
            "¿Qué es una variable en Python?",
            "Una variable es un nombre que referencia un valor.",
        ),
        (
            "¿Qué es una tupla?",
            "Una tupla es una colección ordenada e inmutable.",
        ),
        (
            "¿Qué es un diccionario en Python?",
            "Un diccionario almacena pares de clave y valor.",
        ),
        (
            "¿Qué es un conjunto en Python?",
            "Un conjunto es una colección de elementos únicos.",
        ),
        (
            "¿Qué es un bucle for?",
            "Un bucle for permite recorrer elementos de un iterable.",
        ),
        (
            "¿Qué es un bucle while?",
            "Un bucle while repite instrucciones mientras una condición sea verdadera.",
        ),
        (
            "¿Para qué sirve if en Python?",
            "If permite ejecutar código cuando se cumple una condición.",
        ),
        (
            "¿Qué es una función en Python?",
            "Una función es un bloque de código reutilizable.",
        ),
        (
            "¿Para qué sirve return?",
            "Return finaliza una función y permite devolver un valor.",
        ),
        (
            "¿Qué hace len()?",
            "Len devuelve la cantidad de elementos de un objeto.",
        ),
        (
            "¿Qué hace append() en una lista?",
            "Append agrega un elemento al final de una lista.",
        ),
        (
            "¿Qué es un string?",
            "Un string es una secuencia de caracteres de texto.",
        ),
        (
            "¿Qué es un booleano?",
            "Un booleano es un valor lógico verdadero o falso.",
        ),
        (
            "¿Qué es un módulo en Python?",
            "Un módulo es un archivo Python que contiene código reutilizable.",
        ),
        (
            "¿Para qué sirve import?",
            "Import permite acceder a módulos y sus componentes.",
        ),
        (
            "¿Qué es una excepción en Python?",
            "Una excepción es un evento que interrumpe el flujo normal del programa.",
        ),
        (
            "¿Para qué sirve json.dump()?",
            "Json.dump serializa un objeto Python y lo escribe en un archivo.",
        ),
    ]

    resultados = []

    for consulta, referencia in casos:

        respuesta = consultar_modelo(
            consulta,
            system_instruction=(
                "Responde en español con una definición breve, "
                "en una sola oración de máximo 15 palabras. "
                "Sin listas, ejemplos ni introducciones."
            ),
        )

        metricas = calcular_metricas(referencia, respuesta)

        print("Consulta:", consulta)
        print("Referencia:", referencia)
        print("Respuesta:", respuesta)
        print("Métricas:", metricas)
        print("-" * 50)

        resultados.append({
            "consulta": consulta,
            "referencia": referencia,
            "respuesta": respuesta,
            **metricas,
        })

    # Ordenar resultados de menor a mayor F1
    resultados = sorted(
        resultados,
        key=lambda r: r["f1"]
    )

    # Guardar resultados en JSON
    with open(
        "resultados_metricas.json",
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            resultados,
            archivo,
            indent=2,
            ensure_ascii=False
        )

    # Mostrar promedios
    print("\nPROMEDIOS")
    print(resumir_metricas(resultados))

    # Mostrar los tres casos con menor F1
    print("\nCASOS CON MENOR F1")

    peores_casos = resultados[:3]

    for caso in peores_casos:
        print(
            caso["consulta"],
            "F1:",
            caso["f1"]
        )

    
# referencia = procesar_texto(
#     "Python es un lenguaje de programación interpretado."
# )

# texto_respuesta = consultar_modelo("¿Qué es Python?",
#                                    system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)
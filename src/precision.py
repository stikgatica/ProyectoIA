
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

        # 1° BÁSICO
        (
            "1° básico: Si tienes 4 fichas y agregas 3, ¿cuántas tienes?",
            "Tienes 7 fichas porque 4 más 3 es igual a 7.",
        ),
        (
            "1° básico: ¿Qué número viene después de 19?",
            "Después de 19 viene el número 20.",
        ),

        # 2° BÁSICO
        (
            "2° básico: ¿Cuánto es 14 menos 6?",
            "14 menos 6 es igual a 8.",
        ),
        (
            "2° básico: ¿Cuánto es 3 más 3 más 3?",
            "La suma es 9 y representa tres grupos de 3.",
        ),

        # 3° BÁSICO
        (
            "3° básico: ¿Cuánto es 6 multiplicado por 4?",
            "6 multiplicado por 4 es igual a 24.",
        ),
        (
            "3° básico: Si repartes 20 objetos en 5 grupos iguales, ¿cuántos objetos van en cada grupo?",
            "En cada grupo van 4 objetos porque 20 dividido por 5 es 4.",
        ),
        (
            "3° básico: ¿Qué valor tiene el dígito 7 en el número 374?",
            "El dígito 7 representa 70 unidades, equivalentes a siete decenas.",
        ),

        # 4° BÁSICO
        (
            "4° básico: ¿Cuál es una fracción equivalente a un medio?",
            "Dos cuartos es una fracción equivalente a un medio.",
        ),
        (
            "4° básico: ¿Cuánto es 36 dividido por 6?",
            "36 dividido por 6 es igual a 6.",
        ),
        (
            "4° básico: ¿Cuál es el perímetro de un rectángulo de lados 5 cm y 3 cm?",
            "El perímetro es 16 centímetros porque se suman las longitudes de sus cuatro lados.",
        ),

        # 5° BÁSICO
        (
            "5° básico: ¿Qué suma es imposible al lanzar dos dados de seis caras?",
            "La suma 1 es imposible porque el resultado mínimo al lanzar dos dados es 2.",
        ),
        (
            "5° básico: ¿Cuánto es un tercio más un tercio?",
            "Un tercio más un tercio es igual a dos tercios.",
        ),

        # 6° BÁSICO
        (
            "6° básico: ¿Qué representa el tallo en un diagrama de tallo y hojas de números de dos cifras?",
            "El tallo representa las decenas y las hojas representan las unidades.",
        ),
        (
            "6° básico: ¿Cuánto es el 25 por ciento de 80?",
            "El 25 por ciento de 80 es 20 porque representa su cuarta parte.",
        ),
        (
            "6° básico: ¿Qué operación se realiza primero en 6 + 2 × 3?",
            "Primero se multiplica 2 por 3 y después se suma 6, obteniendo 12.",
        ),

        # 7° BÁSICO
        (
            "7° básico: ¿Cuál es el área de un paralelogramo con base 7 cm y altura 4 cm?",
            "El área es 28 centímetros cuadrados porque se multiplica la base por la altura.",
        ),
        (
            "7° básico: ¿Cuál es el área de un trapecio con bases de 8 cm y 4 cm y altura de 3 cm?",
            "El área es 18 centímetros cuadrados porque se suman las bases, se multiplica por la altura y se divide por dos.",
        ),

        # 8° BÁSICO
        (
            "8° básico: ¿Dónde queda el punto (2, 3) al trasladarlo 4 unidades a la derecha?",
            "El punto se traslada hasta las coordenadas (6, 3).",
        ),
        (
            "8° básico: ¿Dónde queda el punto (3, 2) al reflejarlo respecto del eje X?",
            "El punto reflejado es (3, -2) porque cambia el signo de la coordenada vertical.",
        ),
        (
            "8° básico: ¿Dónde queda el punto (1, 2) después de reflejarlo en el eje Y y trasladarlo tres unidades a la derecha?",
            "El punto pasa primero a (-1, 2) y después termina en (2, 2).",
        ),
    ]

    # Archivo exclusivo para las pruebas de SIGRA
    archivo_resultados = "resultados_metricas_sigra.json"

    # Recuperar resultados anteriores
    try:
        with open(
            archivo_resultados,
            "r",
            encoding="utf-8"
        ) as archivo:

            resultados = json.load(archivo)

        if not isinstance(resultados, list):
            raise ValueError("El JSON debe contener una lista.")

    except FileNotFoundError:
        resultados = []

    # Identificar consultas ya guardadas
    consultas_guardadas = {
        r["consulta"] for r in resultados
    }

    print("Resultados recuperados:", len(resultados))

    for consulta, referencia in casos:

        # Evitar repetir consultas ya evaluadas
        if consulta in consultas_guardadas:
            print("Consulta ya evaluada:", consulta)
            continue

        try:
            respuesta = consultar_modelo(
                consulta,
                system_instruction=(
                    "Responde en español con lenguaje matemático claro, "
                    "en una sola oración breve de máximo 25 palabras. "
                    "Entrega el resultado y explica brevemente el procedimiento "
                    "cuando corresponda. Sin listas ni introducciones."
                ),
            )

        except TimeoutError as error:
            print("Error:", error)
            print("Se conservan los resultados guardados.")
            break

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

        consultas_guardadas.add(consulta)

        # Ordenar resultados de menor a mayor F1
        resultados = sorted(
            resultados,
            key=lambda r: r["f1"]
        )

        # Guardar resultados en JSON después de cada consulta
        with open(
            archivo_resultados,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                resultados,
                archivo,
                indent=2,
                ensure_ascii=False
            )

        print("Resultados guardados:", len(resultados))

    # Mostrar promedios
    print("\nPROMEDIOS")
    print(resumir_metricas(resultados))

    # Mostrar los tres casos con menor F1
    print("\nCASOS CON MENOR F1")

    peores_casos = sorted(
        resultados,
        key=lambda r: r["f1"]
    )[:3]

    for caso in peores_casos:
        print(
            caso["consulta"],
            "F1:",
            caso["f1"]
        )


# referencia = procesar_texto(
#     "Tienes 7 fichas porque 4 más 3 es igual a 7."
# )

# texto_respuesta = consultar_modelo("1° básico: Si tienes 4 fichas y agregas 3, ¿cuántas tienes?",
#                                    system_instruction="Responde en español con lenguaje matemático claro, en una sola oración breve de máximo 25 palabras.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)

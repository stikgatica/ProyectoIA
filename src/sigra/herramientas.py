"""Herramientas deterministas de práctica matemática para SIGRA.

No dependen de Gemini, LangChain ni credenciales: pueden probarse sin conexión.
Los ejercicios son ejemplos, no diagnósticos oficiales ni OA MINEDUC.
"""

from decimal import Decimal, InvalidOperation
from fractions import Fraction
import re
import unicodedata

CONTENIDOS = {
    "1B": {"nombre": "Sumas y restas hasta 20", "nivel": 1, "pregunta": "8 + 5", "respuesta": 13},
    "2B": {"nombre": "Sumas y restas hasta 100", "nivel": 2, "pregunta": "34 - 17", "respuesta": 17},
    "3B": {"nombre": "Multiplicación", "nivel": 3, "pregunta": "6 × 4", "respuesta": 24},
    "4B": {"nombre": "División", "nivel": 4, "pregunta": "48 ÷ 6", "respuesta": 8},
    "5B": {"nombre": "Fracciones", "nivel": 5, "pregunta": "1/3 + 1/3", "respuesta": "2/3"},
    "6B": {"nombre": "Porcentajes", "nivel": 6, "pregunta": "25% de 200", "respuesta": 50},
    "7B": {"nombre": "Números enteros", "nivel": 7, "pregunta": "-8 + 13", "respuesta": 5},
    "8B": {"nombre": "Ecuaciones", "nivel": 8, "pregunta": "3x + 5 = 20. ¿Cuánto vale x?", "respuesta": 5},
}

_ALIASES = {
    "1B": ("sumas", "suma", "restas", "resta", "sumas y restas"),
    "2B": ("sumas", "suma", "restas", "resta", "sumas y restas"),
    "3B": ("multiplicacion", "multiplicaciones", "multiplicar"),
    "4B": ("division", "divisiones", "dividir"),
    "5B": ("fraccion", "fracciones", "fracciones equivalentes"),
    "6B": ("porcentaje", "porcentajes"),
    "7B": ("numeros enteros", "numero entero", "enteros"),
    "8B": ("ecuacion", "ecuaciones", "resolver ecuaciones"),
}

# Acepta enteros, decimales y cocientes; no evalúa expresiones arbitrarias.
_NUMERO = r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)"
_LITERAL = re.compile(rf"({_NUMERO})(?:/({_NUMERO}))?\Z")


def _normalizar(texto: str) -> str:
    texto = texto.strip().casefold().replace("º", "°")
    return "".join(
        letra for letra in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(letra)
    )


def _contiene(texto: str, palabra: str) -> bool:
    return bool(re.search(r"(?<![a-z0-9])" + re.escape(palabra) + r"(?![a-z0-9])", texto))


def identificar_codigo(consulta: str) -> str | None:
    """Resuelve una consulta natural o un código a un código conocido.

    Evita escoger un grado incorrecto cuando tema y nivel se contradicen.
    Si 'sumas' es ambiguo entre 1B y 2B, solicita el nivel.
    """
    if not isinstance(consulta, str):
        return None
    texto = _normalizar(consulta)
    if not texto:
        return None

    nivel = re.search(
        r"(?<![a-z0-9])([1-8])\s*(?:°\s*)?b(?:asico)?(?![a-z0-9])",
        texto,
    )
    if not nivel:
        nivel = re.search(r"(?<![a-z0-9])([1-8])°(?![a-z0-9])", texto)
    if not nivel and re.fullmatch(r"[1-8]", texto):
        nivel = re.fullmatch(r"([1-8])", texto)

    codigo_nivel = f"{nivel.group(1)}B" if nivel else None
    temas = {
        codigo for codigo, aliases in _ALIASES.items()
        if any(_contiene(texto, alias) for alias in aliases)
    }

    if codigo_nivel:
        # El código/nivel concreto tiene preferencia si se identifica su tema.
        if not temas or codigo_nivel in temas:
            return codigo_nivel
        return None
    if len(temas) == 1:
        return next(iter(temas))
    return None


def consultar_contenido(consulta: str) -> str:
    """Devuelve el ejercicio de práctica vinculado con la consulta."""
    codigo = identificar_codigo(consulta)
    if codigo is None:
        return (
            "Contenido no encontrado o ambiguo. "
            "Indica el curso (por ejemplo, 5B) y el contenido."
        )
    contenido = CONTENIDOS[codigo]
    return (
        f"Contenido: {contenido['nombre']}. "
        f"Nivel: {contenido['nivel']}° básico. "
        f"Código: {codigo}. "
        f"Ejercicio diagnóstico: {contenido['pregunta']}."
    )


def _valor_exacto(texto: str, *, permitir_variable: bool = False) -> Fraction | None:
    if not isinstance(texto, str):
        return None
    limpio = texto.strip().casefold().replace("−", "-")
    limpio = re.sub(r"\s+", "", limpio).replace(",", ".")
    if permitir_variable and limpio.startswith("x="):
        limpio = limpio[2:]
    coincidencia = _LITERAL.fullmatch(limpio)
    if not coincidencia:
        return None
    try:
        numerador = Fraction(Decimal(coincidencia.group(1)))
        denominador = (
            Fraction(Decimal(coincidencia.group(2)))
            if coincidencia.group(2) is not None else Fraction(1)
        )
        return numerador / denominador
    except (InvalidOperation, ValueError, ZeroDivisionError, OverflowError):
        return None


def evaluar_respuesta(codigo: str, respuesta_estudiante: str) -> str:
    """Evalúa el valor matemático exacto sin ejecutar expresiones de Python."""
    codigo_canonico = identificar_codigo(codigo)
    if codigo_canonico is None:
        return "Error: el código del contenido no existe o es ambiguo."

    contenido = CONTENIDOS[codigo_canonico]
    if not isinstance(respuesta_estudiante, str) or not respuesta_estudiante.strip():
        return "Error: el estudiante debe proporcionar una respuesta."

    respuesta = _valor_exacto(
        respuesta_estudiante, permitir_variable=(codigo_canonico == "8B")
    )
    if respuesta is None:
        return (
            "Error: formato de respuesta no reconocido. "
            "Escribe un número, una fracción o x=valor en ecuaciones."
        )

    correcta = _valor_exacto(str(contenido["respuesta"]))
    encabezado = (
        f"Contenido: {contenido['nombre']}. "
        f"Nivel: {contenido['nivel']}° básico. "
    )
    if respuesta == correcta:
        return (
            "Resultado: correcto. " + encabezado +
            "Retroalimentación: ¡Muy bien! Resolviste correctamente el ejercicio. "
            "Ruta sugerida: continuar con ejercicios de mayor complejidad "
            "del mismo contenido."
        )
    return (
        "Resultado: incorrecto. " + encabezado +
        f"Respuesta esperada: {contenido['respuesta']}. "
        "Retroalimentación: revisemos el procedimiento paso a paso. "
        "Ruta sugerida: reforzar los conocimientos previos y practicar "
        "con ejercicios más sencillos del mismo contenido."
    )

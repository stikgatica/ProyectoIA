"""Lógica verificable de las herramientas de práctica de SIGRA.

Este módulo NO usa Gemini y puede probarse sin red ni claves API.
El banco es demostrativo: un ejercicio por nivel, no un diagnóstico real.
"""
from __future__ import annotations

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


NUMEROS_CURSOS = {
    "primero": 1, "primer": 1, "segundo": 2, "tercero": 3,
    "tercer": 3, "cuarto": 4, "quinto": 5, "sexto": 6,
    "septimo": 7, "octavo": 8,
}


def normalizar(texto: str) -> str:
    sin_tildes = "".join(
        caracter for caracter in unicodedata.normalize("NFKD", texto.casefold())
        if not unicodedata.combining(caracter)
    )
    return re.sub(r"\s+", " ", sin_tildes).strip()


def _extraer_curso(texto: str) -> int | None:
    encontrado = re.search(r"(?<!\d)([1-8])\s*(?:°|º|o|to|er)?\s*basico\b", texto)
    if encontrado:
        return int(encontrado.group(1))
    for palabra, curso in NUMEROS_CURSOS.items():
        if re.search(rf"\b{palabra}\s+basico\b", texto):
            return curso
    return None


def consultar_contenido_logica(consulta: str) -> str:
    """Selecciona solamente códigos, cursos y temas realmente presentes en el banco."""
    texto = normalizar(consulta)
    if not texto:
        return "Consulta vacía. Indica un curso entre 1° y 8° básico o un código como 5B."

    # Rechaza referencias internas inventadas (ej. 5B-fracciones-suma).
    if re.search(r"\b[1-8]b-[\w-]+", texto):
        return "Código no válido. Los códigos admitidos son 1B, 2B, ..., 8B."

    coincidencia_codigo = re.search(r"(?<![\w])([1-8])\s*b(?![\w])", texto)
    codigo = f"{coincidencia_codigo.group(1)}B" if coincidencia_codigo else None
    curso = _extraer_curso(texto)

    # El banco de ejemplo contiene SUMA de fracciones, no equivalencias.
    if "fraccion" in texto and "equivalent" in texto:
        return "Aún no hay un ejercicio de fracciones equivalentes en este banco de práctica."

    temas = {
        "fraccion": "5B",
        "porcentaje": "6B",
        "multiplicacion": "3B",
        "division": "4B",
        "numero entero": "7B",
        "enteros": "7B",
        "ecuacion": "8B",
    }
    codigos_tema = {
        valor for patron, valor in temas.items() if patron in texto
    }
    if "suma" in texto or "resta" in texto:
        # Sumas/restas del banco existen en 1° y 2° básico.
        if curso in (1, 2):
            codigos_tema.add(f"{curso}B")
        elif codigo in ("1B", "2B"):
            codigos_tema.add(codigo)
        else:
            return "Especifica si necesitas sumas y restas de 1° o 2° básico."

    if len(codigos_tema) > 1:
        return "Consulta ambigua: menciona varios contenidos. Pide solo uno."
    tema_codigo = next(iter(codigos_tema), None)

    if codigo and curso and int(codigo[0]) != curso:
        return "El código y el curso indicado no coinciden. Aclara cuál deseas practicar."
    if tema_codigo and curso and int(tema_codigo[0]) != curso:
        return "Ese contenido no está disponible para el curso solicitado en el banco de ejemplo."
    if codigo and tema_codigo and codigo != tema_codigo:
        return "El código y el contenido indicado no coinciden. Aclara cuál necesitas."

    seleccionado = codigo or tema_codigo or (f"{curso}B" if curso else None)
    if seleccionado not in CONTENIDOS:
        return "Contenido no encontrado. Indica un código entre 1B y 8B o un curso disponible."

    item = CONTENIDOS[seleccionado]
    return (
        f"Contenido: {item['nombre']}. Nivel: {item['nivel']}° básico. "
        f"Código: {seleccionado}. Ejercicio diagnóstico: {item['pregunta']}."
    )


def _interpretar_numero(texto: str, permitir_x: bool) -> Fraction:
    valor = texto.strip().lower().replace(" ", "").replace(",", ".")
    if permitir_x and valor.startswith("x="):
        valor = valor[2:]
    # Aceptar enteros, decimales y fracciones exactas; no ejecutar expresiones.
    if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?(?:/[+-]?\d+(?:\.\d+)?)?", valor):
        raise ValueError("Formato no reconocido")
    return Fraction(valor)


def evaluar_respuesta_logica(codigo: str, respuesta_estudiante: str) -> str:
    """Evalúa igualdad matemática exacta en el pequeño banco de demostración."""
    clave = codigo.strip().upper()
    if clave not in CONTENIDOS:
        return "Error: el código del contenido no existe. Usa uno de 1B a 8B."
    if not respuesta_estudiante.strip():
        return "Error: el estudiante debe proporcionar una respuesta."

    contenido = CONTENIDOS[clave]
    try:
        recibido = _interpretar_numero(respuesta_estudiante, permitir_x=(clave == "8B"))
        esperado = _interpretar_numero(str(contenido["respuesta"]), permitir_x=False)
    except (ValueError, ZeroDivisionError):
        return (
            "Error: formato de respuesta no reconocido. "
            "Escribe un número (50, 50,0), una fracción (2/3, 4/6) "
            "o x=5 para ecuaciones. No se calificó esta respuesta."
        )

    if recibido == esperado:
        return (
            f"Resultado: correcto. Contenido: {contenido['nombre']}. "
            f"Nivel: {contenido['nivel']}° básico. "
            "Retroalimentación: ¡Muy bien! Tu respuesta es matemáticamente equivalente "
            "a la solución del ejercicio. Ruta sugerida: practicar un ejercicio nuevo "
            "del mismo contenido, si está disponible."
        )

    return (
        f"Resultado: incorrecto. Contenido: {contenido['nombre']}. "
        f"Nivel: {contenido['nivel']}° básico. "
        f"Respuesta esperada: {contenido['respuesta']}. "
        "Retroalimentación: revisemos el procedimiento paso a paso. "
        "Ruta sugerida: reforzar conocimientos previos y practicar."
    )

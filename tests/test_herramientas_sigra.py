"""Tests locales, sin costo de API ni llamadas a Gemini."""
import pytest

from src.sigra.herramientas import (
    CONTENIDOS,
    consultar_contenido_logica,
    evaluar_respuesta_logica,
)


@pytest.mark.parametrize("consulta", [
    "5B", "Fracciones", "5 básico", "5° básico",
    "Quiero practicar fracciones de quinto básico",
    "Quiero practicar fracciones de 5 básico",
])
def test_consulta_fracciones(consulta):
    assert "Código: 5B." in consultar_contenido_logica(consulta)


def test_rechaza_curso_y_contenido_incompatibles():
    assert "no está disponible" in consultar_contenido_logica("fracciones de sexto básico")


def test_rechaza_contenido_que_no_hay_en_banco():
    assert "Aún no hay" in consultar_contenido_logica("fracciones equivalentes")


def test_rechaza_codigo_inventado():
    assert "Código no válido" in consultar_contenido_logica("5B-fracciones-suma")
    assert "no existe" in evaluar_respuesta_logica("5B-fracciones-suma", "2/3")


@pytest.mark.parametrize("codigo", list(CONTENIDOS))
def test_respuesta_banco_correcta(codigo):
    valor = str(CONTENIDOS[codigo]["respuesta"])
    assert "Resultado: correcto" in evaluar_respuesta_logica(codigo, valor)


@pytest.mark.parametrize("codigo, respuesta", [
    ("5B", "4/6"),
    ("5B", "2 / 3"),
    ("6B", "50,0"),
    ("6B", "50.0"),
    ("8B", "x=5"),
])
def test_respuestas_equivalentes(codigo, respuesta):
    assert "Resultado: correcto" in evaluar_respuesta_logica(codigo, respuesta)


def test_respuesta_erronea():
    assert "Resultado: incorrecto" in evaluar_respuesta_logica("5B", "1/3")


@pytest.mark.parametrize("respuesta", ["dos tercios", "1/0", "", "__import__('os')"])
def test_respuestas_invalidas_no_se_califican(respuesta):
    assert "Error:" in evaluar_respuesta_logica("5B", respuesta)

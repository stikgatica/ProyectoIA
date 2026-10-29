import json
import pytest
from src.sigra.motor import SesionDiagnostico, cargar_banco
from pathlib import Path

RUTA = Path(__file__).resolve().parents[1] / "data" / "sigra" / "banco_oa_ejemplo.json"


def test_falla_fracciones_y_explora_prerrequisitos():
    banco = cargar_banco(RUTA)
    sesion = SesionDiagnostico(banco, ["SIGRA-MAT-5-FRACC-EQ"])
    assert sesion.siguiente_pregunta()["id_oa"] == "SIGRA-MAT-5-FRACC-EQ"
    assert "correcta" not in sesion.siguiente_pregunta()
    assert sesion.responder(0)["acierto"] is False
    assert sesion.siguiente_pregunta()["id_oa"] == "SIGRA-MAT-4-DIV"
    sesion.responder(0)  # División incorrecta; tablas ya están en cola.
    assert sesion.siguiente_pregunta()["id_oa"] == "SIGRA-MAT-3-TABLAS"
    sesion.responder(1)  # Tablas correctas.
    assert sesion.siguiente_pregunta() is None
    assert [x["id_oa"] for x in sesion.ruta_refuerzo()] == [
        "SIGRA-MAT-4-DIV", "SIGRA-MAT-5-FRACC-EQ"
    ]


def test_respuesta_correcta_termina_si_es_unico_objetivo():
    sesion = SesionDiagnostico(cargar_banco(RUTA), ["SIGRA-MAT-5-FRACC-EQ"])
    sesion.responder(1)
    assert sesion.siguiente_pregunta() is None
    assert sesion.ruta_refuerzo() == []


def test_no_permite_alternativas_invalidas():
    sesion = SesionDiagnostico(cargar_banco(RUTA), ["SIGRA-MAT-5-FRACC-EQ"])
    with pytest.raises(ValueError):
        sesion.responder(4)
    assert len(sesion.pendientes) == 1


def test_rechaza_prerrequisitos_ciclicos(tmp_path):
    registros = [
        {"id": "A", "pregunta": "A?", "curso": 4, "habilidad": "A", "alternativas": ["1","2","3","4"], "correcta": 0, "prerrequisitos": ["B"]},
        {"id": "B", "pregunta": "B?", "curso": 3, "habilidad": "B", "alternativas": ["1","2","3","4"], "correcta": 0, "prerrequisitos": ["A"]},
    ]
    archivo = tmp_path / "ciclos.json"
    archivo.write_text(json.dumps(registros), encoding="utf-8")
    with pytest.raises(ValueError, match="Ciclo"):
        cargar_banco(archivo)

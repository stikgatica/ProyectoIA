"""Motor adaptativo de demostración para SIGRA.

Las decisiones de acierto/error son deterministas, independientes de la IA.
Los identificadores OA del banco de ejemplo son internos, NO son códigos MINEDUC.
"""
from __future__ import annotations
import json
from pathlib import Path


def cargar_banco(ruta: str | Path) -> dict[str, dict]:
    """Carga preguntas y valida referencias a prerrequisitos y ciclos."""
    with Path(ruta).open(encoding="utf-8") as archivo:
        registros = json.load(archivo)
    if not isinstance(registros, list) or not registros:
        raise ValueError("El banco debe ser una lista no vacía")
    banco = {}
    for oa in registros:
        clave = oa.get("id")
        if not isinstance(clave, str) or not clave or clave in banco:
            raise ValueError(f"Identificador de OA inválido o duplicado: {clave}")
        if not (isinstance(oa.get("alternativas"), list) and len(oa["alternativas"]) == 4):
            raise ValueError(f"El OA {clave} debe tener cuatro alternativas")
        if type(oa.get("correcta")) is not int or not 0 <= oa["correcta"] < 4:
            raise ValueError(f"Alternativa correcta fuera de rango en {clave}")
        if not isinstance(oa.get("prerrequisitos"), list):
            raise ValueError(f"Prerrequisitos inválidos en {clave}")
        if not isinstance(oa.get("pregunta"), str) or not oa["pregunta"].strip():
            raise ValueError(f"Falta la pregunta de {clave}")
        banco[clave] = oa

    for clave, oa in banco.items():
        for pre in oa["prerrequisitos"]:
            if pre not in banco:
                raise ValueError(f"El OA {clave} referencia prerrequisito inexistente: {pre}")

    # Detecta ciclos en el grafo de requisitos antes de iniciar diagnósticos.
    visitados, abiertos = set(), set()
    def visitar(clave):
        if clave in abiertos:
            raise ValueError(f"Ciclo detectado en prerrequisitos de {clave}")
        if clave in visitados:
            return
        abiertos.add(clave)
        for previo in banco[clave]["prerrequisitos"]:
            visitar(previo)
        abiertos.remove(clave)
        visitados.add(clave)

    for clave in banco:
        visitar(clave)
    return banco


class SesionDiagnostico:
    """Selecciona una pregunta objetivo y explora prerrequisitos ante errores."""

    def __init__(self, banco: dict[str, dict], objetivos: list[str]):
        if not objetivos or any(obj not in banco for obj in objetivos):
            raise ValueError("Se necesitan objetivos existentes en el banco")
        self.banco = banco
        self.pendientes = list(dict.fromkeys(objetivos))
        self.resultados: dict[str, bool] = {}
        self.historial: list[dict] = []

    def siguiente_pregunta(self) -> dict | None:
        if not self.pendientes:
            return None
        oa = self.banco[self.pendientes[0]]
        # No enviamos `correcta` al usuario ni a la futura interfaz.
        return {
            "id_oa": oa["id"],
            "curso": oa["curso"],
            "pregunta": oa["pregunta"],
            "alternativas": oa["alternativas"],
        }

    def responder(self, alternativa: int) -> dict:
        if not self.pendientes:
            raise ValueError("El diagnóstico ya terminó")
        if type(alternativa) is not int or not 0 <= alternativa < 4:
            raise ValueError("La alternativa debe ser un entero entre 0 y 3")
        clave = self.pendientes.pop(0)
        oa = self.banco[clave]
        acierto = alternativa == oa["correcta"]
        self.resultados[clave] = acierto
        evento = {"id_oa": clave, "alternativa": alternativa, "acierto": acierto}
        self.historial.append(evento)
        if not acierto:
            # Solo programamos prerrequisitos no evaluados ni pendientes.
            nuevos = [pre for pre in oa["prerrequisitos"]
                      if pre not in self.resultados and pre not in self.pendientes]
            self.pendientes = nuevos + self.pendientes
        return evento

    def ruta_refuerzo(self) -> list[dict]:
        """Entrega brechas observadas, con prerrequisitos primero."""
        brechas = {id_oa for id_oa, acierto in self.resultados.items() if not acierto}
        orden, vistos = [], set()
        def ordenar(clave):
            if clave in vistos:
                return
            vistos.add(clave)
            for pre in self.banco[clave]["prerrequisitos"]:
                if pre in brechas:
                    ordenar(pre)
            if clave in brechas:
                orden.append({"id_oa": clave, "habilidad": self.banco[clave]["habilidad"]})
        for clave in sorted(brechas):
            ordenar(clave)
        return orden

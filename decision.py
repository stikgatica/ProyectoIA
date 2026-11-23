"""Evaluación de estrategias de personalización para SIGRA Matemática.

Ejecutar desde la raíz del repositorio: python decision.py
La ejecución no necesita bibliotecas externas ni acceso a servicios.
"""
from pathlib import Path


RESPUESTAS = {
    "informacion_cambia_seguido": False,
    "problema_de_formato_o_tono": False,
    "dataset_grande_y_de_calidad": False,
    "presupuesto_limitado_o_iterar_rapido": True,
    "necesita_multiples_variantes": False,
}

EVIDENCIAS = {
    "informacion_cambia_seguido": (
        "No he reunido un historial de actualizaciones que demuestre cambios "
        "mensuales en las fuentes curriculares durante los últimos tres meses. "
        "Por ello, no considero acreditado este criterio."
    ),
    "problema_de_formato_o_tono": (
        "Dispongo de 20 respuestas evaluadas en SIGRA, pero la evaluación "
        "registrada se concentró en coincidencia textual y corrección matemática. "
        "No existe una revisión de 20 casos con criterios fijos de tono y formato "
        "que permita demostrar al menos 3 incumplimientos."
    ),
    "dataset_grande_y_de_calidad": (
        "El laboratorio de tuning tiene 8 ejemplos etiquetados de errores de una API, "
        "no 200 ejemplos específicos de SIGRA. Tampoco existe una revisión aleatoria "
        "documentada de 20 etiquetas de un conjunto de ese tamaño."
    ),
    "presupuesto_limitado_o_iterar_rapido": (
        "Para la próxima etapa del prototipo establezco como requisito revisar "
        "el efecto de un cambio en menos de un día, sin requerir un nuevo entrenamiento."
    ),
    "necesita_multiples_variantes": (
        "El diseño contempla una misma arquitectura de SIGRA para los 8 niveles, "
        "con actividades y fuentes diferenciadas por curso, no modelos separados."
    ),
}

PROBLEMA = (
    "SIGRA Matemática busca orientar el aprendizaje de estudiantes de 1° a 8° "
    "básico. Para entregar recomendaciones fundamentadas necesita consultar "
    "Objetivos de Aprendizaje y relaciones de prerrequisitos verificadas. "
    "Actualmente su banco curricular es demostrativo y no constituye un "
    "corpus oficial completo para los ocho niveles."
)

JUSTIFICACION = (
    "Elijo **RAG**, porque el problema prioritario es disponer de fuentes "
    "curriculares verificadas y recuperarlas al responder, no una falla de "
    "formato demostrada. Con RAG puedo actualizar el corpus y sus referencias "
    "sin volver a entrenar el modelo cada vez. Mi proyecto ya tiene componentes "
    "de embeddings, Chroma, recuperación, citas y medición de tiempos y tokens.\n\n"
    "En cuanto a los costos, RAG requiere tiempo de recopilación, organización "
    "y validación de las fuentes; utiliza cómputo para indexar y consultar, "
    "pero evita iniciar un entrenamiento por cada actualización. "
    "El fine-tuning completo supondría una inversión más alta en ejemplos "
    "etiquetados, entrenamiento y pruebas. PEFT reduce ese costo, pero aún no "
    "tengo evidencias suficientes de un problema de comportamiento que lo justifique.\n\n"
    "La comparación no implica que RAG garantice respuestas correctas: la "
    "evaluación matemática y la validación de prerrequisitos deben mantenerse "
    "fuera de decisiones autónomas del modelo, con supervisión docente."
)

REQUISITOS = (
    "Actualmente tengo un banco demostrativo con **3 entradas internas de OA** "
    "(3°, 4° y 5° básico). Son identificadores de ejemplo, no OA oficiales "
    "validados. Para una primera etapa de cobertura de 1° a 8° básico "
    "defino la meta de **8 conjuntos documentales oficiales, uno por nivel**. "
    "En el repositorio no hay ocho conjuntos curriculares verificados e "
    "indexados, por lo que los **8 conjuntos de esa meta quedan pendientes**. "
    "Tener información para 3 cursos en el banco de ejemplo no equivale a "
    "contar con los documentos curriculares completos de esos cursos.\n\n"
    "El trabajo previsto consiste en obtener esas 8 fuentes, registrar curso, "
    "eje, OA, versión y origen; validar las relaciones de prerrequisitos con "
    "docentes; dividir e indexar los textos; y comprobar la recuperación y "
    "las citas. Como primera prueba de calidad usaré **20 preguntas matemáticas** "
    "de los ocho niveles, tomando como referencia el conjunto de evaluación "
    "ya registrado en el proyecto y adaptándolo para evaluar recuperación "
    "curricular. La corrección de las respuestas seguirá un control matemático "
    "independiente del texto generado.\n\n"
    "El flujo RAG utilizado en el Bloque 28 recuperó fragmentos de un manual "
    "técnico de demostración; no representa todavía una base curricular de "
    "SIGRA. También debo medir latencia, tokens y costo estimado sobre el "
    "nuevo corpus antes de utilizarlo en la práctica pedagógica."
)


def recomendar_estrategia(respuestas):
    puntos = {"RAG": 0, "Fine-tuning completo": 0, "PEFT": 0}
    if respuestas["informacion_cambia_seguido"]:
        puntos["RAG"] += 3
    if respuestas["problema_de_formato_o_tono"]:
        puntos["PEFT"] += 2
        puntos["Fine-tuning completo"] += 1
    if respuestas["dataset_grande_y_de_calidad"]:
        puntos["Fine-tuning completo"] += 2
        puntos["PEFT"] += 1
    if respuestas["presupuesto_limitado_o_iterar_rapido"]:
        puntos["RAG"] += 2
        puntos["PEFT"] += 1
    if respuestas["necesita_multiples_variantes"]:
        puntos["PEFT"] += 2

    maximo = max(puntos.values())
    ganadoras = [tecnica for tecnica, puntuacion in puntos.items() if puntuacion == maximo]
    return puntos, ganadoras


def generar_esqueleto_decision(problema, puntos, ganadoras):
    """Construye las cuatro secciones en el orden pedido en la actividad."""
    lineas = [
        "# Decisión de personalización: SIGRA Matemática",
        "",
        "## 1. El problema",
        problema,
        "",
        "## 2. Resultado del método de decisión",
        "Apliqué los cinco criterios al estado actual de ProyectoIA:",
        "",
    ]
    for clave, valor in RESPUESTAS.items():
        lineas.append(f"- **{clave}: {valor}.** {EVIDENCIAS[clave]}")
    lineas.extend(["", "**Puntajes:**"])
    for tecnica, puntuacion in sorted(puntos.items(), key=lambda x: -x[1]):
        unidad = "punto" if puntuacion == 1 else "puntos"
        lineas.append(f"- {tecnica}: {puntuacion} {unidad}.")
    lineas.append("")
    if len(ganadoras) > 1:
        lineas.append(f"**Empate:** {', '.join(ganadoras)}. La elección requiere justificación adicional.")
    else:
        lineas.append(f"**Resultado:** {ganadoras[0]} obtiene el mayor puntaje, sin empate.")
    lineas.extend(["", "## 3. Técnica elegida y por qué", "", "## 4. Qué necesitarías para ejecutarla", ""])
    return "\n".join(lineas)


def completar_documento(esqueleto, puntos_originales):
    texto = esqueleto.replace(
        "## 3. Técnica elegida y por qué\n\n## 4. Qué necesitarías para ejecutarla",
        "## 3. Técnica elegida y por qué\n" + JUSTIFICACION +
        "\n\n## 4. Qué necesitarías para ejecutarla\n" + REQUISITOS,
    )
    variante = RESPUESTAS.copy()
    variante["problema_de_formato_o_tono"] = not variante["problema_de_formato_o_tono"]
    otros_puntos, otras_ganadoras = recomendar_estrategia(variante)
    sensibilidad = (
        "\n\n**Comprobación de sensibilidad.** Cambié solo la respuesta "
        "de 'problema_de_formato_o_tono' de False a True, como hipótesis; "
        "esto no representa una medición adicional. "
        f"La nueva puntuación sería RAG {otros_puntos['RAG']}, "
        f"PEFT {otros_puntos['PEFT']} y fine-tuning completo "
        f"{otros_puntos['Fine-tuning completo']}. "
        f"La primera candidata pasaría a ser {', '.join(otras_ganadoras)}. "
        "Si una revisión futura de 20 respuestas detecta 3 o más fallas de "
        "formato o tono, será necesario reevaluar la estrategia."
    )
    texto = texto.replace("\n\n## 3. Técnica elegida y por qué", sensibilidad + "\n\n## 3. Técnica elegida y por qué")
    return texto


if __name__ == "__main__":
    if any(valor is None for valor in RESPUESTAS.values()):
        raise SystemExit("Debes completar las cinco respuestas con True o False.")
    puntos, ganadoras = recomendar_estrategia(RESPUESTAS)
    print("Puntuación:", puntos)
    print("Candidatas:", ", ".join(ganadoras))

    cambio = RESPUESTAS.copy()
    cambio["problema_de_formato_o_tono"] = not cambio["problema_de_formato_o_tono"]
    puntos_cambio, ganadoras_cambio = recomendar_estrategia(cambio)
    print("Análisis de sensibilidad:", puntos_cambio)
    print("Candidatas con el criterio cambiado:", ", ".join(ganadoras_cambio))

    documento = completar_documento(generar_esqueleto_decision(PROBLEMA, puntos, ganadoras), puntos)
    destino = Path("decision_personalizacion.md")
    if destino.exists():
        print(f"{destino} ya existe: no se ha sobrescrito.")
    else:
        destino.write_text(documento, encoding="utf-8")
        print(f"Documento creado: {destino}")

# Decisión de personalización: SIGRA Matemática

## 1. El problema
SIGRA Matemática busca orientar el aprendizaje de estudiantes de 1° a 8° básico. Para entregar recomendaciones fundamentadas necesita consultar Objetivos de Aprendizaje y relaciones de prerrequisitos verificadas. Actualmente su banco curricular es demostrativo y no constituye un corpus oficial completo para los ocho niveles.

## 2. Resultado del método de decisión
Apliqué los cinco criterios al estado actual de ProyectoIA:

- **informacion_cambia_seguido: False.** No he reunido un historial de actualizaciones que demuestre cambios mensuales en las fuentes curriculares durante los últimos tres meses. Por ello, no considero acreditado este criterio.
- **problema_de_formato_o_tono: False.** Dispongo de 20 respuestas evaluadas en SIGRA, pero la evaluación registrada se concentró en coincidencia textual y corrección matemática. No existe una revisión de 20 casos con criterios fijos de tono y formato que permita demostrar al menos 3 incumplimientos.
- **dataset_grande_y_de_calidad: False.** El laboratorio de tuning tiene 8 ejemplos etiquetados de errores de una API, no 200 ejemplos específicos de SIGRA. Tampoco existe una revisión aleatoria documentada de 20 etiquetas de un conjunto de ese tamaño.
- **presupuesto_limitado_o_iterar_rapido: True.** Para la próxima etapa del prototipo establezco como requisito revisar el efecto de un cambio en menos de un día, sin requerir un nuevo entrenamiento.
- **necesita_multiples_variantes: False.** El diseño contempla una misma arquitectura de SIGRA para los 8 niveles, con actividades y fuentes diferenciadas por curso, no modelos separados.

**Puntajes:**
- RAG: 2 puntos.
- PEFT: 1 punto.
- Fine-tuning completo: 0 puntos.

**Resultado:** RAG obtiene el mayor puntaje, sin empate.

**Comprobación de sensibilidad.** Cambié solo la respuesta de 'problema_de_formato_o_tono' de False a True, como hipótesis; esto no representa una medición adicional. La nueva puntuación sería RAG 2, PEFT 3 y fine-tuning completo 1. La primera candidata pasaría a ser PEFT. Si una revisión futura de 20 respuestas detecta 3 o más fallas de formato o tono, será necesario reevaluar la estrategia.

## 3. Técnica elegida y por qué
Elijo **RAG**, porque el problema prioritario es disponer de fuentes curriculares verificadas y recuperarlas al responder, no una falla de formato demostrada. Con RAG puedo actualizar el corpus y sus referencias sin volver a entrenar el modelo cada vez. Mi proyecto ya tiene componentes de embeddings, Chroma, recuperación, citas y medición de tiempos y tokens.

En cuanto a los costos, RAG requiere tiempo de recopilación, organización y validación de las fuentes; utiliza cómputo para indexar y consultar, pero evita iniciar un entrenamiento por cada actualización. El fine-tuning completo supondría una inversión más alta en ejemplos etiquetados, entrenamiento y pruebas. PEFT reduce ese costo, pero aún no tengo evidencias suficientes de un problema de comportamiento que lo justifique.

La comparación no implica que RAG garantice respuestas correctas: la evaluación matemática y la validación de prerrequisitos deben mantenerse fuera de decisiones autónomas del modelo, con supervisión docente.

## 4. Qué necesitarías para ejecutarla
Actualmente tengo un banco demostrativo con **3 entradas internas de OA** (3°, 4° y 5° básico). Son identificadores de ejemplo, no OA oficiales validados. Para una primera etapa de cobertura de 1° a 8° básico defino la meta de **8 conjuntos documentales oficiales, uno por nivel**. En el repositorio no hay ocho conjuntos curriculares verificados e indexados, por lo que los **8 conjuntos de esa meta quedan pendientes**. Tener información para 3 cursos en el banco de ejemplo no equivale a contar con los documentos curriculares completos de esos cursos.

El trabajo previsto consiste en obtener esas 8 fuentes, registrar curso, eje, OA, versión y origen; validar las relaciones de prerrequisitos con docentes; dividir e indexar los textos; y comprobar la recuperación y las citas. Como primera prueba de calidad usaré **20 preguntas matemáticas** de los ocho niveles, tomando como referencia el conjunto de evaluación ya registrado en el proyecto y adaptándolo para evaluar recuperación curricular. La corrección de las respuestas seguirá un control matemático independiente del texto generado.

El flujo RAG utilizado en el Bloque 28 recuperó fragmentos de un manual técnico de demostración; no representa todavía una base curricular de SIGRA. También debo medir latencia, tokens y costo estimado sobre el nuevo corpus antes de utilizarlo en la práctica pedagógica.


# Limitaciones de las métricas de evaluación en SIGRA

## 1. Objetivo de la evaluación

Evaluar las respuestas generadas por un modelo de lenguaje
para preguntas de Matemática de 1° a 8° básico, utilizando
métricas de precisión, cobertura y F1 basadas en coincidencias
textuales.

Se analizaron 20 preguntas con respuestas de referencia
y respuestas generadas por inteligencia artificial.

Posteriormente, se realizó una revisión manual de 10 casos:
5 con los valores F1 más bajos y 5 con los más altos.

## 2. Resultados cuantitativos

Los promedios obtenidos fueron:

- Precisión promedio: 0.3135 (31.35%)
- Cobertura promedio: 0.5528 (55.28%)
- F1 promedio: 0.3917 (39.17%)

Estos resultados representan coincidencias entre tokens
de las respuestas generadas y las referencias.

No representan directamente el porcentaje de respuestas
matemáticamente correctas.

## 3. Resultados de la revisión manual

Se revisaron 10 respuestas, considerando:

- Exactitud matemática.
- Completitud de la respuesta.
- Presencia de contradicciones.
- Coherencia del procedimiento matemático.

Resultados:

- 10 respuestas matemáticamente correctas.
- 10 respuestas completas.
- 0 respuestas con contradicciones detectadas.

Un ejemplo significativo corresponde a la pregunta
"¿Cuánto es 6 multiplicado por 4?".

El modelo respondió correctamente 24 y explicó
la multiplicación mediante una suma reiterada.

Sin embargo, obtuvo un F1 de solo 0.1429.

Esto demuestra que una respuesta correcta puede
recibir una puntuación textual baja.

Otro ejemplo corresponde a las fracciones equivalentes:
la respuesta 2/4 = 1/2 obtuvo un F1 de 0.5806,
aunque tanto esta respuesta como la anterior
eran matemáticamente correctas.

La revisión manual corresponde a una muestra seleccionada
por valores extremos de F1, por lo que no permite
generalizar automáticamente sus resultados a todas
las respuestas del sistema.

## 4. Limitaciones y recomendaciones

### Limitaciones identificadas

1. La comparación textual penaliza respuestas correctas
   expresadas con palabras diferentes.

2. No identifica necesariamente equivalencias matemáticas,
   como "25%" y "25 por ciento".

3. Puede penalizar explicaciones adicionales correctas
   que no aparecen en la referencia.

4. No verifica directamente el resultado de una operación.

5. No detecta necesariamente errores conceptuales,
   contradicciones o procedimientos incorrectos.

6. No evalúa si el lenguaje es apropiado para el nivel
   educativo del estudiante.

7. Un F1 elevado tampoco garantiza que una respuesta
   sea matemáticamente correcta.

### Recomendaciones para SIGRA

- Mantener precisión, cobertura y F1 como indicadores
  complementarios de coincidencia textual.
- Incorporar validación matemática de resultados.
- Normalizar expresiones equivalentes, unidades y símbolos.
- Evaluar por separado la exactitud matemática.
- Evaluar la pertinencia pedagógica según el curso.
- Utilizar revisión humana para validar el sistema.
- Comparar futuros métodos de evaluación con esta
  línea base de 20 casos.

### Conclusión

Las métricas de precisión, cobertura y F1 permiten
estudiar la coincidencia textual entre respuestas,
pero no son suficientes para medir la calidad
matemática y pedagógica de SIGRA.

La revisión manual demostró que respuestas correctas
pueden obtener valores F1 reducidos.

Por lo tanto, SIGRA debería combinar métricas textuales,
validación matemática y criterios pedagógicos antes de
utilizar las evaluaciones para tomar decisiones sobre
el aprendizaje de los estudiantes.

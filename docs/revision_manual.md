# Revisión manual de respuestas de SIGRA

Se seleccionaron cinco casos con F1 bajo y cinco con F1 alto.

El F1 basado en coincidencias textuales no equivale a exactitud matemática.

| Grupo | Consulta | F1 | Exactitud | Completitud | Contradicciones |
|---|---|---:|---|---|---|
| F1 bajo | 3° básico: ¿Cuánto es 6 multiplicado por 4? | 0.1429 | Sí | Sí | No |
| F1 bajo | 5° básico: ¿Cuánto es un tercio más un tercio? | 0.2400 | Sí | Sí | No |
| F1 bajo | 2° básico: ¿Cuánto es 14 menos 6? | 0.2759 | Sí | Sí | No |
| F1 bajo | 2° básico: ¿Cuánto es 3 más 3 más 3? | 0.2941 | Sí | Sí | No |
| F1 bajo | 8° básico: ¿Dónde queda el punto (2, 3) al trasladarlo 4 unidades a la derecha? | 0.2963 | Sí | Sí | No |
| F1 alto | 4° básico: ¿Cuál es una fracción equivalente a un medio? | 0.5806 | Sí | Sí | No |
| F1 alto | 7° básico: ¿Cuál es el área de un paralelogramo con base 7 cm y altura 4 cm? | 0.5294 | Sí | Sí | No |
| F1 alto | 4° básico: ¿Cuál es el perímetro de un rectángulo de lados 5 cm y 3 cm? | 0.5294 | Sí | Sí | No |
| F1 alto | 6° básico: ¿Qué operación se realiza primero en 6 + 2 × 3? | 0.5161 | Sí | Sí | No |
| F1 alto | 6° básico: ¿Cuánto es el 25 por ciento de 80? | 0.5143 | Sí | Sí | No |

## Observaciones por caso

### 1. 3° básico: ¿Cuánto es 6 multiplicado por 4? (F1 bajo)

- Referencia: 6 multiplicado por 4 es igual a 24.
- Respuesta: El resultado es 24, obtenido al sumar el número seis cuatro veces (6+6+6+6) para hallar el producto de la multiplicación.
- F1: 0.1429
- Observación: La respuesta es matemáticamente correcta y explica la multiplicación mediante una suma reiterada. Sin embargo, presenta un F1 bajo porque utiliza palabras distintas de la referencia. Esto demuestra que la coincidencia textual no siempre refleja la calidad matemática de una respuesta.

### 2. 5° básico: ¿Cuánto es un tercio más un tercio? (F1 bajo)

- Referencia: Un tercio más un tercio es igual a dos tercios.
- Respuesta: El resultado es dos tercios, obtenido al sumar los numeradores y mantener el denominador común.
- F1: 0.2400
- Observación: La respuesta es matemáticamente correcta y explica adecuadamente el procedimiento de suma de fracciones con igual denominador. El F1 bajo (0,24) se debe a diferencias en la redacción respecto de la referencia y no a errores matemáticos. Esto evidencia una limitación de la métrica de coincidencia textual.

### 3. 2° básico: ¿Cuánto es 14 menos 6? (F1 bajo)

- Referencia: 14 menos 6 es igual a 8.
- Respuesta: El resultado es 8, obtenido al restar 4 de 14 para llegar a la decena y luego sustraer las 2 unidades restantes.
- F1: 0.2759
- Observación: La respuesta es matemáticamente correcta y presenta una estrategia de cálculo mediante descomposición para llegar a la decena. Aunque el F1 es bajo (0,2759), la explicación es válida y aporta valor pedagógico. Esto demuestra que la métrica de coincidencia textual no reconoce adecuadamente procedimientos matemáticos equivalentes.

### 4. 2° básico: ¿Cuánto es 3 más 3 más 3? (F1 bajo)

- Referencia: La suma es 9 y representa tres grupos de 3.
- Respuesta: El resultado es 9, obtenido al sumar tres veces el número tres, lo cual equivale a la operación matemática de multiplicar tres por tres.
- F1: 0.2941
- Observación: La respuesta es matemáticamente correcta y reconoce la relación entre la suma reiterada y la multiplicación. Sin embargo, utiliza un lenguaje más complejo de lo necesario para estudiantes de 2° básico. El F1 bajo (0,2941) se explica principalmente por diferencias de redacción, lo que demuestra que la métrica no evalúa adecuadamente la comprensión matemática ni la pertinencia pedagógica.

### 5. 8° básico: ¿Dónde queda el punto (2, 3) al trasladarlo 4 unidades a la derecha? (F1 bajo)

- Referencia: El punto se traslada hasta las coordenadas (6, 3).
- Respuesta: El punto resultante es (6, 3), obtenido al sumar 4 unidades a la abscisa del par ordenado inicial.
- F1: 0.2963
- Observación: La respuesta es matemáticamente correcta y explica adecuadamente el procedimiento de traslación horizontal en el plano cartesiano. Utiliza el concepto de abscisa de manera pertinente para 8° básico. El F1 bajo (0,2963) se debe principalmente a diferencias de vocabulario respecto de la referencia, evidenciando que la métrica no reconoce completamente respuestas matemáticamente equivalentes.

### 6. 4° básico: ¿Cuál es una fracción equivalente a un medio? (F1 alto)

- Referencia: Dos cuartos es una fracción equivalente a un medio.
- Respuesta: Dos cuartos es una fracción equivalente a un medio, obtenida al multiplicar tanto el numerador como el denominador por el número dos.
- F1: 0.5806
- Observación: La respuesta es matemáticamente correcta, completa y explica adecuadamente el procedimiento de amplificación para obtener fracciones equivalentes. El F1 de 0,5806 refleja una mayor coincidencia textual con la referencia. Sin embargo, la métrica no evalúa directamente la calidad de la explicación adicional ni su pertinencia pedagógica.

### 7. 7° básico: ¿Cuál es el área de un paralelogramo con base 7 cm y altura 4 cm? (F1 alto)

- Referencia: El área es 28 centímetros cuadrados porque se multiplica la base por la altura.
- Respuesta: El área es 28 cm², resultado de multiplicar la medida de la base por la altura (7 cm × 4 cm).
- F1: 0.5294
- Observación: La respuesta es matemáticamente correcta y completa, ya que aplica adecuadamente la fórmula del área del paralelogramo y expresa el resultado en centímetros cuadrados. El F1 de 0,5294 refleja una coincidencia textual moderada con la referencia. Sin embargo, la métrica no distingue entre las expresiones equivalentes «cm²» y «centímetros cuadrados», lo que evidencia una limitación de la comparación léxica.

### 8. 4° básico: ¿Cuál es el perímetro de un rectángulo de lados 5 cm y 3 cm? (F1 alto)

- Referencia: El perímetro es 16 centímetros porque se suman las longitudes de sus cuatro lados.
- Respuesta: El perímetro es 16 cm, calculado mediante la suma de las medidas de sus cuatro lados: 5 + 5 + 3 + 3.
- F1: 0.5294
- Observación: La respuesta es matemáticamente correcta y completa, ya que calcula adecuadamente el perímetro sumando las longitudes de los cuatro lados del rectángulo. El F1 de 0,5294 refleja una coincidencia textual moderada con la referencia. Sin embargo, la métrica no reconoce plenamente la equivalencia entre «cm» y «centímetros», ni valora directamente la explicación numérica del procedimiento.

### 9. 6° básico: ¿Qué operación se realiza primero en 6 + 2 × 3? (F1 alto)

- Referencia: Primero se multiplica 2 por 3 y después se suma 6, obteniendo 12.
- Respuesta: Se realiza primero la multiplicación $2 \times 3 = 6$ por prioridad de operaciones, obteniendo 12 como resultado final.
- F1: 0.5161
- Observación: La respuesta es matemáticamente correcta y completa, ya que aplica adecuadamente la prioridad de operaciones, realizando primero la multiplicación y obteniendo el resultado final de 12. El F1 de 0,5161 refleja una coincidencia textual moderada con la referencia, pero no evalúa directamente el razonamiento matemático ni la correcta aplicación de la jerarquía de operaciones.

### 10. 6° básico: ¿Cuánto es el 25 por ciento de 80? (F1 alto)

- Referencia: El 25 por ciento de 80 es 20 porque representa su cuarta parte.
- Respuesta: El resultado es 20, calculado al dividir 80 por 4, ya que el 25% equivale a la cuarta parte de una cantidad.
- F1: 0.5143
- Observación: La respuesta es matemáticamente correcta y completa, ya que identifica que el 25% equivale a la cuarta parte de una cantidad y aplica correctamente la división para obtener 20. El F1 de 0,5143 refleja una coincidencia textual moderada con la referencia. Sin embargo, la métrica no reconoce plenamente la equivalencia entre «25%» y «25 por ciento», ni evalúa directamente la validez del procedimiento matemático.

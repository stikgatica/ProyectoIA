# Límites de autonomía: SIGRA

## 1. Herramientas y nivel de riesgo

El agente SIGRA dispone de dos herramientas
para acompañar el aprendizaje matemático.

- consultar_contenido: Riesgo bajo.
  Consulta ejercicios y contenidos matemáticos
  sin modificar información.

- evaluar_respuesta: Riesgo bajo.
  Compara la respuesta del estudiante con
  una solución registrada y entrega
  retroalimentación pedagógica.

Ninguna de estas herramientas modifica
calificaciones ni registros escolares.

## 2. Herramientas que requieren aprobación humana

El agente SIGRA utiliza dos herramientas
de riesgo bajo que no requieren aprobación
humana antes de cada ejecución.

- consultar_contenido:
  No requiere aprobación porque solamente
  consulta información matemática y no
  modifica datos.

- evaluar_respuesta:
  No requiere aprobación para ejercicios
  de práctica, porque compara respuestas
  y entrega retroalimentación sin registrar
  calificaciones oficiales.

Sin embargo, las recomendaciones del agente
deben ser supervisadas por un docente antes
de utilizarlas para decisiones pedagógicas
formales.

SIGRA no está autorizado para modificar
calificaciones, cerrar procesos evaluativos
ni tomar decisiones de promoción escolar.

Si en el futuro se incorporan herramientas
que modifiquen registros escolares, estas
deberán solicitar aprobación humana
antes de ejecutar cualquier cambio.

## 3. Revisión de trazas

Las trazas de SIGRA permiten revisar las
herramientas utilizadas por el agente,
los argumentos enviados, las observaciones
obtenidas y las respuestas finales.

El agente registra cada interacción en el
archivo trazas_agente.jsonl.

Frecuencia de revisión:
Inicialmente revisaré todas las interacciones
de prueba. Posteriormente, realizaré revisiones
semanales o cada 20 interacciones.

Patrones sospechosos:
- Uso de herramientas con argumentos incorrectos.
- Consultas con códigos de contenido inexistentes.
- Llamadas innecesarias o repetidas.
- Respuestas que contradigan los resultados.
- Recomendaciones pedagógicas sin evidencia.

Resultados de las pruebas realizadas:

Se ejecutaron tres interacciones, generando
tres registros en trazas_agente.jsonl.

1. Consulta de fracciones:
   Se llamó a consultar_contenido, pero el
   argumento enviado no coincidió con
   los formatos admitidos.

2. Evaluación de respuesta:
   Se llamó a evaluar_respuesta, pero se
   utilizó un código de contenido inexistente.

3. Saludo:
   El agente respondió correctamente sin
   utilizar herramientas.

Estas pruebas demostraron que el registro
de trazas funciona, pero también permitieron
identificar errores en la selección de argumentos
que requieren ajustes posteriores.


## 4. Qué hacer ante un comportamiento inesperado

Ante un comportamiento inesperado de SIGRA,
aplicaré el siguiente procedimiento:

1. Detener temporalmente el agente para evitar
   que continúe entregando respuestas incorrectas.

2. Revisar el archivo trazas_agente.jsonl
   para identificar la herramienta utilizada,
   los argumentos enviados y la respuesta obtenida.

3. Identificar el origen del problema.
   Si una herramienta recibe argumentos incorrectos,
   revisaré su descripción, validaciones y las
   instrucciones entregadas al modelo.

4. Corregir el problema y ejecutar nuevamente
   las pruebas, comprobando que las herramientas
   reciban los argumentos esperados.

5. Si el problema persiste, deshabilitaré
   temporalmente la herramienta afectada
   hasta encontrar una solución.

6. Si una recomendación pudiera afectar
   decisiones pedagógicas, solicitaré
   revisión docente antes de utilizarla.

Ejemplo real identificado durante las pruebas:

SIGRA utilizó consultar_contenido con el argumento
"fracciones de 5 básico", que no fue reconocido.

También utilizó evaluar_respuesta con el código
"5B-fracciones-suma", inexistente en el banco.

En ambos casos, las trazas permitieron detectar
el problema sin modificar registros escolares.

Como medida correctiva, corresponde mejorar
las instrucciones del agente y validar los
códigos utilizados por sus herramientas.


## 5. Validación final del agente SIGRA — CORE Bloque 23

Se corrigieron los problemas de reconocimiento de consultas matemáticas y de evaluación de respuestas equivalentes.

Pruebas automáticas:
- Motor adaptativo: 4 pruebas aprobadas.
- Herramientas matemáticas: 27 pruebas aprobadas.
- Total: 31 pruebas aprobadas.

Pruebas de integración con Gemini y memoria conversacional:
1. Consulta de fracciones de 5° básico: ejecución correcta de consultar_contenido, código 5B.
2. Respuesta 4/6: ejecución correcta de evaluar_respuesta, recuperando el código 5B desde el historial y reconociendo la equivalencia con 2/3.
3. Saludo: respuesta directa, sin ejecutar herramientas innecesarias.

Se verificaron tres registros en trazas_agente.jsonl con timestamp, session_id, entrada, acciones y respuesta_final.

Conclusión: las pruebas realizadas confirman el funcionamiento de las herramientas, la memoria temporal y la trazabilidad en los escenarios evaluados. SIGRA no modifica registros escolares ni realiza diagnósticos oficiales. Las decisiones pedagógicas formales requieren supervisión docente.

Limitaciones pendientes: la memoria se pierde al cerrar el proceso y LangChain advierte que sus componentes actuales de memoria están obsoletos. Se recomienda migrar a un mecanismo de persistencia compatible en una actualización posterior.

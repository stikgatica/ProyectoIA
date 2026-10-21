
# Decisión de arquitectura: elección de modelo

**Fecha de comparación:** Martes 20 de octubre de 2026

**Nombre de la miniaplicación:** SIGRA (Sistema Inteligente de Generación de Rutas de Aprendizaje)

**Modelos evaluados:**
- Gemini 3 Flash
- Gemini 3.1 Flash Lite
- Gemini 3.6 Flash

## Modelo elegido

**Elegí el modelo: Gemini 3.1 Flash Lite.**

Mi miniaplicación, **SIGRA**, tiene como objetivo desarrollar un sistema inteligente que permita relacionar los Objetivos de Aprendizaje (OA) de Matemática del currículum chileno, desde 1° hasta 8° básico.

La idea es construir una red de relaciones y prerrequisitos entre los OA de diferentes niveles educativos. En etapas posteriores, esta red permitirá identificar brechas de aprendizaje, realizar diagnósticos adaptativos y generar rutas personalizadas de reforzamiento para los estudiantes.

**Los requisitos que necesito cumplir son:**

- Obtener respuestas claras y coherentes sobre las relaciones entre los OA.
- Identificar posibles prerrequisitos y conexiones entre aprendizajes de distintos cursos.
- Mantener tiempos de respuesta reducidos.
- Minimizar los costos de utilización de la API.
- Facilitar la integración con Python.
- Generar recomendaciones pedagógicas que puedan ser revisadas y validadas por docentes.

## Diagrama de arquitectura

[Diagrama de arquitectura](diagrama_arquitectura.png)

El prototipo considera la siguiente estructura:

**Usuario → Aplicación Python (SIGRA) → API Gemini 3.1 Flash Lite → Procesamiento de respuesta → Presentación de resultados.**

En una etapa posterior, se incorporará una base de datos curricular con los OA y un motor de grafos para gestionar sus relaciones y prerrequisitos.

La inteligencia artificial apoyará la identificación de posibles conexiones curriculares, mientras que la lógica del sistema permitirá organizar las rutas de aprendizaje a partir de relaciones previamente validadas.

## Comparación de candidatos

Los tres modelos fueron evaluados utilizando la misma pregunta relacionada directamente con el desarrollo inicial de SIGRA.

**Pregunta utilizada:**

> Quiero crear un pequeño prototipo de mi proyecto SIGRA (Sistema Inteligente de Generación de Rutas de Aprendizaje). El objetivo es simular una red de relaciones entre Objetivos de Aprendizaje (OA) de Matemática de 1° a 8° básico. ¿Cómo comienzo?

**Condiciones de evaluación:**

- Ejecución de solicitudes mediante Python utilizando la API de Gemini.
- Medición de latencia y costo estimado por operación.
- Revisión de la claridad, pertinencia y utilidad de las respuestas.
- Registro de errores y solicitudes exitosas.

| Criterio | Gemini 3.6 Flash | Gemini 3 Flash | Gemini 3.1 Flash Lite |
|---|---|---|---|
| Costo por 1.000 tokens de entrada | US$0,00075 | US$0,00050 | US$0,00025 |
| Costo por 1.000 tokens de salida | US$0,00375 | US$0,00300 | US$0,00150 |
| Costo promedio por operación exitosa | No disponible | US$0,006898 | US$0,003939 |
| Latencia promedio de operaciones exitosas | No disponible | 10,76 segundos | 5,96 segundos |
| Calidad de respuesta para SIGRA | No evaluable por errores | Muy buena: respuestas detalladas y código Python | Buena: respuestas claras y ejemplos prácticos |
| Solicitudes exitosas | 0 de 5 (0%) | 4 de 4 (100%) | 3 de 4 (75%) |

**Fuente de precios:** [Google AI Studio - Pricing](https://aistudio.google.com/docs/pricing)

*Los valores de latencia, costos por operación y solicitudes exitosas corresponden a las pruebas realizadas con Python. Las tarifas por tokens corresponden a los precios consultados para la API.*

## Justificación

Elegí **Gemini 3.1 Flash Lite** porque presentó la mejor relación entre costo, velocidad y utilidad de las respuestas para las necesidades iniciales de SIGRA.

En las pruebas exitosas, obtuvo una latencia promedio de **5,96 segundos**, frente a los 10,76 segundos de Gemini 3 Flash.

Además, su costo promedio estimado fue de **US$0,003939 por operación**, inferior al de Gemini 3 Flash, que alcanzó US$0,006898.

Aunque Gemini 3 Flash entregó respuestas más detalladas, Gemini 3.1 Flash Lite proporcionó orientaciones suficientemente claras para comenzar el desarrollo del prototipo, incluyendo la utilización de Python, NetworkX y estructuras de grafos para relacionar los Objetivos de Aprendizaje.

Considerando que SIGRA podría necesitar múltiples consultas para analizar relaciones curriculares y apoyar la generación de rutas de aprendizaje, resulta conveniente priorizar un modelo que reduzca los tiempos de espera y los costos operacionales.

La principal limitación observada fue un error de disponibilidad en una de sus cuatro ejecuciones. Por ello, será necesario incorporar mecanismos de reintento y manejo de errores.

## Alternativa descartada y por qué

**Gemini 3 Flash:**

Se descarta como modelo principal debido a su mayor costo y latencia.

Si bien presentó respuestas muy completas y todas sus solicitudes fueron exitosas, para esta primera etapa de SIGRA no se justifica el mayor consumo de recursos, considerando que Gemini 3.1 Flash Lite respondió adecuadamente a la consulta planteada.

**Gemini 3.6 Flash:**

Se descarta debido a los problemas de disponibilidad observados durante las pruebas.

Las cinco solicitudes realizadas terminaron con errores HTTP 503 o por tiempo de espera agotado, impidiendo obtener respuestas para evaluar su calidad.

## Conclusión

**Gemini 3.1 Flash Lite es el modelo seleccionado para el prototipo inicial de SIGRA**, principalmente por su menor costo, mayor rapidez y capacidad para entregar respuestas útiles.

Esta elección permitirá comenzar el desarrollo de la miniaplicación de manera eficiente, manteniendo la posibilidad de integrar otros modelos en el futuro si se requieren tareas de mayor complejidad.

La decisión es provisional, ya que la cantidad de pruebas realizadas es reducida. Antes de utilizar SIGRA con estudiantes reales, será necesario evaluar su estabilidad y la precisión pedagógica de sus recomendaciones.

# SIGRA - Plan de integración sobre ProyectoIA

## Primer incremento (Gate 1)
- Banco JSON de preguntas vinculadas con un identificador **interno** de OA.
- Validación de referencias entre prerrequisitos, alternativas y ciclos.
- Motor 100% determinista de selección de preguntas; retrocede ante respuestas incorrectas.
- Historial básico y ruta de reforzamiento de ejemplo.
- Cuatro pruebas de `pytest` sin depender de internet ni de tokens.

## Siguiente incremento (Gate 2)
1. Reemplazar los identificadores internos de muestra por OA **verificados contra las Bases Curriculares** y anotarlos con grado, eje, fuentes y versión.
2. Validar con docentes las relaciones de prerrequisitos. Un prerrequisito es una decisión curricular, no algo que deba inventar el modelo de IA.
3. Crear un `src/sigra/servicio_ia.py` separado que reutilice funciones de `src/consumir_gemini.py` y devuelva un JSON con `retroalimentacion`, `actividad_sugerida`, `id_oa`. Nunca pasar al proveedor información personal de estudiantes.
4. Validar formatos, valores matemáticos y OA de salida antes de presentarlos a estudiantes; la IA no decide aciertos matemáticos.
5. Añadir trazabilidad, límites de solicitudes y pruebas que simulen caídas 429/500.

## Capstone (Gate 3)
- Backend local (por ejemplo FastAPI) con sesiones separadas, sin exposición de secretos.
- Interfaz web accesible en red interna para aproximadamente 20 estudiantes por curso.
- Persistencia local controlada, cuentas institucionales por rol y exportación de reporte docente.
- Validación de privacidad, políticas de retención y evaluación pedagógica antes de usar datos reales.

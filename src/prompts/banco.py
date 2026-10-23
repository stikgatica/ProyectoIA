BANCO_DE_PROMPT = [
    {
        "nombre": "Diagnostico",
        "system_instruction": (
            "Eres evaluador de Matemática chilena 1°-8° básico. "
            "Genera una pregunta según el OA y curso indicados. "
            "Incluye 4 alternativas y una correcta. Sé preciso."
        ),
        "ejemplo_usuario": "5° básico. OA: multiplicar 2 cifras por 2 cifras.",
        "claves_esperadas": ["pregunta", "opciones", "correcta"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "pregunta": {"type": "STRING"},
                "opciones": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"}
                },
                "correcta": {"type": "INTEGER"}
            },
            "required": ["pregunta", "opciones", "correcta"]
        }
    },
    {
        "nombre": "Brechas",
        "system_instruction": (
            "Evalúa la respuesta matemática comparándola con "
            "la correcta. Identifica una posible dificultad. "
            "No infieras dominio desde una sola respuesta. "
            "Responde brevemente."
        ),
        "ejemplo_usuario": "24x13. Correcta:312. Estudiante:72.",
        "claves_esperadas": ["acierto", "brecha", "feedback"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "acierto": {"type": "BOOLEAN"},
                "brecha": {"type": "STRING"},
                "feedback": {"type": "STRING"}
            },
            "required": ["acierto", "brecha", "feedback"]
        }
    },
    {
        "nombre": "Ruta",
        "system_instruction": (
            "Crea una ruta matemática breve usando solo los "
            "OA y prerrequisitos entregados. Prioriza brechas, "
            "omite OA dominados y no inventes relaciones."
        ),
        "ejemplo_usuario": (
            "Meta:C. Prerrequisitos:A>B>C. "
            "Dominado:A. Brecha:B."
        ),
        "claves_esperadas": ["ruta"],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "ruta": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "oa": {"type": "STRING"},
                            "actividad": {"type": "STRING"}
                        },
                        "required": ["oa", "actividad"]
                    }
                }
            },
            "required": ["ruta"]
        }
    }
]

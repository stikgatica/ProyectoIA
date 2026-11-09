
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

clave = os.getenv("GEMINI_API_KEY")
nombre_modelo = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not clave:
    raise ValueError("Falta GEMINI_API_KEY en el archivo .env")

CONTENIDOS = {
    "1B": {"nombre": "Sumas y restas hasta 20", "nivel": 1, "pregunta": "8 + 5", "respuesta": 13},
    "2B": {"nombre": "Sumas y restas hasta 100", "nivel": 2, "pregunta": "34 - 17", "respuesta": 17},
    "3B": {"nombre": "Multiplicación", "nivel": 3, "pregunta": "6 × 4", "respuesta": 24},
    "4B": {"nombre": "División", "nivel": 4, "pregunta": "48 ÷ 6", "respuesta": 8},
    "5B": {"nombre": "Fracciones", "nivel": 5, "pregunta": "1/3 + 1/3", "respuesta": "2/3"},
    "6B": {"nombre": "Porcentajes", "nivel": 6, "pregunta": "25% de 200", "respuesta": 50},
    "7B": {"nombre": "Números enteros", "nivel": 7, "pregunta": "-8 + 13", "respuesta": 5},
    "8B": {"nombre": "Ecuaciones", "nivel": 8, "pregunta": "3x + 5 = 20. ¿Cuánto vale x?", "respuesta": 5}
}

@tool
def consultar_contenido(consulta: str) -> str:
    """Consulta contenidos matemáticos y ejercicios diagnósticos de SIGRA.
    Acepta un código, como 5B, un nivel, como 5 básico,
    o el nombre de un contenido, como fracciones.
    Úsala cuando el estudiante necesite practicar o conocer un contenido.
    No evalúa respuestas ni determina niveles de aprendizaje.
    """
    consulta_limpia = consulta.strip().casefold()

    for codigo, contenido in CONTENIDOS.items():
        coincide_codigo = consulta_limpia == codigo.casefold()
        coincide_nombre = consulta_limpia == contenido["nombre"].casefold()
        coincide_nivel = consulta_limpia in (
            f"{contenido['nivel']} básico",
            f"{contenido['nivel']} basico",
            f"{contenido['nivel']}b",
            f"{contenido['nivel']}º básico",
            f"{contenido['nivel']}° básico",
        )

        if coincide_codigo or coincide_nombre or coincide_nivel:
            return (
                f"Contenido: {contenido['nombre']}. "
                f"Nivel: {contenido['nivel']}° básico. "
                f"Código: {codigo}. "
                f"Ejercicio diagnóstico: {contenido['pregunta']}."
            )

    return "Contenido no encontrado. Pide al estudiante que revise el nivel o contenido."

@tool
def evaluar_respuesta(codigo: str, respuesta_estudiante: str) -> str:
    """Evalúa una respuesta de un ejercicio diagnóstico de SIGRA.
    Recibe el código del contenido y la respuesta del estudiante.
    Compara la respuesta con la solución registrada.
    Entrega retroalimentación y una recomendación inicial.
    No genera un diagnóstico completo ni modifica registros.
    """
    codigo_limpio = codigo.strip().upper()

    if codigo_limpio not in CONTENIDOS:
        return "Error: el código del contenido no existe."

    contenido = CONTENIDOS[codigo_limpio]
    respuesta_correcta = str(contenido["respuesta"])
    respuesta_recibida = respuesta_estudiante.strip().replace(" ", "").replace(",", ".")

    if not respuesta_recibida:
        return "Error: el estudiante debe proporcionar una respuesta."

    if respuesta_recibida == respuesta_correcta:
        return (
            f"Resultado: correcto. "
            f"Contenido: {contenido['nombre']}. "
            f"Nivel: {contenido['nivel']}° básico. "
            f"Retroalimentación: ¡Muy bien! Resolviste correctamente el ejercicio. "
            f"Ruta sugerida: continuar con ejercicios de mayor complejidad "
            f"del mismo contenido."
        )

    return (
        f"Resultado: incorrecto. "
        f"Contenido: {contenido['nombre']}. "
        f"Nivel: {contenido['nivel']}° básico. "
        f"Respuesta esperada: {respuesta_correcta}. "
        f"Retroalimentación: revisemos el procedimiento paso a paso. "
        f"Ruta sugerida: reforzar los conocimientos previos y practicar "
        f"con ejercicios más sencillos del mismo contenido."
    )

modelo = ChatGoogleGenerativeAI(
    model=nombre_modelo,
    api_key=clave,
    temperature=0,
    timeout=20,
    max_retries=0,
)

herramientas = [consultar_contenido, evaluar_respuesta]

instrucciones = (
    "Eres SIGRA, un asistente inteligente de aprendizaje de Matemática "
    "para estudiantes de 1° a 8° básico de Chile. Responde en español. "
    "Tu propósito es acompañar el aprendizaje matemático mediante "
    "ejercicios diagnósticos, retroalimentación y rutas de aprendizaje. "
    "Para consultar contenidos y ejercicios, usa consultar_contenido. "
    "Para evaluar una respuesta, usa evaluar_respuesta. "
    "Si el estudiante menciona un nivel o contenido y solicita practicar, "
    "consulta primero el ejercicio correspondiente. "
    "Presenta el ejercicio y espera la respuesta del estudiante. "
    "No entregues la solución antes de que el estudiante responda. "
    "Si el estudiante responde un ejercicio, utiliza evaluar_respuesta "
    "con el código correspondiente y su respuesta exacta. "
    "No inventes contenidos, ejercicios, respuestas ni resultados. "
    "Si falta información, pídela. "
    "Si el contenido no existe, informa eso sin inventar una evaluación. "
    "Si la respuesta es incorrecta, explica el procedimiento de manera "
    "clara, gradual y adecuada al nivel del estudiante. "
    "Si la respuesta es correcta, felicita brevemente y sugiere avanzar. "
    "Una sola respuesta no permite determinar el dominio de un contenido. "
    "Las rutas sugeridas son orientativas, no diagnósticos definitivos. "
    "Para un saludo, responde directamente sin usar herramientas. "
    "Utiliza lenguaje cercano, motivador y pedagógico. "
    "No realices modificaciones en registros escolares."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", instrucciones),
    ("human", "{entrada}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agente = create_tool_calling_agent(
    llm=modelo,
    tools=herramientas,
    prompt=prompt,
)

ejecutor = AgentExecutor(
    agent=agente,
    tools=herramientas,
    return_intermediate_steps=True,
    verbose=False,
    max_iterations=4,
)

def probar(entrada: str):
    print("\nPREGUNTA:", entrada)

    resultado = ejecutor.invoke({"entrada": entrada})
    pasos = resultado["intermediate_steps"]

    print("\nTRAZA DE HERRAMIENTAS:")

    if not pasos:
        print("No se utilizaron herramientas.")

    for numero, (accion, observacion) in enumerate(pasos, start=1):
        print(f"\nPaso {numero}")
        print("Herramienta:", accion.tool)
        print("Argumentos:", accion.tool_input)
        print("Observación:", observacion)

    print("\nRESPUESTA FINAL:")

    salida = resultado["output"]

    if isinstance(salida, str):
        print(salida)
    else:
        texto = "\n".join(
            bloque["text"]
            for bloque in salida
            if isinstance(bloque, dict)
            and bloque.get("type") == "text"
            and isinstance(bloque.get("text"), str)
        )
        print(texto)

if __name__ == "__main__":
    print("SIGRA - Sistema Inteligente de Generación de Rutas de Aprendizaje")

    nombres = ", ".join(
        f"{contenido['nivel']}° básico: {contenido['nombre']}"
        for contenido in CONTENIDOS.values()
    )

    print("Contenidos disponibles:", nombres)
    print("Escribe 'salir' para terminar.")

    while True:
        entrada = input("\nTu pregunta: ").strip()

        if entrada.lower() == "salir":
            break

        if not entrada:
            continue

        probar(entrada)

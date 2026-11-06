
import logging

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableBranch,
    RunnablePassthrough,
    RunnableLambda,
)
# Identifica los registros generados por este módulo.
logger = logging.getLogger(__name__)


def construir_paso_clasificacion(modelo):
    # Recibimos el modelo para poder reemplazarlo durante las pruebas.
    plantilla = PromptTemplate.from_template(
        "Clasifica el siguiente mensaje de un estudiante de SIGRA "
        "en una sola palabra: dificultad, progreso o consulta. "
        "Responde solo con esa palabra.\n\n"
        "{mensaje}"
    )
    return (
        plantilla
        | modelo
        | StrOutputParser()
        # Quita espacios, convierte a minúsculas y elimina puntos finales.
        | (lambda texto: texto.strip().lower().rstrip(".").strip())
    )

def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_dificultad=None,
    cadena_progreso=None,
    cadena_consulta=None,
):
    # Si una prueba omite una ruta, esa ruta simplemente deja pasar los datos.
    cadena_dificultad = cadena_dificultad or RunnablePassthrough()
    cadena_progreso = cadena_progreso or RunnablePassthrough()
    cadena_consulta = cadena_consulta or RunnablePassthrough()
    bifurcacion = RunnableBranch(
        # Cada condición recibe el diccionario completo.
        (lambda datos: datos["categoria"] == "dificultad", cadena_dificultad),
        (lambda datos: datos["categoria"] == "progreso", cadena_progreso),

        # Se ejecuta si ninguna condición anterior coincide.
        cadena_consulta,
    )

    return (
        # Conserva mensaje y agrega la categoría calculada.
        RunnablePassthrough.assign(categoria=paso_clasificacion)
        | bifurcacion
    )

def fallback_con_log(datos):
    # Registra la excepción que provocó el uso del fallback.
    logger.warning(
        "Fallo la ruta de dificultad; se ejecuta el fallback: %s",
        datos.get("error"),
    )

    return (
        "SIGRA no pudo generar una ayuda personalizada en este momento. "
        "Nuestro equipo puede revisar tu dificultad. "
        "Mientras tanto, intenta resolver un ejemplo mas sencillo "
        "y revisa paso a paso tu procedimiento."
    )
# Convierte la función de Python en una pieza ejecutable de LangChain.
respuesta_generica = RunnableLambda(fallback_con_log)


def construir_cadena_dificultad_segura(cadena_dificultad):
    return cadena_dificultad.with_fallbacks(
        # Alternativa que se ejecutará si falla la cadena de dificultad.
        [respuesta_generica],

        # Entrega la excepción al fallback bajo la clave "error".
        exception_key="error",
    )

def construir_flujo(modelo):
    # Construye el clasificador con el modelo recibido.
    paso_clasificacion = construir_paso_clasificacion(modelo)

    cadena_consulta = (
        PromptTemplate.from_template(
            "Responde esta consulta de Matematica de un estudiante "
            "de SIGRA con una explicacion clara, "
            "en un solo parrafo:\n\n{mensaje}"
        )
        | modelo
        | StrOutputParser()
    )
    cadena_dificultad = (
        PromptTemplate.from_template(
            "Responde esta dificultad matematica de un estudiante "
            "de SIGRA con empatia, identificando el posible error "
            "y entregando una pista para avanzar, "
            "sin dar directamente la respuesta final, "
            "en un solo parrafo:\n\n{mensaje}"
        )
        | modelo
        | StrOutputParser()
    )
    cadena_progreso = (
        PromptTemplate.from_template(
            "Responde a este progreso de aprendizaje de un estudiante "
            "de SIGRA reconociendo su avance y proponiendo "
            "un siguiente desafio matematico, "
            "en un solo parrafo:\n\n{mensaje}"
        )
        | modelo
        | StrOutputParser()
    )

    # Protege la ruta de dificultad antes de conectarla al enrutador.
    cadena_dificultad_segura = construir_cadena_dificultad_segura(cadena_dificultad)
    # Devuelve un único flujo con todas sus conexiones.
    return construir_cadena_con_enrutamiento(
        paso_clasificacion=paso_clasificacion,
        cadena_dificultad=cadena_dificultad_segura,
        cadena_progreso=cadena_progreso,
        cadena_consulta=cadena_consulta,
    )


def procesar_mensaje_seguro(cadena, mensaje):
    try:
        # Ejecuta el flujo completo con el mensaje recibido.
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        # Captura y registra fallos que no resolvió el fallback.
        logger.error("Error al procesar el mensaje: %s", error)

        return (
            "no pudimos procesar tu mensaje en SIGRA. "
            "Por favor, intenta de nuevo mas tarde."
        )

if __name__ == "__main__":
    # Configura los registros solamente al ejecutar este módulo.
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="errores.log",
        filemode="a",
        encoding="utf-8",
    )

    # Carga las variables de entorno y prepara el modelo.
    load_dotenv()
    modelo = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
    # Construye el flujo, incluyendo el fallback de dificultad.
    cadena_con_enrutamiento = construir_flujo(modelo)

    mensaje = "No entiendo como sumar fracciones con distinto denominador."

    # Ejecuta el flujo bajo la protección general del try/except.
    resultado = procesar_mensaje_seguro(
        cadena_con_enrutamiento,
        mensaje,
    )

    print(resultado)

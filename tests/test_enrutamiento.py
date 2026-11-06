
import pytest

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from src.enrutamiento import (
    construir_paso_clasificacion,
    construir_cadena_con_enrutamiento,
    construir_flujo,
)

# Ejecuta la misma prueba con cuatro categorías diferentes.
@pytest.mark.parametrize("categoria,ruta_esperada", [
    ("dificultad", "dificultad"),
    ("progreso", "progreso"),
    ("consulta", "consulta"),
    ("categoria_inventada", "consulta"),
])
def test_selecciona_solo_una_ruta_y_conserva_mensaje(
    categoria,
    ruta_esperada,
):
    ejecutadas = []

    def crear_ruta(nombre):
        def responder(datos):
            # Registra qué ruta recibió la entrada.
            ejecutadas.append(nombre)

            # Confirma que llegaron el mensaje y la categoría.
            assert datos["mensaje"] == "mensaje original"
            assert datos["categoria"] == categoria

            return nombre

        return RunnableLambda(responder)

    # Devuelve una categoría fija, sin consultar un modelo real.
    clasificador = RunnableLambda(lambda datos: categoria)

    flujo = construir_cadena_con_enrutamiento(
        clasificador,
        crear_ruta("dificultad"),
        crear_ruta("progreso"),
        crear_ruta("consulta"),
    )

    entrada = {"mensaje": "mensaje original"}
    resultado = flujo.invoke(entrada)

    # Comprueba el resultado y que solo se ejecutó una ruta.
    assert resultado == ruta_esperada
    assert ejecutadas == [ruta_esperada]

    # Confirma que no se modificó el diccionario original.
    assert entrada == {"mensaje": "mensaje original"}


@pytest.mark.parametrize("salida,esperada", [
    (" Dificultad \n", "dificultad"),
    ("DIFICULTAD.", "dificultad"),
    ("no estoy seguro", "no estoy seguro"),
])
def test_normaliza_la_salida_del_modelo(salida, esperada):
    # Simula una respuesta del modelo con el formato indicado.
    modelo = RunnableLambda(
        lambda prompt: AIMessage(content=salida)
    )

    clasificador = construir_paso_clasificacion(modelo)

    resultado = clasificador.invoke({"mensaje": "un mensaje"})

    assert resultado == esperada


@pytest.mark.parametrize("categoria,instruccion", [
    ("dificultad", "Responde esta dificultad matematica"),
    ("progreso", "Responde a este progreso de aprendizaje"),
    ("consulta", "Responde esta consulta de Matematica"),
    ("desconocida", "Responde esta consulta de Matematica"),
])
def test_flujo_completo_usa_dos_consultas_y_la_ruta_correcta(
    categoria,
    instruccion,
):
    prompts = []

    # Primera respuesta: categoría. Segunda respuesta: texto final.
    respuestas = iter([categoria, "respuesta simulada"])

    def responder(prompt):
        # Guarda cada instrucción recibida por el modelo falso.
        prompts.append(prompt.to_string())

        # Entrega la siguiente respuesta prefijada.
        return AIMessage(content=next(respuestas))

    flujo = construir_flujo(RunnableLambda(responder))

    resultado = flujo.invoke({
        "mensaje": "NO ENTIENDO LAS FRACCIONES"
    })

    # Una consulta clasifica y otra genera la respuesta.
    assert len(prompts) == 2

    # Ambas consultas deben recibir el mensaje original.
    assert all(
        "NO ENTIENDO LAS FRACCIONES" in prompt
        for prompt in prompts
    )

    # La segunda consulta debe usar la instrucción de la ruta esperada.
    assert instruccion in prompts[1]

    # Nuestro flujo devuelve la respuesta como texto.
    assert resultado == "respuesta simulada"

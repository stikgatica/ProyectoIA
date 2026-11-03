
import json
from pathlib import Path

# RUTAS DE LOS ARCHIVOS
RAIZ = Path(__file__).resolve().parent.parent

ARCHIVO_RESULTADOS = RAIZ / "resultados_metricas_sigra.json"
ARCHIVO_REVISION = RAIZ / "revision_manual.json"
ARCHIVO_INFORME = RAIZ / "docs" / "revision_manual.md"


def leer_json(ruta, defecto=None):
    if not ruta.exists():
        if defecto is not None:
            return defecto
        raise FileNotFoundError(f"No se encontró: {ruta}")

    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


# SELECCIONAR LOS 5 F1 MÁS BAJOS Y LOS 5 MÁS ALTOS
def seleccionar_casos(resultados):
    unicos = {}

    for caso in resultados:
        if "consulta" not in caso or "f1" not in caso:
            raise ValueError(
                "Cada resultado necesita 'consulta' y 'f1'."
            )
        unicos[caso["consulta"]] = caso

    if len(unicos) < 10:
        raise ValueError("Se necesitan al menos 10 consultas distintas.")

    ordenados = sorted(
        unicos.values(),
        key=lambda caso: float(caso["f1"])
    )

    bajos = ordenados[:5]
    consultas_bajas = {caso["consulta"] for caso in bajos}

    altos = [
        caso
        for caso in reversed(ordenados)
        if caso["consulta"] not in consultas_bajas
    ][:5]

    return (
        [("F1 bajo", caso) for caso in bajos]
        + [("F1 alto", caso) for caso in altos]
    )


# PEDIR LA EVALUACIÓN DEL USUARIO
def preguntar(mensaje, opciones):
    while True:
        valor = input(mensaje).strip().lower()

        if valor == "q":
            return None

        if valor in opciones:
            return opciones[valor]

        print("Opción incorrecta. Intente nuevamente.")


def texto_tabla(valor):
    return str(valor).replace("|", "\\|").replace("\n", " ")


# GENERAR INFORME MARKDOWN
def generar_informe(seleccionados, revisiones):
    por_consulta = {
        item["consulta"]: item for item in revisiones
    }

    lineas = [
        "# Revisión manual de respuestas de SIGRA",
        "",
        "Se seleccionaron cinco casos con F1 bajo y cinco "
        "con F1 alto.",
        "",
        "El F1 basado en coincidencias textuales no equivale "
        "a exactitud matemática.",
        "",
        "| Grupo | Consulta | F1 | Exactitud | Completitud | Contradicciones |",
        "|---|---|---:|---|---|---|",
    ]

    for grupo, caso in seleccionados:
        revision = por_consulta.get(caso["consulta"], {})

        lineas.append(
            f"| {grupo} "
            f"| {texto_tabla(caso['consulta'])} "
            f"| {float(caso['f1']):.4f} "
            f"| {revision.get('exactitud', 'Pendiente')} "
            f"| {revision.get('completitud', 'Pendiente')} "
            f"| {revision.get('contradicciones', 'Pendiente')} |"
        )

    lineas.extend(["", "## Observaciones por caso", ""])

    for numero, (grupo, caso) in enumerate(seleccionados, 1):
        revision = por_consulta.get(caso["consulta"], {})

        lineas.extend([
            f"### {numero}. {caso['consulta']} ({grupo})",
            "",
            f"- Referencia: {caso.get('referencia', '')}",
            f"- Respuesta: {caso.get('respuesta', '')}",
            f"- F1: {float(caso['f1']):.4f}",
            f"- Observación: {revision.get('observacion', 'Pendiente')}",
            "",
        ])

    ARCHIVO_INFORME.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ARCHIVO_INFORME.write_text(
        "\n".join(lineas),
        encoding="utf-8"
    )


# PROGRAMA PRINCIPAL
def main():
    resultados = leer_json(ARCHIVO_RESULTADOS)

    if not isinstance(resultados, list):
        raise ValueError(
            "El archivo de resultados debe contener una lista JSON."
        )

    seleccionados = seleccionar_casos(resultados)

    revisiones = leer_json(
        ARCHIVO_REVISION,
        defecto=[]
    )

    if not isinstance(revisiones, list):
        raise ValueError(
            "El archivo de revisión debe contener una lista JSON."
        )

    revisadas = {
        revision["consulta"] for revision in revisiones
    }

    print(f"Resultados cargados: {len(resultados)}")
    print(f"Revisiones recuperadas: {len(revisadas)}")
    print("Se revisarán 5 casos con F1 bajo y 5 con F1 alto.")
    print("Opciones: s = sí, n = no, p = parcial, q = salir")

    for numero, (grupo, caso) in enumerate(seleccionados, 1):
        consulta = caso["consulta"]

        if consulta in revisadas:
            print(f"Ya revisada: {consulta}")
            continue

        print("\n" + "=" * 60)
        print(f"CASO {numero}/10 - {grupo}")
        print(f"Consulta: {consulta}")
        print(f"Referencia: {caso.get('referencia', '')}")
        print(f"Respuesta: {caso.get('respuesta', '')}")
        print(f"F1: {float(caso['f1']):.4f}")
        print("=" * 60)

        exactitud = preguntar(
            "¿Es matemáticamente correcta? [s/n/p/q]: ",
            {"s": "Sí", "n": "No", "p": "Parcial"}
        )

        if exactitud is None:
            break

        completitud = preguntar(
            "¿Responde de forma completa? [s/n/p/q]: ",
            {"s": "Sí", "n": "No", "p": "Parcial"}
        )

        if completitud is None:
            break

        contradicciones = preguntar(
            "¿Contiene contradicciones o errores internos? [s/n/q]: ",
            {"s": "Sí", "n": "No"}
        )

        if contradicciones is None:
            break

        observacion = input(
            "Escriba su observación: "
        ).strip()

        revision = {
            "consulta": consulta,
            "grupo": grupo,
            "f1": float(caso["f1"]),
            "referencia": caso.get("referencia", ""),
            "respuesta": caso.get("respuesta", ""),
            "exactitud": exactitud,
            "completitud": completitud,
            "contradicciones": contradicciones,
            "observacion": observacion,
        }

        revisiones.append(revision)
        revisadas.add(consulta)

        # Guardar inmediatamente para no perder avances
        guardar_json(ARCHIVO_REVISION, revisiones)
        generar_informe(seleccionados, revisiones)

        print("Revisión guardada correctamente.")

    generar_informe(seleccionados, revisiones)

    completadas = sum(
        caso["consulta"] in revisadas
        for _, caso in seleccionados
    )

    print("\nREVISIÓN FINALIZADA")
    print(f"Casos revisados: {completadas}/10")
    print(f"Resultados: {ARCHIVO_REVISION}")
    print(f"Informe: {ARCHIVO_INFORME}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
    except (KeyboardInterrupt, EOFError):
        print(
            "\nPrograma interrumpido. "
            "Las evaluaciones guardadas se conservarán."
        )

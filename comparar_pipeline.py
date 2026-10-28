
from cliente import consultar_modelo

from pipeline_limpieza import procesar_texto


casos = [
    (
        "¿Qué es Python?",
        "Python es un lenguaje de programación interpretado."
    ),
    (
        "¿Qué son las fracciones equivalentes?",
        "Dos fracciones son equivalentes cuando representan la misma cantidad."
    ),
    (
        "¿Qué es un número primo?",
        "Un número primo es un número natural mayor que uno que tiene exactamente dos divisores: uno y sí mismo."
    )
]


for numero, (consulta, referencia) in enumerate(casos, start=1):
    respuesta = consultar_modelo(consulta)

    crudo_ref = referencia.split()
    crudo_resp = respuesta.split()
    comunes_crudo = set(crudo_ref) & set(crudo_resp)
    pct_crudo = len(comunes_crudo) / len(set(crudo_ref))

    tokens_ref = procesar_texto(referencia)
    tokens_resp = procesar_texto(respuesta)
    comunes = set(tokens_ref) & set(tokens_resp)
    pct_proc = len(comunes) / len(set(tokens_ref))

    print(f"\n[Caso {numero}] Consulta: {consulta}")
    print(f"[Caso {numero}] Referencia: {referencia}")
    print(f"[Caso {numero}] Respuesta real: {respuesta}")
    print(f"[Caso {numero}] Coincidencia texto crudo: {pct_crudo:.1%}")
    print(f"[Caso {numero}] Coincidencia texto procesado: {pct_proc:.1%}")

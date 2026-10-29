"""Demo completamente local y sin datos personales."""
from pathlib import Path
from src.sigra.motor import SesionDiagnostico, cargar_banco

banco = cargar_banco(Path('data/sigra/banco_oa_ejemplo.json'))
sesion = SesionDiagnostico(banco, ['SIGRA-MAT-5-FRACC-EQ'])

# Simula estudiante que falla fracciones y división, y acierta tablas.
respuestas_demo = [0, 0, 1]
for alternativa in respuestas_demo:
    pregunta = sesion.siguiente_pregunta()
    if pregunta is None:
        break
    print('\nOA:', pregunta['id_oa'])
    print(pregunta['pregunta'])
    print('Opciones:', pregunta['alternativas'])
    print('Resultado:', sesion.responder(alternativa))

print('\nRuta de reforzamiento:', sesion.ruta_refuerzo())

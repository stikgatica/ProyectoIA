from google import genai

PROJECT_ID = "pruebastuning-515221"
LOCATION = "us-central1"

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

tuning_job = (
    "projects/71514445740/locations/us-central1/"
    "tuningJobs/5767038895430565888"
)

# Consultar estado
job = client.tunings.get(name=tuning_job)

print("Estado actual:", job.state)

# Preguntar antes de cancelar
respuesta = input("¿Deseas cancelar el entrenamiento? (s/n): ")

if respuesta.lower() == "s":
    client.tunings.cancel(name=tuning_job)
    print("Cancelación solicitada correctamente.")
else:
    print("El entrenamiento no fue cancelado.")
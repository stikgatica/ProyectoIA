#El nombre de la estudiante
#La calificación del curso
#El titulo de la segunda tarea
#Si la primera tarea está completada
estudiante = {
    "nombre": "Ana",
    "edad": 24,
    "curso": {
        "nombre": "Python",
        "calificacion": 92
    },
    "tareas": [
        {
            "titulo": "Variables",
            "completada": True
        },
        {
            "titulo": "Consumo de APIs",
            "completada": False
        }
    ]
}

print(estudiante["nombre"])
print(estudiante["curso"]["calificacion"])
print(estudiante["tareas"][1]["titulo"])
print(estudiante["tareas"][1]["completada"])
print("El titulo de la segunda tarea", estudiante["tareas"][1]["titulo"])
if estudiante["tareas"][0]["completada"]:
    print("La primera tarea está completada")

print("La primera tarea está completada", "Sí" if estudiante["tareas"][0]["completada"] else "No")





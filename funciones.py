def suma(a, b):
    resultado = a + b
    return resultado

print(suma(5, 6))

curso= {
    "nombre": "Especialización de IA",
    "horas": 180,
    "estudiantes": [
        {
            "nombre": "Juana",
            "apellido": "De Arco",
            },
            {
                "nombre": "Juan",
                "apellido": "Pérez"
            }
    ]
}


print(curso["estudiantes"][2]["nombre"])

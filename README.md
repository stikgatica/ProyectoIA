# Proyecto Gradual de Stik Gatica — Especialización en Desarrollo con IA Generativa (Accenture)

Esta es la estructura base que vas a usar como punto de partida para tu proyecto en este programa. Es la misma estructura que vas a ir ampliando bloque a bloque, hasta llegar a la aplicación completa que entregas en el Gate 3.

## Cómo empezar

1. Abre el terminal `Gitbash` en `VS Studio Code` y dirígete a la carpeta donde quieres guardar el proyecto utilizando `cd NombreCarpetaInstalación`
2. Clona este repositorio utilizando el comando `git clone https://github.com/stikgatica/ProyectoIA.git`
4. Entra en la carpeta del proyecto utilizando `cd ProyectoIA`
5. Abre el proyecto en Visual Studio Code utilizando `code .`
6. Abre nuevamente en esa ventana del proyecto el terminal y crea tu entorno virtual de Python utilizando `py -m venv .venv`
7. Activa el entorno virtual utilizando `source .venv/Scripts/activate`
8. Instala las dependencias utilizando `python -m pip install -r requirements.txt`
9. Crea tu archivo `.env` a partir del archivo `.env.example` utilizando el comando `cp .env.example .env`
10. Abre el archivo `.env` que acabas de crear y agrega tu clave `GEMINI_API_KEY`, recuerda guardar los cambios `CTRL + S` .
11. Para ejecutar las pruebas de la aplicación, utiliza el comando `python src/consumir_gemini.py` o `python src/consistencia.py`


## Estructura de carpetas

- `src/` : todo el código fuente de tu proyecto va aquí.
- `docs/` : documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas).
- `tests/` : pruebas de tu código (las vas a usar más adelante en el programa, cuando el proyecto lo requiera).
- `requirements.txt` : dependencias de Python de tu proyecto, para que cualquier otra persona pueda reconstruir tu entorno con un solo comando.
- `.env.example` : plantilla de las variables de entorno que tu proyecto necesita, sin valores reales. Tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore` : le dice a Git qué archivos y carpetas ignorar (entre ellos, tu entorno virtual y tu archivo `.env`).

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.

## Registro del ensayo de instalación limpia
 
- Fecha: 2026-10-24 18:30
- Encontrado: Faltaba python-dotenv en requirements.txt
- Corregido: agregado con 'pip freeze > requirements.txt' y commiteado
- Resultado tras la corrección: Error API KEY not valid

- Fecha: 2026-10-24 18:35
- Encontrado: Faltaba renombre en .env.example a "GEMINI_API_KEY"
- Corregido: renombrado donde se ingresa la key de Gemini
- Resultado tras la corrección: Funciona con éxito

## Registro del ensayo de rate limit
 
- Fecha: 2026-10-26
- Peticiones enviadas: 10
- Petición donde apareció el primer 429: la número 4
- Esperas observadas: 2.1s, 4.2s (backoff exponencial con jitter, correcto)
- Costo total del ensayo: $0.00710
- Resultado: todas las peticiones terminaron con éxito tras reintentar


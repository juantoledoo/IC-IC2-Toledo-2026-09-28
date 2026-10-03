# Clase 3 - Parte C: notas

## C2 - El requirements.txt olvidado

La primera vez el `requirements.txt` solo tenía `fastapi`. El contenedor murió
al arrancar (`docker ps -a` mostró `Exited (1)`) y `docker logs api-libros`
mostró `No module named uvicorn`. `fastapi` es el framework y `uvicorn` es el
servidor que lo ejecuta: son paquetes distintos. En mi máquina andaba porque
estaban instalados en el venv de la clase 2, pero la imagen es un entorno
limpio que solo tiene lo declarado en el `requirements.txt`. Lo resolví
agregando `uvicorn`.

## C3 - "El contenedor corre pero no llego a /docs"

**(a) Sin publicar el puerto (sin `-p`).** `docker logs` mostró
`Uvicorn running on http://0.0.0.0:8000`: la API funciona adentro. `docker ps`
mostró `8000/tcp` sin flecha hacia mi máquina. Desde afuera:
`curl: (7) Failed to connect to 127.0.0.1 port 8000 ... Could not connect to server`
(y `ERR_CONNECTION_REFUSED` en el navegador). Es "connection refused": nadie
atiende en ese puerto de mi máquina, porque el puerto no está publicado. El
`EXPOSE` del Dockerfile solo documenta.

**(b) Puerto publicado pero sin `--host`.** `docker logs` mostró
`Uvicorn running on http://127.0.0.1:8000`. Desde afuera:
`curl: (52) Empty reply from server` (y `ERR_EMPTY_RESPONSE` en el navegador).
El puerto sí está publicado, pero la conexión se corta sin respuesta.

**Cómo distinguirlos:** "refused / couldn't connect" es puerto sin publicar;
"empty reply / connection reset", con el log diciendo `127.0.0.1`, es uvicorn
escuchando solo en localhost.

**Qué significa `127.0.0.1` adentro de un contenedor:** es el `localhost` del
propio contenedor, y solo acepta conexiones que se originan adentro de ese
mismo contenedor. Lo que llega desde mi máquina entra por otra interfaz de red
del contenedor, que uvicorn ignora si escucha solo en `127.0.0.1`. Con
`--host 0.0.0.0` escucha en todas las interfaces.


## C4 - Lo que no tiene que viajar

Recreé el problema poniendo un `venv` y una carpeta `__pycache__` dentro de
`ejercicios-C`. Sin `.dockerignore`, el `COPY . .` los metió en la imagen: lo
comprobé con `docker exec api-libros ls -a /app`, que listó `venv` y
`__pycache__`. Agregué un `.dockerignore` con `venv/`, `**/__pycache__/`,
`*.pyc`, `.git/` y `.pytest_cache/`; la imagen resultante (`api-libros:limpia`)
pesa menos que la anterior (`api-libros:con-venv`, comparadas con
`docker images api-libros`) y ya no tiene esas carpetas adentro.

Un `venv` de mi máquina no serviría adentro del contenedor: tiene programas
compilados para Windows y rutas de mi computadora que adentro no existen (el
contenedor es Linux). Además la imagen instala sus propias dependencias con
`pip` durante el build.


Aclaración: si miro adentro de un contenedor que ya está corriendo, con
`docker exec api-libros ls -a /app`, aparece un `__pycache__` aunque el
`.dockerignore` lo excluya. No viajó con el `COPY`: lo genera Python al arrancar
la API, cuando uvicorn importa `main.py`. Para ver lo que realmente trae la
imagen hay que listar sin arrancar la API:
`docker run --rm api-libros:limpia ls -a /app`, que no muestra ni `venv` ni
`__pycache__`.


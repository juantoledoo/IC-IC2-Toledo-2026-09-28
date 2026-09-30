# Clase 3 - Parte A: imagen vs contenedor

## A1 - Tu primer contenedor

Corrí `docker run --name hola-mundo hello-world` y salió el mensaje "Hello from
Docker!" sin instalar nada. Después corrí
`docker run --name python-version python:3.11-slim python --version`, que
imprimió la versión de Python del contenedor (3.11.x). La versión de Python de
mi máquina es otra (3.12.5): el contenedor trae su propio Python y no depende
del que tenga instalado.

## A2 - La misma imagen, varios contenedores

Levanté dos contenedores de la misma imagen con
`docker run -d --name espera1 python:3.11-slim sleep 3600` y lo mismo con
`espera2`. `docker ps` mostró los dos, ambos con la imagen `python:3.11-slim`,
y `docker images` mostró esa imagen una sola vez. La imagen es una (el molde) y
los contenedores son varios (las galletas): cada uno corre por separado.

## A3 - ¿Adónde se fue mi contenedor?

Corrí un contenedor que imprime un texto y termina. No aparece en `docker ps`
porque `docker ps` muestra solo los contenedores que están corriendo, y este ya
terminó: no se rompió, su proceso llegó al final y el contenedor se detuvo. Con
`docker ps -a` aparece con estado `Exited (0)` (terminó sin errores), y con
`docker logs imprime-y-termina` recupero lo que imprimió, aunque ya no esté
corriendo.

## A4 - Descartable

Entré a `espera1` con `docker exec -it espera1 sh`, creé `/tmp/archivo.txt` y
salí. Después borré el contenedor con `docker rm -f espera1` y levanté otro
(`espera3`) de la misma imagen: el archivo no estaba. Lo que se escribe adentro
de un contenedor muere con él, y la imagen no cambió: cada contenedor nuevo
parte de la imagen original. (Esto vuelve en la Parte D, con la base de datos:
para que sus datos sobrevivan hay que guardarlos fuera del contenedor.)

## A5 - Explicalo

Una **imagen** es el paquete estático y congelado con el programa y todo lo que
necesita para correr (sistema base, Python, librerías, archivos), y un
**contenedor** es esa imagen en ejecución: de una misma imagen salen muchos
contenedores. Docker resuelve el "en mi máquina anda y en la tuya no" porque
empaqueta el programa junto con todo su entorno, así que corre igual en
cualquier computadora que tenga Docker. El `venv` solo aislaba las librerías de
Python; no aislaba la versión de Python, ni el sistema operativo, ni los
programas que no son de Python (como un broker MQTT o una base de datos), y
además había que acordarse de activarlo.


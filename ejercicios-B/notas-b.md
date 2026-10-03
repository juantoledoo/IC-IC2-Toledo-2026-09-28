# Clase 3 - Parte B: notas

## B2 - Por qué no hace falta un venv adentro de la imagen

El `venv` aísla las librerías de distintos proyectos que comparten un mismo
Python. Adentro de la imagen no se comparte nada: el contenedor ya es un
entorno aislado y dedicado a un solo programa, así que las librerías se
instalan directo con `pip`. `requests` quedó instalado adentro de la imagen y
no en mi máquina.

## B3 - Rompelo a propósito

Al sacar el `RUN pip install -r requirements.txt`, el `docker build` terminó
bien, pero al correr el contenedor falló con
`ModuleNotFoundError: No module named 'requests'`. Falló **al correr**, no al
construir: el build solo ejecuta las instrucciones del Dockerfile y no verifica
que el script funcione. En mi máquina el script anda porque `requests` está
instalado acá, pero la imagen es un entorno limpio que solo tiene lo que le
pedí instalar. Si una librería no está en el `requirements.txt` y no se instala
en el Dockerfile, no está en la imagen.


## B4 - RUN vs CMD

Agregué un `RUN echo ...` al Dockerfile y corrí el contenedor tres veces. El
texto del `RUN` se imprimió una sola vez, durante el `docker build` (usando
`--progress=plain` para verlo), y quedó guardado en la imagen. El `CMD` (mi
script) se ejecutó las tres veces, una por cada contenedor que arranqué. `RUN`
pasa una vez al construir la imagen; `CMD` pasa cada vez que arranca un
contenedor.


## B5 - La caché de capas

Con `COPY . .` antes del `RUN pip install`, cambiar una sola línea del script
invalidó la capa del `COPY` y todas las siguientes, así que el `pip install`
se ejecutó de nuevo. Lo arreglé reordenando: primero `COPY requirements.txt .`,
después `RUN pip install -r requirements.txt` y al final `COPY . .`. Docker
reutiliza las capas hasta la primera que cambió: el `requirements.txt` casi no
cambia, así que su capa y la del `pip install` se reutilizan, y lo que cambia
seguido (el código) queda al final, donde invalida solo su propia capa.


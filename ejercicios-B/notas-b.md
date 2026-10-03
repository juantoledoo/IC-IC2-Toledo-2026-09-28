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

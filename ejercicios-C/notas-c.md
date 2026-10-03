# Clase 3 - Parte C: notas

## C2 - El requirements.txt olvidado

La primera vez el `requirements.txt` solo tenía `fastapi`. El contenedor murió
al arrancar (`docker ps -a` mostró `Exited (1)`) y `docker logs api-libros`
mostró `No module named uvicorn`. `fastapi` es el framework y `uvicorn` es el
servidor que lo ejecuta: son paquetes distintos. En mi máquina andaba porque
estaban instalados en el venv de la clase 2, pero la imagen es un entorno
limpio que solo tiene lo declarado en el `requirements.txt`. Lo resolví
agregando `uvicorn`.


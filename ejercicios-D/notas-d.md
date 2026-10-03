# Clase 3 - Parte D: notas

## D1 - Dos servicios

El `compose.yaml` define dos servicios: `api` (que se construye con el
Dockerfile de la carpeta `api`) y `base` (la imagen oficial `postgres:16`).
Con `docker compose up -d` se levantaron juntos. Al principio la base se moría
a los pocos segundos: `docker compose ps -a` la mostraba como `Exited (1)` y
`docker compose logs base` decía que la base no estaba inicializada y que no se
había especificado la contraseña del superusuario. La imagen oficial de
Postgres se niega a arrancar sin la variable de entorno `POSTGRES_PASSWORD`
(está documentada en su página de Docker Hub). La agregué en `environment:` del
servicio y desde entonces los dos servicios siguen vivos en
`docker compose ps`. La contraseña es solo de práctica, para una base local.


## D2 - Sumar el broker

Agregué un tercer servicio, `broker`, con la imagen `eclipse-mosquitto:2` y el
puerto 1883 publicado. Con `docker compose up -d` los tres servicios (`api`,
`base` y `broker`) levantaron con un solo comando y quedaron en `Up` en
`docker compose ps`. El broker no lo instalé ni lo programé: lo bajé como
imagen oficial. En sus logs aparece que arranca en "modo local" (solo acepta
clientes de adentro de su propio contenedor), algo que hay que cambiar con un
archivo de configuración más adelante.


## D3 - Configuración por variables de entorno

Agregué a la API un endpoint `GET /salud` que intenta conectarse a Postgres con
`psycopg` y responde `{"base": "ok"}` o, si falla, un `503` con el motivo. El
host, el puerto, el usuario, la contraseña y el nombre de la base no están en el
código: la API los lee con `os.environ` y el `compose.yaml` se los pasa con
`environment:`. Lo comprobé buscando la contraseña en `main.py` (no aparece) y
cambiando solo `DB_HOST` en el compose: con `base-que-no-existe` la API devolvió
503 con "Name or service not known", y con `base` volvió a responder ok. Así el
mismo código corre en mi máquina, en el compose o en un servidor cambiando solo
la configuración, y la contraseña no queda subida a GitHub dentro de un `.py`.


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

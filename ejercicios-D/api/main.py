import os

import psycopg
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()


class Editorial(BaseModel):
    nombre: str
    pais: str


class Libro(BaseModel):
    titulo: str
    paginas: int = Field(gt=0)
    disponible: bool = True
    editorial: Editorial | None = None


class Autor(BaseModel):
    nombre: str
    pais: str


libros = [
    Libro(titulo="El Aleph", paginas=180),
    Libro(titulo="Rayuela", paginas=600),
    Libro(titulo="Ficciones", paginas=200),
]

autores = [
    Autor(nombre="Jorge Luis Borges", pais="Argentina"),
    Autor(nombre="Julio Cortazar", pais="Argentina"),
]


@app.get("/")
def raiz():
    return {"mensaje": "hola"}


@app.get("/libros")
def listar_libros(paginas_min: int | None = None):
    if paginas_min is None:
        return libros
    filtrados = []
    for libro in libros:
        if libro.paginas >= paginas_min:
            filtrados.append(libro)
    return filtrados


@app.post("/libros", status_code=201)
def crear_libro(libro: Libro):
    libros.append(libro)
    return libro


@app.get("/libros/{titulo}")
def obtener_libro(titulo: str):
    for libro in libros:
        if libro.titulo == titulo:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.put("/libros/{titulo}")
def reemplazar_libro(titulo: str, libro_nuevo: Libro):
    for i in range(len(libros)):
        if libros[i].titulo == titulo:
            libros[i] = libro_nuevo
            return libro_nuevo
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.delete("/libros/{titulo}", status_code=204)
def borrar_libro(titulo: str):
    for i in range(len(libros)):
        if libros[i].titulo == titulo:
            libros.pop(i)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.get("/autores")
def listar_autores():
    return autores


@app.post("/autores", status_code=201)
def crear_autor(autor: Autor):
    autores.append(autor)
    return autor


def conectar_db():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dbname=os.environ["DB_NAME"],
        connect_timeout=3,
    )


@app.get("/salud")
def salud():
    try:
        with conectar_db() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return {"base": "ok"}
    except KeyError as error:
        motivo = f"falta la variable de entorno {error}"
    except Exception as error:
        motivo = str(error)
    return JSONResponse(status_code=503, content={"base": "error", "motivo": motivo})

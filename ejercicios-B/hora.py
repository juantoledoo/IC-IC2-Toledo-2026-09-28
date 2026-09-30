from datetime import datetime

ahora = datetime.now()
print("Hola desde un contenedor de Docker")
print("Fecha y hora dentro del contenedor:", ahora.strftime("%Y-%m-%d %H:%M:%S"))

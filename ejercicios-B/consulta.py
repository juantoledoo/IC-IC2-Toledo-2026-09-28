import requests

respuesta = requests.get("https://example.com", timeout=10)
print("Codigo de estado:", respuesta.status_code)
print("Caracteres recibidos:", len(respuesta.text))
print("Version del script: 3")


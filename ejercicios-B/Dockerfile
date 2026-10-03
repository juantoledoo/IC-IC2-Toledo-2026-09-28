FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN echo "RUN: esto se ejecuta UNA vez, al construir la imagen"
CMD ["python", "consulta.py"]

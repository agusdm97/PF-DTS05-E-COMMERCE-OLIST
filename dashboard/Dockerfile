FROM python:3.10-slim

# Copia el archivo requirements.txt
COPY requirements.txt /requirements.txt

# Instala las dependencias
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./src /src
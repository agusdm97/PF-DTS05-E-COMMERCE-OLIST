import json
import requests
import pandas as pd
from dotenv import load_dotenv
import os


# Carga de variables de entorno ubicadas en el archivo .env (puede obtener sus credenciales en https://www.back4app.com/database/back4app/brazil-zip-code-database)
load_dotenv()

# Parámetros de consulta de API
skip = 0
LIMIT = 100
X_PARSE_APPLICATION_ID = os.getenv("X_PARSE_APPLICATION_ID")
X_PARSE_REST_API_KEY = os.getenv("X_PARSE_REST_API_KEY")

# Parámetros del bucle
data_empty = False

# Listas de salida de datos
latitude = []
longitude = []
zip_code = []
city_name = []

while not data_empty:
    url = f"https://parseapi.back4app.com/classes/Worldzipcode_BR?skip={skip}&limit={LIMIT}&keys=geoPosition,placeName,postalCode"
    headers = {
        "X-Parse-Application-Id": X_PARSE_APPLICATION_ID,  # ID de la aplicación
        "X-Parse-REST-API-Key": X_PARSE_REST_API_KEY,  # REST API key
    }
    data = json.loads(
        requests.get(url, headers=headers).content.decode("utf-8")
    )  # Respuesta de la API
    skip += 100

    # Chequeo de respuesta de la API en blanco
    if len(data.get("results")) == 0:
        data_empty = True
        continue

    # Iteración de los resultados
    for result in data.get("results"):
        latitude.append(result.get("geoPosition").get("latitude"))
        longitude.append(result.get("geoPosition").get("longitude"))
        zip_code.append(result.get("postalCode"))
        city_name.append(result.get("placeName"))


# Creación del dataframe
df = pd.DataFrame(
    {
        "city_name": city_name,
        "latitude": latitude,
        "longitude": longitude,
        "zip_code": zip_code,
    }
)

# Guardado de los datos en un archivo csv
df.to_csv(path_or_buf="datasets/br_zip_code.csv", index=False)

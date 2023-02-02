FROM apache/airflow:2.5.0

# Copia el archivo requirements.txt
COPY requirements.txt /requirements.txt

# Instala las dependencias
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Copia el modulo de ETL
COPY ./etl_module /opt/airflow/etl_module

# Añade el modulo de ETL al PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/etl_module"
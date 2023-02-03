<p align="center">
  <img src="etapas_del_proyecto/_src/logo_white.png" alt="Logo Data Insights">
</p>

# TITULO DEL PROYECTO

## Introducción

## Problemática del proyecto

## Solución propuesta

## Estructura del repositorio

Este repositorio tiene una estructura organizada para facilitar la gestión del proyecto. A continuación, se describen las carpetas principales y su contenido:

### Carpeta: etapas_del_proyecto

```
.
└── etapas_del_proyecto
    └── etapa_1
    └── etapa_2
    └── etapa_3

```

Esta carpeta contiene los reportes de los avances del proyecto en sus diferentes etapas. Cada etapa está contenida en una carpeta para una fácil gestión.

### Carpeta: data_warehouse

```
.
└── data_warehouse
    └── apache_airflow
    └── datasets
    └── datasets_incremental
    └── etl_module
```

Esta carpeta contiene todo lo relacionado a la implementación de Apache Airflow, los datasets originales del proyecto, los datasets generados para las pruebas de carga incremental y el módulo de ETL desarrollado en Python.

### Carpeta: dashboard

```
.
└── dashboard
    └── app
```

Esta carpeta contiene la aplicación desarrollada en Streamlit que permite la visualización de los datos.

### Carpeta: machine_learning

```
.
└── machine_learning
    └── app
    └── models
    └── notebooks
```

Esta carpeta contiene los notebooks de Python utilizados para las pruebas y generación de modelos de Machine Learning (ML), los modelos generados y la aplicación desarrollada en Streamlit para probar los modelos de ML

## Instalación

El proyecto ha sido desarrollado utilizando Docker, por lo que la instalación es simple. Siga los siguientes pasos para correr el proyecto:

1.  Clone el repositorio:

    ```cmd
    git clone https://github.com/agusdm97/PF-DTS05-E-COMMERCE-OLIST.git
    ```

2.  Navegue hasta la carpeta raíz del proyecto:

    ```cmd
    cd PF-DTS05-E-COMMERCE-OLIST
    ```

3.  Ejecute el siguiente comando para levantar los contenedores de Docker:

    :warning: ADVERTENCIA: El siguiente paso puede ser estresante para algunas computadoras. Por favor, asegúrese
    de tener suficiente memoria y recursos de procesamiento antes de ejecutar este comando.

    ```cmd
    docker-compose up -d
    ```

## Uso

Una vez que los contenedores se encuentran funcionando correctamente deberá seguir los siguientes pasos:

1. Entrar a MinIO y subir los datasets:

Esto se puede lograr entrando al siguiente enlace [MinIO], se debe ingresar con el usuario `root` y la contraseña `password`. Luego de ingresar se tiene que crear un bucket llamado `airflow` y se tienen que cargar los datasets.

![Minio GIF](etapas_del_proyecto/_src/MinIO.gif)

2. Entrar a Airflow y activar la DAG:

Esto se puede lograr entrando al siguiente enlace [Airflow], se debe ingresar con el usuario `root` y la contraseña `password`. Luego de ingresar se tiene que ingresar en la DAG llamada `carga_inicial` y activarla.

![Airflow GIF](etapas_del_proyecto/_src/Airflow.gif)

3. Entrar al Dashboard y a la app de Machine Learning:

Una vez terminado el paso anterior ya se puede acceder al [Dashboard] para visualizar los datos y a la [App-ML] para explorar los modelos de ML.

[minio]: (http://localhost:9090)
[airflow]: (http://localhost:8080)
[dashboard]: (http://localhost:5050)
[app-ml]: (http://localhost:5000)

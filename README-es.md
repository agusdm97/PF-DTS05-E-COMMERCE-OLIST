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

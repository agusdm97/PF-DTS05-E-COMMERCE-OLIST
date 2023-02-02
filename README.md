<p align="center">
  <img src="etapas_del_proyecto/_src/logo_white.png" alt="Logo Data Insights">
</p>

Other languages:
[Español](README-es.md)

# PROJECT TITLE

## Introduction

## Problem

## Proposed solution

## Repository structure

This repository has an organized structure to facilitate project management. The main folders and their content are described below:

### Folder: etapas_del_proyecto

```
.
└── etapas_del_proyecto
    └── etapa_1
    └── etapa_2
    └── etapa_3

```

This folder contains reports on the progress of the project in its different stages. Each stage is contained in a folder for easy management.

### Folder: data_warehouse

```
.
└── data_warehouse
    └── apache_airflow
    └── datasets
    └── datasets_incremental
    └── etl_module
```

This folder contains everything related to the Apache Airflow implementation, the original project datasets, the datasets generated for the incremental load tests, and the ETL module developed in Python.

### Folder: dashboard

```
.
└── dashboard
    └── app
```

This folder contains the application developed in Streamlit that allows the visualization of the data.

### Folder: machine_learning

```
.
└── machine_learning
    └── app
    └── models
    └── notebooks
```

This folder contains the Python notebooks used for testing and building Machine Learning (ML) models, the generated models, and the application developed in Streamlit to test the ML models.

## Installation

The project has been developed using Docker, so the installation is simple. Follow the steps below to run the project:

1.  Clone the repository:

    ```cmd
    git clone https://github.com/agusdm97/PF-DTS05-E-COMMERCE-OLIST.git
    ```

2.  Navigate to the root folder of the project:

    ```cmd
    cd PF-DTS05-E-COMMERCE-OLIST
    ```

3.  Run the following command to run the docker containers:

        WARNING :warning:: The next step can be stressful for some computers. Please be assured
        you have enough memory and processing resources before executing this command.

    ```cmd
    docker-compose up -d
    ```

Other languages:
[Spanish](README-es.md)

<p align="center">
  <img src="etapas_del_proyecto/_src/logo_white.png" alt="Logo Data Insights">
</p>

# FINAL PROJECT E-COMMERCE OLIST

## Introduction

OList is a complete ecosystem of digital services for online sales. It's mission is to promote digital retail commerce and provide real growth opportunities to all types of companies, eliminating obstacles and helping entrepreneurs for their space on the internet.

In this context, we are entrusted with consulting and product development work based on a set of data provided by Olist. These correspond to the period of time between 2016 and 2018 and contain information related to the Sales, Logistics and Marketing Departments.

## Problem

We assume the task of converting the raw company data into valuable information for improving decision-making process, increasing the profits and the quality of the company's service.

## Proposed solution

We have implemented an automated pipeline for the ETL process. In addition, each component of the project runs as a Docker container, contributing to the scalability and portability of the system.

By using the Streamlit framework in Python, we have built a dashboard to monitor KPIs and critical aspects of the business model, helping with the decision-making process.

Additionally, to put machine learning models into operation, we have designed a web app to meet the needs in the areas of sales, marketing, and logistics. Specifically, we have implemented time series models for sales predictions, recommendation models based on content and collaborative filtering, and a regression model to estimate product delivery time.

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

    :warning: WARNING: The next step can be stressful for some computers. Please be assured
    you have enough memory and processing resources before executing this command.

    ```cmd
    docker-compose up -d
    ```

## Usage

Once the containers are working correctly you must follow the following steps:

1. Enter to MinIO and upload the datasets:

This can be achieved by entering the following link [MinIO](http://localhost:9090), you must enter with the user `root` and the password `password`. After logging in, a bucket called `airflow` has to be created and the datasets have to be loaded.

![Minio GIF](etapas_del_proyecto/_src/MinIO.gif)

2. Enter to Airflow and activate the DAG:

This can be achieved by entering the following link [Airflow](http://localhost:8080), you must enter with the user `root` and the password `password`. After entering, you have to enter the DAG called `initial_load` and activate it.

![Airflow GIF](etapas_del_proyecto/_src/Airflow.gif)

3. Enter to the Dashboard and the Machine Learning app:

Once the previous step is finished, you can access the [Dashboard](http://localhost:5050) to view the data and the [App-ML](http://localhost:5000) to explore the ML models.

![HenryLogo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)

### PROYECTO FINAL - OLIST E-COMMERCE

## FASE 1

### TABLA DE CONTENIDO

1. Entendimiento de la situación
2. Objetivos
3. Alcances
4. Objetivos y KPIs asociados (planteo)
5. Repositorio Github
6. Solución propuesta

### 1. ENTENDIMIENTO DE LA SITUACION

**“Para entender hay que conocer”**.

OList  es un ecosistema de servicios digitales para ventas online. La principal necesidad de los vendedores es clara: **Como vender más, mejor y atraer nuevos clientes?** Por esta razón la misión de Olist es:

**“Nacimos para potenciar el comercio minorista digital y brindar oportunidades reales de crecimiento para pequeñas, medianas y grandes empresas. Existimos para eliminar obstáculos y ayudar a los minoristas a vender más. Derribamos barreras y transformamos lo presencial en online, acelerando los resultados para todos los emprendedores que buscan su espacio en internet”.**

En este contexto, se nos encomienda realizar labores de consultoría con productos entregables basados en un conjunto de datos suministrados por Olist. Estos corresponden al periodo de tiempo que transcurre entre los años 2016 al 2018 y contienen información relativa a los Departamentos de Ventas, de Logística y de Marketing.

<img src="../src/Olist1.png"  height="200">

### 2. OBJETIVOS DEL PROYECTO

**Objetivos Generales**:

1. Realizar un proceso de Extracción, Transformación y Carga (ETL) de la información relativa al negocio de la plataforma OLIST para la elaboración y análisis de KPI's y métricas que proporcionen información relevante para la toma de decisiones basada en inteligencia de negocios

2. Implementar y desplegar modelos de Machine Learning que sirvan de ayuda en análisis predictivos o prescriptivos a los participantes del modelo de negocio de OLIST

**Objetivos Especificos:**

1.1) Elaborar un completo análisis exploratorio y arquitectura de datos adecuada, proporcionando los insumos necesarios para la implementación de distintas herramientas como dashboards, algoritmos o modelos de machine learning.

1.2) Construir un modelo de visualización analítica que permita sistematizar y monitorear los distintos KPI's y métricas relevantes, asi como encontrar patrones e insights, mejorando la inteligencia de negocios.

2.1) Implementar un modelo de recomendación para compradores considerando sus preferencias históricas y de usuarios con perfiles similares

2.2) Implementar un modelo de predicción de las ventas considerando la evolución histórica de las mismas.


<img src="../src/objetivos.jpg"  height="300">

### 3. ALCANCES

En los datasets de Marketplace de e-commerce Olist se realizará un análisis exploratorio de los datos a través del uso de Python para determinar el contenido, estado y uso de los features relevantes que serán utilizados.

El proyecto abarca cuatro (4) fases que contienen específicamente el contenido y pasos a desarrollar.

**En la Fase 1**: se definen los objetivos, alcances, repositorio del proyecto y una solución al problema. En esta fase utilizaremos metodologías de desarrollo colaborativo, tecnologías e interfaces a utilizar, diseño de entregables, cronograma de tiempos, roles y responsabilidades de cada uno de los integrantes.

**En la Fase 2**: corresponde al proceso de Data Enginner en el que se inicia la infraestructura del proyecto. En esta fase realizaremos el modelado de los datos, procedimiento de ETL (Extract, Transform, Load), normalización de los features, se define la estructura de data warehouse, la automatización y validación de los datos. Además de la documentación de ello.

**En la Fase 3**: Corresponde al proceso de Data Analytics y Machine Learning (ML) en el que se desarrollara el mockup de visualización, inclusión de métricas, la definición y pruebas de modelos de ML asi como también la preparación del storytelling del proyecto.

**En la Fase 4**: Es la entrega final del Dashboard definitivo y preparación del storytelling del proyecto. Se repasan y realizan los ajustes y pruebas de ello. Además de organizar y actualizar el repositorio y la documentación correspondiente.

### KPIs

- #### Variación porcentual del volumen de ventas por mes (VVV)

  - **Área:** Ventas
    - **Objetivo:** Evaluar aumento o disminucion de la variación porcentual del volumen de ventas por mes
    - **Variables:**
      - $V_{actual}$ = volumen de ventas mes actual
      - $V_{anterior}$ = volumen de vental mes anterior

- **Fórmula:** $$VVV=\frac{V_{actual}-V_{anterior}}{V_{anterior}}\times 100 $$

  - **Frecuencia de evaluación:** Mensual
  - **Unidad:** Porcetaje [%]
  - **Valor objetivo:** 2 %

- #### Puntuación neta del promotor (PN)

  - **Área:** Ventas
    - **Objetivo:** Medir la satisfacción del cliente
    - **Variables:**
      - Porcentaje de calificaciones positivas (> 3 estrellas)
      - Porcentaje de calificaciones negativas (< 3 estrellas)
    - **Fórmula:** $$PN={{ \%}\ calificaciones\ positivas} - {{ \%}\ calificaciones\ negativas}$$
    - **Frecuencia de evaluación:** Mensual
    - **Unidad:** Porcentaje [%]
    - **Valor objetivo:** 30 [%]

- #### Fidelidad del cliente (FC)

  - **Área:** Ventas
    - **Objetivo:** Medir la tasa de clientes que vuelven a comprar dentro de un periodo determinado
    - **Variables:**
      - N° de clientes que volvieron a realizar compras
      - N° total de clientes
    - **Fórmula:** $$FC =\frac{N°\ de\ clientes\ que\ volvieron\ a\ comprar}{N°\ total\ de\ compra}\times 100$$
    - **Frecuencia de evaluación:** Trimestral
    - **Unidad:** [%]
    - **Valor objetivo:** 30 [%]

- #### Tasa de conversión (TC)

  - **Área:** Marketing
    - **Objetivo:** Medir la tasa de vendedores potenciales que se unen a la empresa
    - **Variables:**
      - $N°_{convertidos}$ = Número total de contactos convertidos
      - $N°_{interesados}$ = Número de contactos interesados
    - **Fórmula:** $$ TC=\left(\frac{N°_{convertidos}}{N°_{interesados}}\right)\times 100$$
    - **Frecuencia de evaluación:** Trimestral
    - **Unidad:** [%]
    - **Valor objetivo:** 15 [%]

- #### Puntualidad de la entrega (PE)

  - **Área:** Logistica
  - **Objetivo:** Medir el porcentaje de entregas que se realizan a tiempo en relación con el número total de entregas.
  - **Variables:**
    - $N°_{entiempo}$ = Número de entregas a tiempo
    - $N°_{entregas}$ = Número total de entregas
  - **Fórmula:** $$ PE =\left(\frac{N°_{entiempo}}{N°_{entregas}}\right)\times 100$$
  - **Frecuencia de evaluación:** Mensual
  - **Unidad:** Porcentaje [%]
  - **Valor objetivo:** 95 [%]

- #### Tiempo total del proceso (TTP)

  - **Área:** Logistica
  - **Objetivo:** Optimizar los tiempos de compra y envio.
  - **Variables:**
    - Fecha de compra
    - Fecha de recivimiento
    - Número total de compras (N)
  - **Fórmula:**  $$  TTP= \frac{1}{N}\sum_{i}^{N}\left(Fecha\ recibimiento - Fecha\ compra \right)_i  $$
  - **Frecuencia de evaluación:** Mesual
  - **Unidad:** Dias [d]
  - **Valor objetivo:** 8 [d]

- ### SOLUCIÓN Y PROPUESTA DE VALOR

**DATA WAREHOUSE:** Proporciona una arquitectura de datos unificada y actualizable en tiempo real en un esquema batch

**DASHBOARDS DINÁMICOS:** Permite un seguimiento y monitoreo de KPIs en tiempo real, generarando nuevos insights y reportes actualizados basados en inteligencia de negocios   

**SISTEMA DE RECOMENDACIÓN:** Genera ofertas de productos de interés particular para compradores, aumentando las probabilidades de ventas y retención de clientes 

**SISTEMA DE PREDICCIÓN DE VENTAS FUTURAS:** Ayuda a la gestión estratégica del negocio. Entre otras cosas permite anticiparnos al comportamiento de los consumidores, evaluar el rendimiento de los vendedores y manejar cuestiones lógisticas como el stock o inversiones inteligentes
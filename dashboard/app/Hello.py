#----LIBRERIAS--------------------------------------------------------------------------------------#
import sqlalchemy as sql
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pylab as plt
import plotly.express as px
import datetime
from PIL import Image
import altair as alt
import pymysql
import time
#------------------------------------------------------------------------------------------#
st.set_page_config(page_title="Proyecto Final - Olist", page_icon=':low_brightness:', layout="wide")
#------------------------------------------------------------------------------------------#
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')
#------------------------------------------------------------------------------------------#
# Conexion al DATAWAREHOUSE de los datos
engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"
)
emojis = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🎁", "📦","📈","📙","🖊","🧮","💳","💵"]
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
# Logo de Olist
image = Image.open('D:\PF-DTS05-E-COMMERCE-OLIST\dashboard\src\Olist1.png')
st.image(image, caption='', width=200)
#--------------------------------------------------------------------------------------#
st.title(":clipboard: Proyecto Final - Olist Dashboard") 
st.text('Sitio web para explorar la visualizacion de Dashboard')
#--------------------------------------------------------------------------------------#
# Divido en 2 columnas el texto de la consultoria y objetivo general
left_column, right_column = st.columns(2)

st.markdown('***')
with left_column:
    st.markdown(f'<p style="color:#F3FF33;font-size:32px;border-radius:2%;">Consultoría</p>', unsafe_allow_html=True)
    st.markdown('Análisis y aplicación de estrategias de Data Science a un conjunto de datasets para conocer el comportamiento general de ventas, compras, mercadeo y demás datos de interés de la plataforma')

with right_column:
    st.markdown(f'<p style="color:#F3FF33;font-size:32px;border-radius:2%;">Objetivo General</p>', unsafe_allow_html=True)
    st.markdown('Realizar un proceso de Extracción, Transformación y Carga (ETL) de la información relativa a la actividad de la plataforma OLIST para la elaboración y análisis de KPIs y métricas que proporcionen información relevante para la toma de decisiones basada en inteligencia de negocios')

#-------------------POR EL MOMENTO NO SE VA A MOSTRAR---------------------------------#
#Video de Olist
st.header('Que es Olist?')
video_file = open('D:\PF-DTS05-E-COMMERCE-OLIST\dashboard\src\Olist.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

#--------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
# CARGA DE DATASET A DATAFRAME
st.sidebar.title('Navegador de Opciones')
uploaded_file = st.sidebar.file_uploader('Cargue su DATASET aqui(Opcional)')

if uploaded_file:
    dataset = pd.read_csv(uploaded_file)
#--------------------------------------------------------------------------------------#
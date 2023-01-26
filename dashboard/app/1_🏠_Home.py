import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")


st.write("# Title")

st.sidebar.header("Home")
st.sidebar.write("BIENVENIDOS")

image = Image.open('dashboard\src\Olist1.png')
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

# Que es Olist (Video)
st.header('Que es Olist?')
video_file = open('D:\PF-DTS05-E-COMMERCE-OLIST\dashboard\src\Olist.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

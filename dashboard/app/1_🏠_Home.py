import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")


st.sidebar.header("Home")
st.sidebar.write("BIENVENIDOS")


st.title(":clipboard: Proyecto Final - Olist Dashboard")

left_column, right_column = st.columns(2)

st.markdown("---")

with left_column:
    st.markdown("### Consultoría")
    st.markdown(
        "Análisis y aplicación de estrategias de Data Science a un conjunto de datasets para conocer el comportamiento general de ventas, compras, mercadeo y demás datos de interés de la plataforma"
    )

with right_column:
    st.markdown("### Objetivo General")
    st.markdown(
        "Realizar un proceso de Extracción, Transformación y Carga (ETL) de la información relativa a la actividad de la plataforma OLIST para la elaboración y análisis de KPIs y métricas que proporcionen información relevante para la toma de decisiones basada en inteligencia de negocios"
    )


st.header("Que es Olist?")
video_file = open("src/Olist.mp4", "rb")
video_bytes = video_file.read()

st.video(video_bytes)

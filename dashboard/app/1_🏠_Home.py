import streamlit as st

st.set_page_config(page_title="Home", page_icon="馃彔", layout="wide")


st.sidebar.header("Home")
st.sidebar.write("BIENVENIDOS")


st.title(":clipboard: Proyecto Final - Olist Dashboard")

left_column, right_column = st.columns(2)

st.markdown("---")

with left_column:
    st.markdown("### Consultor铆a")
    st.markdown(
        "An谩lisis y aplicaci贸n de estrategias de Data Science a un conjunto de datasets para conocer el comportamiento general de ventas, compras, mercadeo y dem谩s datos de inter茅s de la plataforma"
    )

with right_column:
    st.markdown("### Objetivo General")
    st.markdown(
        "Realizar un proceso de Extracci贸n, Transformaci贸n y Carga (ETL) de la informaci贸n relativa a la actividad de la plataforma OLIST para la elaboraci贸n y an谩lisis de KPIs y m茅tricas que proporcionen informaci贸n relevante para la toma de decisiones basada en inteligencia de negocios"
    )


st.header("Que es Olist?")
video_file = open("src/Olist.mp4", "rb")
video_bytes = video_file.read()

st.video(video_bytes)

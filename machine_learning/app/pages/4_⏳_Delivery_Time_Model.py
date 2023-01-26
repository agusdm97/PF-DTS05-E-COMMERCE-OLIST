import streamlit as st
import pandas as pd
import pickle as pkl
from datetime import date, datetime
from xgboost.sklearn import XGBRegressor

st.header("4.-Delivery Time Model")

zip_comprador = st.text_input("Zip code del comprador")
if type(zip_comprador) != str:
    st.write("El valor ingresado no es un número entero")
zip_vendedor = st.text_input("Zip code del vendedor")
dia_compra = st.date_input("Día en la que realizó la compra")
fecha_completa = datetime.combine(dia_compra, datetime.min.time())
timestamp = fecha_completa.timestamp()
flete = st.text_input("Valor del flete")
peso = st.text_input("Peso del producto")

st.write(timestamp)

list = pd.DataFrame(
    [[zip_comprador], [zip_comprador], [timestamp], [flete], [peso]]
).transpose()
list.rename(
    columns={
        0: "zip_comprador",
        1: "zip_vendedor",
        2: "dia_compra",
        3: "flete",
        4: "peso",
    },
    inplace=True,
)


def dias_espera(datos):
    modelo = pd.read_pickle("app/dias_espera.pkl")
    pred = modelo.predict(datos)
    return pred


btn = st.button("predict")

if btn:
    st.write(dias_espera(list))

import streamlit as st
import pandas as pd
import pickle as pkl
from datetime import date, datetime
from xgboost.sklearn import XGBRegressor

st.header("4.-Delivery Time Model")

st.write(
    """Este modelo tiene por finalidad estimar la cantidad de días de espera que tomará en llegar 
un producto, contados a partir de que el cliente lo compra."""
)
st.write("""Ingrese los siguientes valores para calcular:""")
# st.write("* Zip Code del comprador: número entero")
# st.write("* Zip Code del vendedor: número entero")
# st.write("* Día en la que realizó la compra: Seleccione la fecha en formato AAAA/MM/DD")
# st.write("* Valor del flete: numero decimal")
# st.write("* Peso del producto: el peso en gramos (numero entero)")


zip_comprador = st.number_input("Zip code del comprador", value=1000)
# st.write(type(zip_comprador))

zip_vendedor = st.number_input("Zip code del vendedor", value=1000)
# st.write(type(zip_vendedor))

dia_compra = st.date_input("Día en la que realizó la compra")
fecha_completa = datetime.combine(dia_compra, datetime.min.time())
timestamp = fecha_completa.timestamp()

flete = st.number_input("Valor del flete")
# st.write(type(flete))

peso = st.number_input("Peso del producto", value=1)
# st.write(type(peso))
# st.write(timestamp)

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

# st.write("Los valores ingresados son: \n", list)


def dias_espera(datos):
    modelo = pd.read_pickle("app/dias_espera.pkl")
    pred = modelo.predict(datos)
    # pred.rename(columns={0: "Predicción [días]"}, inpace=True)
    return pred[0]


btn = st.button("Evaluar días para entrega")

if btn:
    st.write(f"### El tiempo de espera del producto será {int(dias_espera(list))} días")

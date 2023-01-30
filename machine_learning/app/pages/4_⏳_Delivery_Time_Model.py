import streamlit as st
import pandas as pd
import pickle as pkl
import sqlalchemy as sql
from datetime import date, datetime
from xgboost.sklearn import XGBRegressor

st.header("4.-Delivery Time Model")

engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

DF = pd.read_sql(
    "SELECT zip_code, latitude, longitude FROM data_warehouse_olist.geolocations;",
    con=engine,
)

st.write(
    """Este modelo tiene por finalidad estimar la cantidad de días de espera que tomará en llegar 
un producto, contados a partir de que el cliente lo compra."""
)
st.write("""Ingrese los siguientes valores para calcular:""")


zip_comprador = st.number_input("Zip code del comprador", min_value=1001, value=1001)
# Filtering the dataframe DF by zip_code and then getting the latitude and longitude of the zip code.
filtro_comprador = DF["zip_code"] == zip_comprador
lat_comp = DF[filtro_comprador]["latitude"].values[0]
long_comp = DF[filtro_comprador]["longitude"].values[0]

# Test mode
# st.write(lat_comp)
# st.write(type(lat_comp))
# st.write(type(long_comp))

zip_vendedor = st.number_input("Zip code del vendedor", min_value=1001, value=1001)
filtro_vendedor = DF["zip_code"] == zip_vendedor
lat_vend = DF[filtro_vendedor]["latitude"].values[0]
long_vend = DF[filtro_vendedor]["longitude"].values[0]
# st.write(type(zip_vendedor))

start_date = date(2017, 12, 31)
max_date = date(2018, 12, 31)
min_date = date(2016, 6, 1)
dia_compra = st.date_input(
    "Día en la que realizó la compra",
    value=start_date,
    min_value=min_date,
    max_value=max_date,
)
fecha_completa = datetime.combine(dia_compra, datetime.min.time())
timestamp = fecha_completa.timestamp()

flete = st.number_input("Valor del flete")
# st.write(type(flete))

peso = st.number_input("Peso del producto", value=1)
# st.write(type(peso))
# st.write(timestamp)

list = pd.DataFrame(
    [[lat_comp], [long_comp], [lat_vend], [long_vend], [timestamp], [flete], [peso]]
).transpose()
list.rename(
    columns={
        0: "lat_comp",
        1: "long_comp",
        2: "lat_vend",
        3: "long_vend",
        4: "dia_compra",
        5: "flete",
        6: "peso",
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

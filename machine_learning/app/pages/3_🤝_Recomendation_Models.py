import streamlit as st
import pandas as pd

st.header("3.-Modelo de recomendación-producto")

product = st.text_input("Field 1")

btn = st.button("predict")


def recommend_products(product_id):
    df_ml = pd.read_pickle("app/recomendacion_producto.pkl")
    filtro_aux = df_ml["product_id"] == product
    categoria = df_ml[filtro_aux]["category_name"]
    group = df_ml[filtro_aux]["group"]
    filtro = (
        (df_ml["group"] == group.values[0])
        & (df_ml["category_name"] == categoria.values[0])
        & (df_ml["product_id"] != product)
    )
    df = df_ml[filtro].sort_values(by="ventas_producto", ascending=False)
    return df.head(3)


if btn:
    st.write(recommend_products(product).head(3))

import streamlit as st
import pandas as pd

st.title("Modelos de recomendación")

st.header("1.- Modelo de recomendación. Producto-Producto.")

st.write("""Este modelo tiene por finalidad recomendar artículos similares a un producto determinado. 
Utiliza un filtro de contenido teniendo en cuenta las carácteristicas del producto y es especialmente 
útil para solucionar el problema de 'arranque en frío', es decir, 
cuando no se tienen suficientes datos del usuario para realizar un filtro colaborativo eficiente. """)

st.write('Puedes:')

product = st.text_input("Ingresar un producto.")


product = st.selectbox('Elegir un producto', 
['00066f42aeeb9f3007548bb9d3f33c38', '00088930e925c41fd95ebfe695fd2655', '0009406fd7479715e4bef61dd91f2462', '000b8f95fcb9e0096488278317764d19'])


btn = st.button("Recomendar")

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



st.header("2.- Modelo de recomendación. Usuario-Producto.")

st.write("""Este modelo tiene por finalidad recomendar artículos teniendo en cuenta el perfil de un usuario determinado. 
Utiliza un filtro colaborativo basado en los antecedentes y preferencias de un cliente en específico, luego los compara con perfiles similares
 y por último, con esa información realiza las recomendaciones de los productos. Este sistema es ideal, cuando se cuenta con una base de datos robusta, porque permite 
 hacer recomendaciones personalizadas a los clientes. """)

usuario = st.text_input("Ingrese el id del usuario.")

st.write('Puedes:')

product = st.text_input("Ingresar un usuario.")


product = st.selectbox('Elegir un usuario', 
['432aa6200ee9673be90863a912dc91dc', 'fd8ccc89be43894d2553494c71a61fd8', 'dd8c09f1b309c9ffc302c745550a9ff3', 'dd8c09f1b309c9ffc302c745550a9ff3'])

btn2 = st.button("Predecir") 

if btn2:
    st.write('falta la funcion aqui')
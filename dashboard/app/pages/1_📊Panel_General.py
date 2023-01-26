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

st.set_page_config(page_title="Panel General", page_icon=":📈", layout="wide")
st.sidebar.header("Panel General")

my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')

status_text = st.sidebar.empty()
#------------------------------------------------------------------------------------------#
# Conexion al DATAWAREHOUSE de los datos
engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"
)

#------------------------------------------------------------------------------------------#
dataset = pd.read_sql('order_items', con=engine)
dataset4 = pd.read_sql('products', con=engine)
dataset6 = pd.read_sql('customers', con=engine)


st.title(':mag_right: Visualizacion de Datos Generales')
st.text('A continuación se observara los resultados del análisis')
st.markdown('***')
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           1. parte de la visualizacion
#               - Total ingresos mas el flete
#               - Total Flete
#               - Total ingresos
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
# Consulta del total de ingresos sumado el valor del flete
precios = round(dataset['price'].sum(), 2)
freight = round(dataset['freight_value'].sum(), 2)
total = precios + freight

#---------------------------------------------------------------------------------------#
# Cosulta de solo el total de los fletes sin ingresos
total_freight = round(dataset['freight_value'].sum(), 2)
#---------------------------------------------------------------------------------------#
# Consulta de solo el total de los ingresos sin fletes
total_ingresos = round(dataset['price'].sum(), 2)
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#

left_column, middle_column, right_column = st.columns(3)
st.markdown('***')
with left_column:
    st.subheader('Total Ingresos')
    #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
    st.markdown('<p style="color:#33ff33;font-size:24px;border-radius:2%;">Reales ${:,.2f}</p>'.format(total_ingresos), unsafe_allow_html=True)
    
with middle_column:
    st.subheader('Total Fletes')
    st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">Reales ${:,.2f}</p>'.format(total_freight), unsafe_allow_html=True)

with right_column:
    st.subheader('Total Ingresos Ventas + Flete')
    st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">Reales ${:,.2f}</p>'.format(total), unsafe_allow_html=True)
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. parte de la visualizacion
#               - Cantidad de Vendedores
#               - Cantidad de Ordenes de Venta
#               - Cantidad de Clientes
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
    # Visualizacion de la cantidad de vendedores
cant_vendedores = round(dataset['seller_id'].nunique(), 0)
#--------------------------------------------------------------------------------------#
cant_customers = round(dataset6['unique_id'].nunique(), 0)
#--------------------------------------------------------------------------------------#
# Visualizacion de la cantidad de ordenes de venta
cant_ordenes = round(dataset['order_id'].count(), 0)
#--------------------------------------------------------------------------------------#

left_column, middle_column, right_column = st.columns(3)
st.markdown('***')
with left_column:
    st.subheader('Cantidad Vendedores')
    #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
    st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_vendedores), unsafe_allow_html=True)

with middle_column:
    st.subheader('Cantidad Clientes')
    st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_customers), unsafe_allow_html=True)    

with right_column:
    st.subheader('Cantidad de Ordenes')
    st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_ordenes), unsafe_allow_html=True)

#--------------------------------------------------------------------------------------#
    # Visualizacion de la cantidad de productos
cant_productos = round(dataset4['product_id'].nunique(), 0)
#--------------------------------------------------------------------------------------#
# Visualizacion de la cantidad de productos
cant_categorias = round(dataset4['category_name'].nunique(), 0)
#--------------------------------------------------------------------------------------#

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader('Cantidad Productos')
    st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_productos), unsafe_allow_html=True)

with middle_column:
    st.markdown('')

with right_column:
    st.subheader('Cantidad Categorías')
    st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_categorias), unsafe_allow_html=True)

#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           3. Dashboard visualizacion grafica de lineas
#               - Grafica de ingresos x año
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           - Aplicacion de filtro
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
    #x_axis_val = st.selectbox('Seleccione X-Eje Value', options=ingresos_anio.columns)
    #y_axis_val = st.selectbox('Seleccione Y-Eje Value', options=ingresos_anio.columns)
    #col = st.color_picker('Seleccione color de la grafica')
    #plot = px.scatter(ingresos_anio, x=x_axis_val, y=y_axis_val)
    #plot.update_traces(marker=dict(color=col))
    #st.plotly_chart(plot)
    
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
ingresos_anio = pd.read_sql("""
    select year(o.purchase_timestamp) AS anio, sum(oi.price) as total
    from order_items oi
    JOIN orders o ON(oi.order_id = o.order_id)
    group by anio
    order by anio asc; """, con=engine)
        
st.markdown('***')
line_chart = alt.Chart(ingresos_anio).mark_line().encode(
    y =  alt.Y('total', title='Ingresos($)'),
    x =  alt.X('anio', title='Año')
    #x = x_axis_val
).properties(
    height=500, width=800,
    title="Ingresos por Año"
).configure_title(
    fontSize=16
).configure_axis(
    titleFontSize=14,
    labelFontSize=12
)
st.altair_chart(line_chart, use_container_width=True)

    #opcion = st.selectbox('Seleccione X-Eje Value', options=ingresos_anio.anio)
    #y_axis_val = st.selectbox('Seleccione Y-Eje Value', options=ingresos_anio.total)
    #col = st.color_picker('Seleccione color de la grafica')
    #plot = px.scatter(ingresos_anio, x=x_axis_val, y=y_axis_val)
    #plot = st.altair_chart(ingresos_anio, x = opcion ,use_container_width=True)
    #plot.update_traces(marker=dict(color=col))
    #st.plotly_chart(plot) 
    
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           4. Dashboard visualizacion grafica de barras
#               - Ingresos por Ciudad
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
ingresos_ciudad = pd.read_sql("""
    select g.city, sum(oi.price) as total
    from order_items oi
    JOIN orders o ON(oi.order_id = o.order_id)
    JOIN customers c ON(c.customer_id = o.customer_id )
    JOIN geolocations g ON(g.zip_code = c.zip_code)
    group by g.city
    order by total desc
    limit 20;""", con=engine)

fig_ingresos_ciudad = px.bar(
    ingresos_ciudad,
    x = 'total',
    y = 'city',
    orientation="h",
    title="Top 20 Ingresos por Ciudad",
    color_discrete_sequence=["#5EFF33"] * len(ingresos_ciudad),
    template='plotly_white',
)
fig_ingresos_ciudad.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = dict(showgrid=False)
    )
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           5. Dashboard visualizacion grafica de funnel
#               - Ingresos por Categoria de Producto
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
categoria_produ = pd.read_sql("""
    select p.category_name, sum(oi.price) as total
    from order_items oi
    JOIN products p ON(oi.product_id = p.product_id)
    group by p.category_name
    order by total desc
    limit 10""", con=engine)

temp = categoria_produ.category_name
val = round(categoria_produ['total'], 0)

fig = px.funnel(categoria_produ, 
    x = val, 
    y = temp,
    #textposition = "inside",
    title="Ingresos por Categoria",
    color_discrete_sequence=["#33E3FF"] * len(categoria_produ),
    #color = ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
    #labels=(),
    orientation="h",
    opacity = 0.65

    )
    #fig.show()
fig.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = dict(showgrid=False)
    )


left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_ingresos_ciudad, use_container_width=True)
right_column.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           6. Dashboard visualizacion grafica de pie
#               - Ingresos por estado
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
ventas_state = pd.read_sql("""
    select g.state, sum(oi.price) as total
    from order_items oi
    JOIN orders o ON(oi.order_id = o.order_id)
    JOIN customers c ON(c.customer_id = o.customer_id )
    JOIN geolocations g ON(g.zip_code = c.zip_code)
    group by g.state
    order by total desc
    limit 5; """, con=engine)

estados = ventas_state['state']
valores_state = ventas_state['total']

fig = px.pie(values=valores_state, names=estados, title='Participacion de las Ventas por Estado', color_discrete_sequence=px.colors.sequential.RdBu)
#--------------------------------------------------------------------------------------#    

left_column, middle_column, right_column = st.columns(3)

with left_column:
        st.markdown('')

with middle_column:
        st.plotly_chart(fig, use_container_width=True)

with right_column:
        st.markdown('')


st.balloons()

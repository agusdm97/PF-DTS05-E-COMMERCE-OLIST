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
#------------------------------------------------------------------------------------------#
st.set_page_config(page_title="Proyecto Final - Olist", page_icon='low_brightness:', layout="wide")
#------------------------------------------------------------------------------------------#
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[39m'

#------------------------------------------------------------------------------------------#
# Conexion al DATAWAREHOUSE de los datos
engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"
)

#------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------#
# Logo de Olist
image = Image.open('D:\PF-DTS05-E-COMMERCE-OLIST\dashboard\src\Olist1.png')
st.image(image, caption='', width=200)
#--------------------------------------------------------------------------------------#
st.title(":clipboard: Proyecto Final - Olist") 
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

#video_file = open('D:\PF-DTS05-E-COMMERCE-OLIST\dashboard\src\Olist.mp4', 'rb')
#video_bytes = video_file.read()

#st.video(video_bytes)

#--------------------------------------------------------------------------------------#
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#--------------------------------------------------------------------------------------#
# NAVEGADOR DE OPCIONES CON LA CARGA DE DATASET
st.sidebar.title('Navegador de Opciones')
uploaded_file = st.sidebar.file_uploader('Cargue su DATASET aqui(Opcional)')

options = st.sidebar.radio('Paginas', options=['Panel General', 'Sellers-Customers', 'Payments-Delivery', 'Marketing-Method Payments','Reviews', 'KPIs'
                            
])

#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
# CARGA DE DATASET A DATAFRAME

if uploaded_file:
    dataset = pd.read_csv(uploaded_file)
#--------------------------------------------------------------------------------------#
#st.subheader('Dataset de Análisis')
dataset = pd.read_sql('order_items', con=engine)
dataset1 = pd.read_sql('orders', con=engine)
dataset2 = pd.read_sql('order_payments', con=engine)
dataset3 = pd.read_sql('order_reviews', con=engine)
dataset4 = pd.read_sql('products', con=engine)
dataset5 = pd.read_sql('sellers', con=engine)
dataset6 = pd.read_sql('customers', con=engine)
dataset7 = pd.read_sql('closed_deals', con=engine)
dataset8 = pd.read_sql('marketing_qualified_leads', con=engine)
dataset9 = pd.read_sql('geolocations', con=engine)



#dataset = pd.read_csv('Datasets/ventas_ejemplo2.csv', sep = ',', encoding = 'utf_8')
#st.dataframe(dataset) # visualiza el dataframe
#filter = (dataset[['country','price']].groupby(['country']).mean().sort_values(by='price', ascending=False))
#filter
st.header('Visualizacion de Dashboard')
st.text('A continuación se observara los resultados del análisis')
st.markdown('***')
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           1. Area de consultaS a la base de datos
#               - Ingresos por año
#               - Ingresos por ciudad
#               - Categorizacion de productos x ingresos
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
ingresos_anio = pd.read_sql('select c.anio, sum(oi.price) as total from order_items oi JOIN orders o ON(oi.order_id = o.id) JOIN calendario c ON(c.Fecha = o.purchase_timestamp) group by c.anio ;', con=engine)
#--------------------------------------------------------------------------------------#
ingresos_ciudad = pd.read_sql('select g.city, sum(oi.price) as total from order_items oi JOIN orders o ON(oi.order_id = o.id) JOIN customers c ON(c.id = o.customer_id ) JOIN geolocations g ON(g.zip_code = c.zip_code) group by g.city order by total desc limit 20', con=engine)
#--------------------------------------------------------------------------------------#
categoria_produ = pd.read_sql('select p.category_name, sum(oi.price) as total from order_items oi JOIN products p ON(oi.product_id = p.id) group by p.category_name order by total desc limit 10 ;', con=engine)
temp = categoria_produ.category_name
val = round(categoria_produ['total'], 0)
#--------------------------------------------------------------------------------------#
# Visualizacion del total de ingresos sumado el valor del flete
precios = round(dataset['price'].sum(), 2)
freight = round(dataset['freight_value'].sum(), 2)
total = precios + freight

#---------------------------------------------------------------------------------------#
# Visualizacion de solo el total de los fletes sin ingresos
total_freight = round(dataset['freight_value'].sum(), 2)
#---------------------------------------------------------------------------------------#
# Visualizacion de solo el total de los ingresos sin fletes
total_ingresos = round(dataset['price'].sum(), 2)
#---------------------------------------------------------------------------------------#
# Visualizacion de la cantidad de vendedores
cant_vendedores = round(dataset['seller_id'].nunique(), 0)
#--------------------------------------------------------------------------------------#
cant_customers = round(dataset6['unique_id'].nunique(), 0)

#--------------------------------------------------------------------------------------#
# Visualizacion de la cantidad de ordenes de venta
cant_ordenes = round(dataset['order_id'].count(), 0)
#--------------------------------------------------------------------------------------#
# Visualizacion de la cantidad de productos
cant_productos = round(dataset4['id'].nunique(), 0)
#--------------------------------------------------------------------------------------#
# Visualizacion de la cantidad de productos
cant_categorias = round(dataset4['category_name'].nunique(), 0)
#--------------------------------------------------------------------------------------#
vendedores_state = pd.read_sql('select g.latitude, g.longitude, g.state, sum(oi.price) as total from order_items oi JOIN sellers s ON(s.id = oi.seller_id) JOIN geolocations g ON(s.zip_code = g.zip_code) group by g.latitude, g.longitude, g.state order by total desc ;', con=engine)
latitude = vendedores_state['latitude']
longitude = vendedores_state['longitude']
state = vendedores_state['state']
total_vend = vendedores_state['total']
#--------------------------------------------------------------------------------------#
ventas_state = pd.read_sql('select g.state, sum(oi.price) as total from order_items oi JOIN orders o ON(oi.order_id = o.id) JOIN customers c ON(c.id = o.customer_id ) JOIN geolocations g ON(g.zip_code = c.zip_code) group by g.state order by total desc limit 5 ;', con=engine)
estados = ventas_state['state']
valores_state = ventas_state['total']
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. KPIs
#               - Variación porcentual del volumen de ventas por mes
#               - 
#               - Total Flete
#               - Total ingresos
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. KPI
#           A. Variación porcentual del volumen de ventas por mes
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
kpi_variacionVentas = pd.read_sql('SELECT s.purchase_timestamp AS fecha, sum(s.total) AS total FROM (SELECT o.purchase_timestamp, sum(i.price) AS total FROM orders AS o RIGHT JOIN order_items AS i ON (o.id = i.order_id) WHERE o.status != "canceled" AND o.status != "unavailable" GROUP BY o.id ) AS s GROUP BY year(s.purchase_timestamp), month(s.purchase_timestamp) HAVING year(s.purchase_timestamp) = 2017 order by fecha asc ;', con=engine)
kpi_variacionVentas['dif_perc'] = kpi_variacionVentas['price'].pct_change()
kpi_variacionVentas['dif_perc'].map(lambda x:format(x,'.2%'))





#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. parte de la visualizacion
#               - Total ingresos mas el flete
#               - Total Flete
#               - Total ingresos
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
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
#           3. parte de la visualizacion
#               - Cantidad de Vendedores
#               - Cantidad de Ordenes de Venta
#                - Cantidad de Clientes
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
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
#           4. Dashboard visualizacion grafica de lineas
#               - Grafica de ingresos x año
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
st.markdown('***')
line_chart = alt.Chart(ingresos_anio).mark_line().encode(
        y =  alt.Y('total', title='Ingresos($)'),
        x =  alt.X('anio', title='Año')
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
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           5. Dashboard visualizacion grafica de barras
#               - Ingresos por Ciudad
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
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
#           6. Dashboard visualizacion grafica de funnel
#               - Ingresos por Categoria de Producto
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------#
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
#--------------------------------------------------------------------------------------#
#           7. Dashboard visualizacion grafica de shatter
#               - Ingresos por Categoria de Producto
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
# -- Create three columns
col1, col2, col3 = st.columns([5, 5, 20])
# -- Put the image in the middle column
# - Commented out here so that the file will run without having the image downloaded
# with col2:
# st.image("streamlit.png", width=200)
# -- Put the title in the last column
with col3:
    st.title("Streamlit Demo")
# -- We use the first column here as a dummy to add a space to the left
# -- Get the user input
year_col, continent_col, log_x_col = st.columns([5, 5, 5])
with year_col:
    year_choice = st.slider(
        "What year would you like to examine?",
        min_value=1952,
        max_value=2007,
        step=5,
        value=2007,
    )
with continent_col:
    continent_choice = st.selectbox(
        "What continent would you like to look at?",
        ("All", "Asia", "Europe", "Africa", "Americas", "Oceania"),
    )
with log_x_col:
    log_x_choice = st.checkbox("Log X Axis?")

# -- Read in the data

df = px.data.gapminder()
# -- Apply the year filter given by the user
filtered_df = df[(df.year == year_choice)]
# -- Apply the continent filter
if continent_choice != "All":
    filtered_df = filtered_df[filtered_df.continent == continent_choice]

# -- Create the figure in Plotly
fig = px.scatter(
    filtered_df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=log_x_choice,
    size_max=60,
)
fig.update_layout(title="GDP per Capita vs. Life Expectancy")
# -- Input the Plotly chart to the Streamlit interface
st.plotly_chart(fig, use_container_width=True)



#-------------------------------------------------------------------------------------#
x_axis_val = st.selectbox('Seleccione X-Eje Value', options=ingresos_anio.columns)
y_axis_val = st.selectbox('Seleccione Y-Eje Value', options=ingresos_anio.columns)
col = st.color_picker('Seleccione color de la grafica')
plot = px.scatter(ingresos_anio, x=x_axis_val, y=y_axis_val)
plot.update_traces(marker=dict(color=col))
st.plotly_chart(plot)
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           8. Dashboard visualizacion grafica de pie
#               - Ingresos por estado
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
 
fig = px.pie(values=valores_state, names=estados, title='Participacion de las Ventas por Estado', color_discrete_sequence=px.colors.sequential.RdBu)
fig.show()



#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
# FUNCIONES PRINCIPALES
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           7. Funciones que visualizan el NAVEGADOR de Opciones
#               - Ventas
#               - Productos
#               - Vendedores
#               - Clientes
#               - Marketing
#               - Metodos de pago
#               - Reviews
#               - Delivery
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
@st.cache(persist = True)
def Ventas(dataset):
    st.header('Dataset')
    #st.dataframe(dataset)
    precios_promedio = (dataset.groupby(by=['Nombres']).sum()[['Facturado']].sort_values(by='Facturado'))
    fig_precios_promedio = px.bar(
        precios_promedio,
        x = 'Facturado',
        y = precios_promedio.index,
        orientation="h",
        title="Ventas Vendedor",
        color_discrete_sequence=["#f5b932"] * len(precios_promedio),
        template='plotly_white',
    )
    fig_precios_promedio.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
    )

    vendedor_presupuesto = (dataset.groupby(by=['Nombres']).sum()[['Presupuesto']].sort_values(by='Presupuesto'))
    fig_vendedor_presupuesto = px.bar(
        vendedor_presupuesto,
        x = vendedor_presupuesto.index,
        y = 'Presupuesto',
        orientation="h",
        title="Presupuesto vendedor",
        color_discrete_sequence=["#f6b960"] * len(vendedor_presupuesto),
        template='plotly_white',
    )
    fig_vendedor_presupuesto.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
    )

    

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_precios_promedio, use_container_width=True)
    right_column.plotly_chart(fig, use_container_width=True)
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           4. Opcion de Productos
#               - Ventas
#               - Productos
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#

def Productos(categoria_produ):
    st.header('PRODUCTOS(Products)')
    #categoria_produ = pd.read_sql('select p.category_name, sum(oi.price) as total from order_items oi JOIN products p ON(oi.product_id = p.id) group by p.category_name order by total desc limit 20 ;', con=engine)
    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.subheader('Cantidad Productos')
        st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_productos), unsafe_allow_html=True)

    with middle_column:
        st.markdown('')

    with right_column:
        st.subheader('Cantidad Categorías')
        st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_categorias), unsafe_allow_html=True)


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
    left_column.plotly_chart(fig, use_container_width=True)
   
#------------------------------------------------------------------------------#
def Vendedores(categoria_produ):
    st.header('VENDEDORES(Seller)')
    #categoria_produ = pd.read_sql('select p.category_name, sum(oi.price) as total from order_items oi JOIN products p ON(oi.product_id = p.id) group by p.category_name order by total desc limit 20 ;', con=engine)
    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.subheader('Cantidad Productos')
        st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_productos), unsafe_allow_html=True)

    with middle_column:
        st.markdown('')

    with right_column:
        st.subheader('Cantidad Categorías')
        st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(cant_categorias), unsafe_allow_html=True)


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
    left_column.plotly_chart(fig, use_container_width=True)  


#-------------------------------------------------------------------------------#
@st.cache
def stats(dataset):
    st.header('Data Statistics')
    st.write(dataset.describe())
#-------------------------------------------------------------------------------#
@st.cache
def data_header(dataset):
    st.header('Data Header')
    st.write(dataset.head(10))
#-------------------------------------------------------------------------------#
@st.cache
def plot(dataset):
    fig, ax=plt.subplot(1,1)
    ax.scatter(x=dataset['country'], y=dataset['points'])
    ax.set_xlabel('pais')
    ax.set_ylabel('puntos')
    st.pyplot(fig)
#-------------------------------------------------------------------------------#
@st.cache
def lines():
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
    st.line_chart(chart_data)
#-------------------------------------------------------------------------------#

def lines1():
    line_chart = alt.Chart(dataset).mark_line().encode(
        y =  alt.Y('Facturado', title='Precios($)'),
        x =  alt.X( 'Fecha', title='Pais')
    ).properties(
        height=500, width=800,
        title="Vinos del Mundo"
    ).configure_title(
        fontSize=16
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
 
    st.altair_chart(line_chart, use_container_width=True)

#-------------------------------------------------------------------------------#
@st.cache
def interactive_plot(dataset):
    x_axis_val = st.selectbox('Seleccione X-Eje Value', options=dataset.columns)
    y_axis_val = st.selectbox('Seleccione Y-Eje Value', options=dataset.columns)
    col = st.color_picker('Seleccione color de la grafica')
    plot = px.scatter(dataset, x=x_axis_val, y=y_axis_val)
    plot.update_traces(marker=dict(color=col))
    st.plotly_chart(plot)
#-------------------------------------------------------------------------------#
def barras():
    st.subheader('Grafico de Barras')
    source = (dataset)
    bar_chart = alt.Chart(source).mark_bar().encode(
        y = 'Facturado',
        x = 'Nombres',
    )
    st.altair_chart(bar_chart, use_container_width=True)

#-------------------------------------------------------------------------------#
def kpi():
    st.header('KPIs')
    

    left_column, middle_colum, right_column = st.columns(3)

    st.markdown('***')
    with left_column:
        st.header('KPI Venta Agrupada por mes 2017')
        st.dataframe(kpi_variacionVentas)

    with middle_colum:
        st.header('Venta Total')
        st.dataframe(kpi_variacionVentas)

    with right_column:
        st.header('Presupuesto Total')
        {total_presupuesto}


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


#{"Pelis":int(peliculas), "Series":int(series)}

#--------------------------------------------------------------------------------------#
# AREA DE OPCIONES PARA EJECUTAR LAS FUNCIONALIDADES y DE NAVEGACION
if options == 'Ventas':
    st.text('Podemos Observar el Dataset')
    Ventas(dataset)
elif options == 'Productos':
    st.text('Visualizacion de Graficas')
    Productos(categoria_produ)
elif options == 'Vendedores':
    st.text('Visualizacion de Graficas')
    Vendedores()
elif options == 'Data Header':
    st.text('Despliegue de los primeros 10 registros')
    data_header(dataset)
elif options == 'plot':
    st.text('Grafico de puntos')
    plot(dataset)
elif options == 'lineas':
    st.text('Grafico de lineas')
    lines()
elif options == 'Grafica Interactiva':
    st.text('Grafico Interactivo')
    interactive_plot(dataset)
elif options == 'Barras':
    st.text('Grafico de Barras')
    barras()
elif options == 'Lineas':
    st.text('Grafico de Lineas')
    lines1()
elif options == 'KPIs':
    st.text('Muestra KPI')
    kpi()

#--------------------------------------------------------------------------------------#





#------------------------------------------------------------------------------------------#
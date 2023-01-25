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

#-------------------POR EL MOMENTO NO SE VA A MOSTRAR---------------------------------#
#Video de Olist
st.header('Que es Olist?')
video_file = open('D:\PF-DTS05-E-COMMERCE-OLIST\dashboard\src\Olist.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

#--------------------------------------------------------------------------------------#
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#--------------------------------------------------------------------------------------#
# NAVEGADOR DE OPCIONES CON LA CARGA DE DATASET
st.sidebar.title('Navegador de Opciones')
uploaded_file = st.sidebar.file_uploader('Cargue su DATASET aqui(Opcional)')

options = st.sidebar.radio('Paginas', options=['Home', 'Panel General', 'Sellers-Customers', 'Method Payments-Delivery', 'Marketing-Reviews', 'KPIs'
                            
])

#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
# CARGA DE DATASET A DATAFRAME

if uploaded_file:
    dataset = pd.read_csv(uploaded_file)
#--------------------------------------------------------------------------------------#
#st.subheader('Dataset de Análisis')
dataset = pd.read_sql('order_items', con=engine)
#dataset1 = pd.read_sql('orders', con=engine)
#dataset2 = pd.read_sql('order_payments', con=engine)
#dataset3 = pd.read_sql('order_reviews', con=engine)
dataset4 = pd.read_sql('products', con=engine)
#dataset5 = pd.read_sql('sellers', con=engine)
dataset6 = pd.read_sql('customers', con=engine)
#dataset7 = pd.read_sql('closed_deals', con=engine)
#dataset8 = pd.read_sql('marketing_qualified_leads', con=engine)
#dataset9 = pd.read_sql('geolocations', con=engine)



#dataset = pd.read_csv('Datasets/ventas_ejemplo2.csv', sep = ',', encoding = 'utf_8')
#st.dataframe(dataset) # visualiza el dataframe
#filter = (dataset[['country','price']].groupby(['country']).mean().sort_values(by='price', ascending=False))
#filter
#st.header('Visualizacion de Dashboard')
#st.text('A continuación se observara los resultados del análisis')
st.markdown('***')
#--------------------------------------------------------------------------------------#
#              1.CONSULTAS GENERALES          
#               - Area de consultaS a la base de datos
#               - Ingresos por año
#               - Ingresos por ciudad
#               - Categorizacion de productos x ingresos
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
ingresos_anio = pd.read_sql("""
    select year(o.purchase_timestamp) AS anio, sum(oi.price) as total
    from order_items oi
    JOIN orders o ON(oi.order_id = o.order_id)
    group by anio;""", con=engine)

categoria_produ = pd.read_sql("""
    select p.category_name, sum(oi.price) as total
    from order_items oi
    JOIN products p ON(oi.product_id = p.product_id)
    group by p.category_name
    order by total desc
    limit 10""", con=engine)

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
cant_productos = round(dataset4['product_id'].nunique(), 0)
#--------------------------------------------------------------------------------------#
# Visualizacion de la cantidad de productos
cant_categorias = round(dataset4['category_name'].nunique(), 0)
#--------------------------------------------------------------------------------------#
vendedores_state = pd.read_sql("""
    select g.latitude, g.longitude, g.state, sum(oi.price) as total
    from order_items oi
    JOIN sellers s ON(s.seller_id = oi.seller_id) 
    JOIN geolocations g ON(s.zip_code = g.zip_code)
    group by g.latitude, g.longitude, g.state
    order by total desc;""", con=engine)

latitude = vendedores_state['latitude']
longitude = vendedores_state['longitude']
state = vendedores_state['state']
total_vend = vendedores_state['total']
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
#--------------------------PENDIENTE POR DEFINIR GRAFICA-------------------------------#
ingresos_ST_ciudad = pd.read_sql("""
    select g.latitude, g.longitude, g.state, g.city, sum(oi.price) as ventas
    from order_items oi
    JOIN sellers s ON(s.seller_id = oi.seller_id)
    JOIN geolocations g ON(s.zip_code = g.zip_code)
    group by g.latitude, g.longitude, g.state
    order by ventas desc
    limit 20;""", con=engine)
#--------------------------------------------------------------------------------------#
clientes_estado = pd.read_sql("""
    select g.state, count(c.customer_id) as nclientes
    from customers c
    JOIN geolocations g ON(c.zip_code = g.zip_code)
    group by g.state
    order by nclientes desc
    limit 10;""", con=engine)

#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
vendedores_estado = pd.read_sql("""
    select g.state, count(s.seller_id) as nvendedores
    from sellers s
    JOIN geolocations g ON(s.zip_code = g.zip_code)
    group by g.state
    order by nvendedores desc
    limit 10;""", con=engine)
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
ordenes_mes = pd.read_sql("""
    select month(o.approved_at) as mes, sum(oi.price) as ingresos
    from order_items oi
    JOIN orders o ON(oi.order_id = o.order_id)
    group by mes
    order by mes;""", con=engine)
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
relacion_status = pd.read_sql("""
    select year(purchase_timestamp) as anio, status, count(status) as total
    from orders
    where status = 'delivered' or status='canceled' or status='unavailable'
    group by anio, status;""", con=engine)
estatus = relacion_status['status']
valores = relacion_status['total']

#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
method_payment = pd.read_sql("""
    select op.type, count(*) as total
    from order_payments op
    group by op.type
    order by total desc;""", con=engine)

tipo = method_payment['type']
cantidad = method_payment['total']
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#


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
kpi_variacionVentas = pd.read_sql(""" 
    SELECT s.purchase_timestamp AS fecha, sum(s.total) AS total
    FROM (
        SELECT o.purchase_timestamp, sum(i.price) AS total
        FROM orders AS o
        RIGHT JOIN order_items AS i ON (o.order_id = i.order_id)
        WHERE o.status != "canceled" AND o.status != "unavailable"
        GROUP BY o.order_id
    ) AS s
    GROUP BY year(s.purchase_timestamp), month(s.purchase_timestamp)
    HAVING year(s.purchase_timestamp) = 2017
    order by fecha asc ;""", con=engine)

diferencia = kpi_variacionVentas['dif_perc'] = kpi_variacionVentas['total'].pct_change()
#kpi_variacionVentas['dif_perc'] = round(kpi_variacionVentas['dif_perc'], 0)

dif = kpi_variacionVentas['dif_perc'].map(lambda x:format(x,'.2%'))

prom_variacion = kpi_variacionVentas['dif_perc'].mean()
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. KPI
#           B. Puntuacion neta del promotor
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
kpi_puntuacionPromotor = pd.read_sql(""" 
    select score 
    from order_reviews
    where score > 3
    """, con=engine)
kpn = kpi_puntuacionPromotor.shape[0]
#--------------------------------------------------------------------------------------#
kpi_puntuacionPromotor = pd.read_sql(""" 
select score 
from order_reviews
where score <= 3
""", con=engine)
nkpn = kpi_puntuacionPromotor.shape[0]
#--------------------------------------------------------------------------------------#
total_c = kpn + nkpn
#--------------------------------------------------------------------------------------#
pn = round(((kpn-nkpn)/total_c)*100 ,2)
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. KPI
#           C. Fidelidad del cliente
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
df_customers = pd.read_csv("D:\PF-DTS05-E-COMMERCE-OLIST\data_warehouse\datasets\olist_customers_dataset.csv") #1
df_orders = pd.read_csv("D:\PF-DTS05-E-COMMERCE-OLIST\data_warehouse\datasets\olist_orders_dataset.csv") #2
df_merged_FC = pd.merge(df_customers, df_orders, on='customer_id') #3
df_merged_FC.drop(columns=['customer_zip_code_prefix','customer_city', 'customer_state', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date'], inplace=True) #4
df_merged_FC['order_purchase_timestamp'] = pd.to_datetime(df_merged_FC['order_purchase_timestamp']) #5
df_merged_FC['quarter'] =df_merged_FC['order_purchase_timestamp'].dt.quarter #6
df_merged_FC['year'] = df_merged_FC['order_purchase_timestamp'].dt.year #7
clientes_group = df_merged_FC.groupby(['customer_unique_id','quarter','year']).size().reset_index(name='num_compras') #8
clientes_group['compro_en_trimestre'] = clientes_group['num_compras'] > 1 #9
clientes_group['compro_en_trimestre_anterior'] = clientes_group.groupby("customer_unique_id")['compro_en_trimestre'].shift(1) #10
clientes_fieles = clientes_group[(clientes_group['compro_en_trimestre'] == True) & (clientes_group['compro_en_trimestre_anterior'] == True)] #11
num_clientes_fieles = len(clientes_fieles) #12 resultado de numero de clietes fieles
num_total_clientes = len(clientes_group[clientes_group['compro_en_trimestre'] == True]) #13 resultado de numero total de clientes que compro en el trimestre
porcentaje_clientes_fieles = round((num_clientes_fieles / num_total_clientes)*100,2) #14 resultado del porcentaje de fidelidad del cliente
objetivo = (porcentaje_clientes_fieles + (porcentaje_clientes_fieles * 5) /100) 
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. KPI
#           D. Tasa de Conversión
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
vendedores_interesados = pd.read_sql(""" 
    select count(mql_id) as interesados
    from marketing_qualified_leads;
    """, con=engine)
Vi = vendedores_interesados['interesados'][0]
#--------------------------------------------------------------------------------------#
vendedores_cerrados = pd.read_sql(""" 
    select count(mql_id) as cerrados
    from closed_deals;
    """, con=engine)
Vc = vendedores_cerrados['cerrados'][0]
#--------------------------------------------------------------------------------------#
TC = round((Vc/Vi)*100, 2)
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. KPI
#           E. Puntualidad de la entrega
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
entregas_puntuales = pd.read_sql(""" 
    select *
    from orders
    where estimated_delivery_date > delivered_customer_date 
    having status = 'delivered';
    """, con=engine)
Ep = entregas_puntuales.shape[0]
#--------------------------------------------------------------------------------------#  
total_entregas = pd.read_sql(""" 
    select * from orders;
    """, con=engine)
Te = total_entregas.shape[0]
#--------------------------------------------------------------------------------------#
Pe = round((Ep/Te)*100, 2)
Pe
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           2. KPI
#           F. Tiempo total del proceso (TTP)
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#











#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           
#               
#               
#-------------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
# FUNCIONES PRINCIPALES
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
#           3. Funciones que visualizan el NAVEGADOR de Opciones
#               
#               - Panel General
#               - Seller - Customers
#               - Method Payments - Delivery
#               - Marketing - Review
#               - KPIs
#               
#               
#--------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------#
#@st.cache(persist=True)
def Panel():
    st.header('Visualizacion de Datos Generales')
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
#           3. Dashboard visualizacion grafica de lineas
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
#           4. Dashboard visualizacion grafica de barras
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
#           5. Dashboard visualizacion grafica de funnel
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
#           6. Dashboard visualizacion grafica de pie
#               - Ingresos por estado
#               
#               
#--------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------#
 
    fig = px.pie(values=valores_state, names=estados, title='Participacion de las Ventas por Estado', color_discrete_sequence=px.colors.sequential.RdBu)
    

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.markdown('')

    with middle_column:
        st.plotly_chart(fig, use_container_width=True)

    with right_column:
        st.markdown('')




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


    fig1 = px.funnel(categoria_produ, 
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
    fig1.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
    )
#------------------------------------------------------------------------------#
    fig2 = px.funnel(ordenes_mes, 
    x = 'total', 
    y = 'fecha',
    #textposition = "inside",
    title="Total Ordenes Agrupadas por Mes",
    color_discrete_sequence=["#33E3FF"] * len(ordenes_mes),
    #color = ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
    #labels=(),
    orientation="h",
    opacity = 0.65

    )
    #fig.show()
    fig2.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
    )

#------------------------------------------------------------------------------#
#       - Ubicaciones de las graficas
#------------------------------------------------------------------------------#

    left_column, right_column = st.columns(3)
    left_column.plotly_chart(fig1, use_container_width=True)
    left_column.plotly_chart(fig2, use_container_width=True)
   
#------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#
#              FUNCION Customers-Sellers
#-------------------------------------------------------------------------------#
#@st.cache(persist=True)
def Vendedores():
    
    st.header('Visualizacion de análisis de Vendedores y Clientes')
    st.text('A continuación se observara los resultados del análisis')
    st.markdown('***')
#------------------------------------------------------------------------------#
#       1. Grafica de Clientes por estado
#------------------------------------------------------------------------------#
    fig_clientes_estado = px.bar(
        clientes_estado,
        x = 'nclientes',
        y = 'state',
        orientation="h",
        title="Top 10 Clientes por Estado",
        color_discrete_sequence=["#F21F2C"] * len(clientes_estado),
        template='plotly_white',
    )
    fig_clientes_estado.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )
#------------------------------------------------------------------------------#
#       2. Grafica de Vendedores por estado
#------------------------------------------------------------------------------#

    fig_vendedores_estado = px.bar(
        vendedores_estado,
        x = 'state',
        y = 'nvendedores',
        #orientation="h",
        title="Top 10 Vendedores por Estado",
        color_discrete_sequence=["#1FF29F"] * len(vendedores_estado),
        template='plotly_white',
    )
    fig_vendedores_estado.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )
#------------------------------------------------------------------------------#
#       3. Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_clientes_estado, use_container_width=True) 
    #middle_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig_vendedores_estado, use_container_width=True)
#------------------------------------------------------------------------------#
#       4. Grafica de ordenes agrupadas por mes
#------------------------------------------------------------------------------#
    fig_ordenes_mes = px.bar(
        ordenes_mes,
        x = 'mes', 
        y = 'ingresos',
        #orientation="h",
        title="Total Ordenes Agrupadas por Mes",
        color_discrete_sequence=["#F1C11E"] * len(ordenes_mes),
        template='plotly_white',
    )
    fig_ordenes_mes.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )    
#------------------------------------------------------------------------------#
#       5. Grafica de pie
#------------------------------------------------------------------------------#
    fig_pie = px.pie(values=valores, names=estatus, title='Relacion estado de ordenes agrupadas por año', color_discrete_sequence=px.colors.sequential.Viridis)
#------------------------------------------------------------------------------#
#      
#------------------------------------------------------------------------------#    
#------------------------------------------------------------------------------#
#       6. Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_ordenes_mes, use_container_width=True) 
    #middle_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig_pie, use_container_width=True)

#-------------------------------------------------------------------------------#
#              FUNCION Method Payments-Delivery
#-------------------------------------------------------------------------------#
def Method():
    st.header('Visualizacion de análisis de Metodos de pago y Entregas')
    st.text('A continuación se observara los resultados del análisis')
    st.markdown('***')
#------------------------------------------------------------------------------#
#       1. Grafica de pie
#------------------------------------------------------------------------------#
    fig_pie = px.pie(values=cantidad, names=tipo, title='Número de pagos por tipo', color_discrete_sequence=px.colors.sequential.Inferno)
#------------------------------------------------------------------------------#
#      
#------------------------------------------------------------------------------# 
    diferido_valor = pd.read_sql("""
        select installments, count(*) as diferido, sum(value) as total
        from order_payments
        group by installments
        order by installments asc;""", con=engine)

#------------------------------------------------------------------------------#
#       2. Grafica de linea para la distribución de pagos por diferido
#------------------------------------------------------------------------------#    
    st.markdown('***')
    line_chart = alt.Chart(diferido_valor).mark_line().encode(
        y =  alt.Y('total', title='Ingresos($)'),
        x =  alt.X('installments', title='Diferido')
    ).properties(
        height=400, width=400,
        title="Distribucion de cuotas diferidas"
    ).configure_title(
        fontSize=16
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
 
    #st.altair_chart(line_chart, use_container_width=True)
#------------------------------------------------------------------------------#
#        Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)

    left_column.plotly_chart(fig_pie, use_container_width=True)
    right_column.altair_chart(line_chart, use_container_width=True) 
    #middle_column.plotly_chart(fig, use_container_width=True)

#------------------------------------------------------------------------------#
#       3. Grafica de barras ingresos por tipo de pago
#------------------------------------------------------------------------------#
    payment_type = pd.read_sql("""
        select type, sum(value) as total
        from order_payments
        group by type
        order by total desc;""", con=engine)

    fig_pyment_type = px.bar(
        payment_type,
        x = 'type', 
        y = 'total',
        #orientation="h",
        title="Ingresos por tipo de metodo de pago",
        color_discrete_sequence=["#DA8DF9"] * len(payment_type),
        template='plotly_white',
    )
    fig_pyment_type.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )    
#------------------------------------------------------------------------------#
#       4. Grafica de Productos entregados en la fecha estimada
#------------------------------------------------------------------------------# 
    delivery_estimado = pd.read_sql("""
        SELECT count(d.dias) AS 'entregado',
            CASE
            WHEN d.dias  < 1 THEN 'Llego en fecha estimada'
            ELSE 'LLego con retrazo'
            END
            AS Plazo_de_entrega
        FROM (SELECT datediff(o.delivered_customer_date, o.estimated_delivery_date ) as dias
            FROM orders AS o
            WHERE o.status = 'delivered'
             ) AS d

        GROUP BY Plazo_de_entrega;""", con=engine)
    entregado = delivery_estimado['entregado']
    plazo = delivery_estimado['Plazo_de_entrega']


    fig_pie_delivery = px.pie(values=entregado, names=plazo, title='Productos entregados en fecha estimada', color_discrete_sequence=px.colors.sequential.Cividis)

#------------------------------------------------------------------------------#
#       Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_pyment_type, use_container_width=True) 
    #middle_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig_pie_delivery, use_container_width=True)

    
#------------------------------------------------------------------------------#
#       5. Grafica Productos entregado en un rango de dias
#------------------------------------------------------------------------------#
    delivery_rango = pd.read_sql("""
        SELECT count(d.dias) AS 'cantidad',
            CASE
                WHEN dias  < 4 THEN 'menos de 4'
                WHEN dias < 7 THEN 'de 4 a 6'
                WHEN dias < 11 THEN 'de 7 a 10'
                WHEN dias < 16 THEN 'de 11 a 15'
                ELSE 'más de 15'
            END
            AS rango_entregas
        FROM (SELECT datediff(o.delivered_customer_date, o.purchase_timestamp ) as dias
            FROM orders AS o
        WHERE o.status = 'delivered'
            ) AS d
        GROUP BY rango_entregas;""", con=engine)

    #cantidad_delivery = delivery_rango['cantidad']
    #rangos = delivery_rango['rango_entregas']  

    fig_delivery_rango = px.bar(
        delivery_rango,
        x = 'rango_entregas', 
        y = 'cantidad',
        #orientation="h",
        title="Productos Entregados en un rango de días",
        color_discrete_sequence=["#7EA2F7"] * len(payment_type),
        template='plotly_white',
    )
    fig_delivery_rango.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )    

#------------------------------------------------------------------------------#
#       6. Grafica Productos entregado en un rango de dias
#------------------------------------------------------------------------------#   
    delivery_peso = pd.read_sql("""
    SELECT avg(d.freight_value) AS 'promedio_flete',
        CASE
        WHEN d.weight_g  < 501 THEN 'menos de 500g'
        WHEN d.weight_g < 1001 THEN 'de 500g a 1kg'
        WHEN d.weight_g < 5001 THEN 'de 1kg a 5kg'
        WHEN d.weight_g < 10001 THEN 'de 5kg a 10kg'
        WHEN d.weight_g < 20001 THEN 'de 10kg a 20kg'
        ELSE 'más de 20kg'
        END
        as rango_peso
    FROM (SELECT i.product_id, i.freight_value, p.weight_g
        FROM order_items AS i
        LEFT JOIN products as p ON(i.product_id = p.product_id)
            ) AS d

    GROUP BY rango_peso;""", con=engine)
    prom_flete = delivery_peso['promedio_flete']
    rango_peso = delivery_peso['rango_peso']

    fig_pie_peso = px.pie(values=prom_flete, names=rango_peso, title='Promedio de Flete por rango de pesoa', color_discrete_sequence=px.colors.sequential.algae)
  
#------------------------------------------------------------------------------#
#       Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_delivery_rango, use_container_width=True) 
#middle_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig_pie_peso, use_container_width=True)
  
def Marketing():
    st.header('Visualizacion de análisis de Marketing y Reviews')
    st.text('A continuación se observara los resultados del análisis')
    st.markdown('***')
#------------------------------------------------------------------------------#
#       1. Grafica de linea volumen de primer contacto con el vendedor por año-mes
#      
#------------------------------------------------------------------------------# 
    marketing_volumen = pd.read_sql("""
        select concat(year(first_contact_date), '-', month(first_contact_date)) as anio_mes, count(*) as volumen 
        from marketing_qualified_leads
        group by anio_mes
        order by first_contact_date asc;""", con=engine)
  
    st.markdown('***')
    line_chart = alt.Chart(marketing_volumen).mark_line().encode(
        y =  alt.Y('volumen', title='volumne(#)'),
        x =  alt.X('anio_mes', title='Anio-Mes')
    ).properties(
        height=400, width=400,
        title="Distribucion de volumen primer contacto por año y mes"
    ).configure_title(
        fontSize=16
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
    
    #st.altair_chart(line_chart, use_container_width=True)
#------------------------------------------------------------------------------#
#       2. Grafica de barras del Volumen por canal de mercadeo
#------------------------------------------------------------------------------# 
    marketing_origin = pd.read_sql("""
        select origin, count(*) as volumen
        from marketing_qualified_leads
        group by origin
        order by volumen desc;""", con=engine)

    fig_marketing_origin = px.bar(
        marketing_origin,
        x = 'origin', 
        y = 'volumen',
        #orientation="h",
        title="Volumen por canal de mercadeo",
        color_discrete_sequence=["#BC0330"] * len(marketing_origin),
        template='plotly_white',
    )
    fig_marketing_origin.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )    

#------------------------------------------------------------------------------#
#        Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)

    left_column.altair_chart(line_chart, use_container_width=True) 
    right_column.plotly_chart(fig_marketing_origin, use_container_width=True)
    #middle_column.plotly_chart(fig, use_container_width=True)
#------------------------------------------------------------------------------#
#       3. Grafica de barras Promedio de score por categoria
#------------------------------------------------------------------------------#
    reviews_score_prom = pd.read_sql("""
    SELECT AVG(a.score) as prom_score, c.category_name AS categoria
    FROM order_reviews AS a
        INNER JOIN order_items AS b
        ON (a.order_id = b.order_id)
        INNER JOIN products AS c
        ON (b.product_id = c.product_id)
    GROUP BY categoria
    order by prom_score desc
    limit 15; """, con=engine) 

    fig_reviews_score_prom = px.bar(
        reviews_score_prom,
        x = 'prom_score',
        y = 'categoria',
        orientation="h",
        title="Top 15 Score por categoria",
        color_discrete_sequence=["#93F553"] * len(ingresos_ciudad),
        template='plotly_white',
    )
    fig_reviews_score_prom.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )


#------------------------------------------------------------------------------#
#       4. Grafica cierre de acuerdo por segmento de negocio
#------------------------------------------------------------------------------# 
    cierre_volumen_segm = pd.read_sql("""
    select business_segment, count(*) as volumen
        from closed_deals
        group by business_segment
        order by volumen desc
        limit 10; """, con=engine) 
    

    fig_cierre = px.funnel(cierre_volumen_segm, 
        x = 'volumen', 
        y = 'business_segment',
        #textposition = "inside",
        title="Top 10 cierre acuerdo por segmento de negocio",
        color_discrete_sequence=["#E3B7F9"] * len(cierre_volumen_segm),
        #color = ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
        #labels=(),
        orientation="h",
        opacity = 0.65

        )
        #fig.show()
    fig_cierre.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = dict(showgrid=False)
        )
    
#------------------------------------------------------------------------------#
#       5. Grafica Productos entregado en un rango de dias
#------------------------------------------------------------------------------#
    

    #cantidad_delivery = delivery_rango['cantidad']
    #rangos = delivery_rango['rango_entregas']  

    

    
#------------------------------------------------------------------------------#
#       6. Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_reviews_score_prom, use_container_width=True) 
    #middle_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig_cierre, use_container_width=True)


#------------------------------------------------------------------------------#
#       6. Ubicaciones de las graficas
#------------------------------------------------------------------------------#
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_delivery_rango, use_container_width=True) 
    #middle_column.plotly_chart(fig, use_container_width=True)
    right_column.plotly_chart(fig_pie_delivery, use_container_width=True)
  




def kpi():
    st.header('KPIs')
    st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">1. Variación porcentual del volumen de ventas por mes año 2017</p>', unsafe_allow_html=True)
    #st.subheader('Variación porcentual del volumen de ventas por mes año 2017')
    st.text('Objetivo: Evaluar aumento o disminucion de la variación porcentual del volumen de ventas por mes')

    left_column, middle_colum, right_column = st.columns(3)

    st.markdown('***')
    with left_column:
        st.text('Venta Agrupada por mes 2017')
        st.dataframe(kpi_variacionVentas)

    with middle_colum:
        st.text('Variación')
        st.dataframe(dif)

    with right_column:
        st.text('Promedio Variación')
        st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(prom_variacion), unsafe_allow_html=True) 

#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#

    st.markdown('***')
#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#
#               2. kpi - PUNTUACION NETA DEL PROMOTOR
#-------------------------------------------------------------------------------#
    st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">2. Puntuación neta del promotor</p>', unsafe_allow_html=True)
    st.text('Objetivo: Medir la satisfacción del cliente')

    left_column, middle_column, right_column = st.columns(3)
    
    with left_column:
      st.subheader('Cantidad Calificaciones Positivas')
      st.text('Esta calificación es de score > 3')
      #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
      #st.subheader("Reales $ {:,.2f}".format(kpn))
    #  st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(kpn), unsafe_allow_html=True)

    with middle_column:
        st.subheader('Cantidad Calificaciones Negativas')
        st.text('Esta calificación es de score <= 3')
    #   st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(nkpn), unsafe_allow_html=True)    

    with right_column:
        st.subheader('Puntuación Neta')
        st.text('Satisfacción del cliente')
    #    st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(pn), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Positivas:", kpn, "90000")
    col2.metric("Negativas",  nkpn, "-10000")
    col3.metric("Objetivo", pn, "5%")

#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
    st.markdown('***') 
#-------------------------------------------------------------------------------#
#               3. kpi - FIDELIDAD DEL CLIENTE
#-------------------------------------------------------------------------------#
    st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">3. Fidelidad del Cliente</p>', unsafe_allow_html=True)
    st.text('Objetivo: Medir la tasa de clientes que vuelven a comprar dentro de un periodo determinado')

    left_column, middle_column, right_column = st.columns(3)
    #st.markdown('***')
    with left_column:
      st.subheader('Cantidad Clientes Fieles')
      st.text('Con pocos datos se identifican clientes fieles')
      #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
      #st.subheader("Reales $ {:,.2f}".format(kpn))
    #  st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(num_clientes_fieles), unsafe_allow_html=True)

    with middle_column:
        st.subheader('Total de Clientes ')
        st.text('Número de clientes')
    #    st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(num_total_clientes), unsafe_allow_html=True)    

    with right_column:
        st.subheader('Porcentaje de Fidelidad')
        st.text('Basado en los datos obtenidos de clientes del 2017')
    #    st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(porcentaje_clientes_fieles), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Fidelidad:", num_clientes_fieles, "500")
    col2.metric("Total Clientes",  num_total_clientes, "2500")
    col3.metric("Objetivo", "0.92%", "5%")

#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
    st.markdown('***')
#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#
#               4. kpi - TASA DE CONVERSION
#-------------------------------------------------------------------------------#
    st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">4. Tasa de Conversión</p>', unsafe_allow_html=True)
    st.text('Objetivo: Medir la tasa de vendedores potenciales que se unen a la empresa')

    left_column, middle_column, right_column = st.columns(3)
    st.markdown('***')
    with left_column:
      st.subheader('Cant. Vendedores Interesados')
      st.text('Vendedores que desean ofrecer sus productos')
      #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
      #st.subheader("Reales $ {:,.2f}".format(kpn))
    #  st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Vi), unsafe_allow_html=True)

    with middle_column:
        st.subheader('Cant. Vendedores Acuerdo Cerrado ')
        st.text('Vendedores que hicieron acuerdo de cierre')
    #    st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Vc), unsafe_allow_html=True)    

    with right_column:
        st.subheader('Tasa de Conversión')
        st.text('Tasa de conversión actual')
    #    st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(TC), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Interesados:", Vi, "10000")
    col2.metric("Cierres",  Vc, "1500")
    col3.metric("Conversión", TC, "15%")
#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
    st.markdown('***')
#-------------------------------------------------------------------------------#
#               5. kpi - PUNTUALIDAD DE LA ENTREGA
#-------------------------------------------------------------------------------#  
#-------------------------------------------------------------------------------#
    st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">5. Puntualidad de la Entrega</p>', unsafe_allow_html=True)
    st.text('Objetivo: Medir el porcentaje de entregas que se realizan a tiempo en relación con el número total de entregas.')

    left_column, middle_column, right_column = st.columns(3)
    st.markdown('***')
    with left_column:
      st.subheader('Cant. Pedidos Entregados')
      st.text('Número de pedidos')
      #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
      #st.subheader("Reales $ {:,.2f}".format(kpn))
    #  st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Te), unsafe_allow_html=True)

    with middle_column:
        st.subheader('Pedidos Entregados Puntualmente ')
        st.text('Pedidos Entregados puntualmente')
    #    st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Ep), unsafe_allow_html=True)    

    with right_column:
        st.subheader('% Puntualidad de Entrega')
        st.text('La puntualidad de entrega de los productos')
    #    st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Pe), unsafe_allow_html=True)
    

    col1, col2, col3 = st.columns(3)
    col1.metric("Entregados:", Te, "105000")
    col2.metric("Puntualmente",  Ep, "95000")
    col3.metric("% Puntualidad", Pe, "95%")
#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
    st.markdown('***')
#-------------------------------------------------------------------------------#
    st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">6. Tiempo total del proceso (TTP)</p>', unsafe_allow_html=True)
    st.text('Objetivo: Optimizar los tiempos de compra y envío.')

    left_column, middle_column, right_column = st.columns(3)
    st.markdown('***')
    with left_column:
      st.subheader('Cant. Pedidos Entregados')
      st.text('Número de pedidos')
      #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
      #st.subheader("Reales $ {:,.2f}".format(kpn))
      st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Te), unsafe_allow_html=True)

    with middle_column:
        st.subheader('Pedidos Entregados Puntualmente ')
        st.text('Pedidos Entregados puntualmente')
        st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Ep), unsafe_allow_html=True)    

    with right_column:
        st.subheader('% Puntualidad de Entrega')
        st.text('La puntualidad de entrega de los productos')
        st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Pe), unsafe_allow_html=True)
#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
    st.markdown('***')
#-------------------------------------------------------------------------------#
#     Configuracion de Metricas
#-------------------------------------------------------------------------------#
    #col1, col2, col3 = st.columns(3)
    #col1.metric("Temperature", "70 °F", "1.2 °F")
    #col2.metric("Wind", "9 mph", "-8%")
    #col3.metric("Humidity", "86%", "4%")
#-------------------------------------------------------------------------------#
@st.cache
def data_header(dataset):
    st.header('Data Header')
    st.write(dataset.head(10))
#-------------------------------------------------------------------------------#
#               DEMO
#-------------------------------------------------------------------------------#
    x_axis_val = st.selectbox('Seleccione X-Eje Value', options=ingresos_anio.columns)
    y_axis_val = st.selectbox('Seleccione Y-Eje Value', options=ingresos_anio.columns)
    col = st.color_picker('Seleccione color de la grafica')
    plot = px.scatter(ingresos_anio, x=x_axis_val, y=y_axis_val)
    plot.update_traces(marker=dict(color=col))
    st.plotly_chart(plot)
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
@st.cache
def stats(dataset):
    st.header('Data Statistics')
    st.write(dataset.describe())
#--------------------------------------------------------------------------------------#
#               DEMO 
#--------------------------------------------------------------------------------------#
# -- Create three columns
    col1, col2, col3 = st.columns([5, 5, 20])
# -- Put the image in the middle column
# - Commented out here so that the file will run without having the image downloaded
#with col2:
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
        ("All", "BA", "MG", "PR", "RJ", "SP"),
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
#-------------------------------------------------------------------------------#



#--------------------------------------------------------------------------------------#
# AREA DE OPCIONES PARA EJECUTAR LAS FUNCIONALIDADES y DE NAVEGACION
if options == 'Panel General':
    st.text('Bienvenidos')
    Panel()
elif options == 'Sellers-Customers':
    st.text('Bienvenidos')
    Vendedores()
elif options == 'Method Payments-Delivery':
    st.text('Bienvenidos')
    Method()
elif options == 'Marketing-Reviews':
    st.text('Bienvenidos')
    Marketing()
elif options == 'KPIs':
    st.text('Bienvenidos')
    kpi()
#--------------------------------------------------------------------------------------#
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

elif options == 'Ventas':
    st.text('Podemos Observar el Dataset')
    Ventas(dataset)
elif options == 'Productos':
    st.text('Visualizacion de Graficas')
    Productos(categoria_produ)
#--------------------------------------------------------------------------------------#





#------------------------------------------------------------------------------------------#
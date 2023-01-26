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

st.set_page_config(page_title="KPIs", page_icon="📈", layout="wide")

st.sidebar.header("KPIs")

my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')
#------------------------------------------------------------------------------------------#
# Conexion al DATAWAREHOUSE de los datos
engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"
)

#------------------------------------------------------------------------------------------#



st.title(':mag_right: KPIs')
st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">1. Variación porcentual del volumen de ventas por mes año 2017</p>', unsafe_allow_html=True)
#st.subheader('Variación porcentual del volumen de ventas por mes año 2017')
st.text('Objetivo: Evaluar aumento o disminucion de la variación porcentual del volumen de ventas por mes')

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
st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">2. Puntuación neta del promotor</p>', unsafe_allow_html=True)
st.text('Objetivo: Medir la satisfacción del cliente')

left_column, middle_column, right_column = st.columns(3)
    
with left_column:
    st.subheader('Cantidad Calificaciones Positivas')
    st.text('Esta calificación es de score > 3')
    #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
    #st.subheader("Reales $ {:,.2f}".format(kpn))
    #st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(kpn), unsafe_allow_html=True)

with middle_column:
    st.subheader('Cantidad Calificaciones Negativas')
    st.text('Esta calificación es de score <= 3')
    #st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(nkpn), unsafe_allow_html=True)    

with right_column:
    st.subheader('Puntuación Neta')
    st.text('Satisfacción del cliente')
    #st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(pn), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Positivas:", kpn, "81000")
col2.metric("Negativas",  nkpn, "-21400")
col3.metric("Objetivo", pn, "60%")

#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
st.markdown('***') 
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

st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">3. Fidelidad del Cliente</p>', unsafe_allow_html=True)
st.text('Objetivo: Medir la tasa de clientes que vuelven a comprar dentro de un periodo determinado')

left_column, middle_column, right_column = st.columns(3)
#st.markdown('***')
with left_column:
    st.subheader('Cantidad Clientes Fieles')
    st.text('Con pocos datos se identifican clientes fieles')
    #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
    #st.subheader("Reales $ {:,.2f}".format(kpn))
    #st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(num_clientes_fieles), unsafe_allow_html=True)

with middle_column:
    st.subheader('Total de Clientes ')
    st.text('Número de clientes')
    #st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(num_total_clientes), unsafe_allow_html=True)    

with right_column:
    st.subheader('Porcentaje de Fidelidad')
    st.text('Basado en los datos obtenidos de clientes del 2017')
    #st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(porcentaje_clientes_fieles), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Fidelidad:", num_clientes_fieles, "17")
col2.metric("Total Clientes",  num_total_clientes, "1850")
col3.metric("Objetivo", "0.92%", "5%")

#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
st.markdown('***')
#-------------------------------------------------------------------------------#
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

st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">4. Tasa de Conversión</p>', unsafe_allow_html=True)
st.text('Objetivo: Medir la tasa de vendedores potenciales que se unen a la empresa')

left_column, middle_column, right_column = st.columns(3)
    
with left_column:
    st.subheader('Cant. Vendedores Interesados')
    st.text('Vendedores que desean ofrecer sus productos')
    #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
    #st.subheader("Reales $ {:,.2f}".format(kpn))
    #st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Vi), unsafe_allow_html=True)

with middle_column:
    st.subheader('Cant. Vendedores Acuerdo Cerrado ')
    st.text('Vendedores que hicieron acuerdo de cierre')
    #st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Vc), unsafe_allow_html=True)    

with right_column:
    st.subheader('Tasa de Conversión')
    st.text('Tasa de conversión actual')
    #st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(TC), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Interesados:", Vi, "9200")
col2.metric("Cierres",  Vc, "970")
col3.metric("Conversión", TC, "15%")
#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
st.markdown('***')
  
#-------------------------------------------------------------------------------#
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
Pe = round((Ep/Te)*100, 2)
Pe

st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">5. Puntualidad de la Entrega</p>', unsafe_allow_html=True)
st.text('Objetivo: Medir el porcentaje de entregas que se realizan a tiempo en relación con el número total de entregas.')

left_column, middle_column, right_column = st.columns(3)
    
with left_column:
    st.subheader('Cant. Pedidos Entregados')
    st.text('Número de pedidos')
    #st.subheader("Reales $ {:,.2f}".format(total_ingresos))
    #st.subheader("Reales $ {:,.2f}".format(kpn))
    #st.markdown('<p style="color:#33FFFF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Te), unsafe_allow_html=True)

with middle_column:
    st.subheader('Pedidos Entregados Puntualmente ')
    st.text('Pedidos Entregados puntualmente')
    #st.markdown('<p style="color:#F56ACF;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Ep), unsafe_allow_html=True)    

with right_column:
    st.subheader('% Puntualidad de Entrega')
    st.text('La puntualidad de entrega de los productos')
    #st.markdown('<p style="color:#F3FF33;font-size:24px;border-radius:2%;">{:,.2f}</p>'.format(Pe), unsafe_allow_html=True)
    

col1, col2, col3 = st.columns(3)
col1.metric("Entregados:", Te, "105000")
col2.metric("Puntualmente",  Ep, "93800")
col3.metric("% Puntualidad", Pe, "95%")
#---------------FINALIZA EL LIMITE DE CADA KPI----------------------------------#
st.markdown('***')
#-------------------------------------------------------------------------------#
st.markdown(f'<p style="color:#F3FF33;font-size:18px;border-radius:2%;">6. Tiempo total del proceso (TTP)</p>', unsafe_allow_html=True)
st.text('Objetivo: Optimizar los tiempos de compra y envío.')

left_column, middle_column, right_column = st.columns(3)
    
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
st.balloons()
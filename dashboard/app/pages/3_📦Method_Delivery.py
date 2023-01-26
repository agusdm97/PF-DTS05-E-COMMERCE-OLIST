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

st.set_page_config(page_title="Method Payment - Delivery", page_icon="", layout="wide")

st.sidebar.header("Method Payment & Delivery")

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



st.title(':mag_right: Visualizacion de análisis de Metodos de pago y Entregas')
st.text('A continuación se observara los resultados del análisis')
st.markdown('***')
#------------------------------------------------------------------------------#
#       1. Grafica de pie
#------------------------------------------------------------------------------#
method_payment = pd.read_sql("""
    select op.type, count(*) as total
    from order_payments op
    group by op.type
    order by total desc;""", con=engine)

tipo = method_payment['type']
cantidad = method_payment['total']

fig_pie = px.pie(values=cantidad, names=tipo, title='Proporción por metodo de pago', color_discrete_sequence=px.colors.sequential.Inferno)
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
    title="Productos Entregados segun rango de días",
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

fig_pie_peso = px.pie(values=prom_flete, names=rango_peso, title='Promedio valor flete por rango de peso', color_discrete_sequence=px.colors.sequential.algae)
  
#------------------------------------------------------------------------------#
#       Ubicaciones de las graficas
#------------------------------------------------------------------------------#
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_delivery_rango, use_container_width=True) 
#middle_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig_pie_peso, use_container_width=True)

st.balloons()
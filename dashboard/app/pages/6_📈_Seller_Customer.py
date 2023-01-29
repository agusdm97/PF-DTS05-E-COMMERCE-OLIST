# ----LIBRERIAS--------------------------------------------------------------------------------------#
import sqlalchemy as sql
import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
import pymysql


st.set_page_config(page_title="Sellers - Customers", page_icon="📈", layout="wide")
st.sidebar.header("Sellers & Customers")

my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)

with st.spinner("Wait for it..."):
    time.sleep(5)
st.success("Done!")
# ------------------------------------------------------------------------------------------#
# Conexion al DATAWAREHOUSE de los datos
engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

# ------------------------------------------------------------------------------------------#
st.title(":mag_right: Visualizacion de análisis de Vendedores y Clientes")
st.text("A continuación se observara los resultados del análisis")
st.markdown("***")
# ------------------------------------------------------------------------------#
#       
# ------------------------------------------------------------------------------#

tab1, tab2 = st.tabs(["Sellers-Customers", "Orders"])

with tab1:
   st.header("Bienvenidos")
# ------------------------------------------------------------------------------#
#       1. Grafica de Clientes por estado
# ------------------------------------------------------------------------------#
   clientes_estado = pd.read_sql(
    """
    select g.state, count(c.customer_id) as nclientes
    from customers c
    JOIN geolocations g ON(c.zip_code = g.zip_code)
    group by g.state
    order by nclientes desc
    limit 10;""",
    con=engine,
   )

   fig_clientes_estado = px.bar(
    clientes_estado,
    x="nclientes",
    y="state",
    orientation="h",
    title="Top 10 Clientes por Estado",
    color_discrete_sequence=["#F21F2C"] * len(clientes_estado),
    template="plotly_white",
   )
   fig_clientes_estado.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False)
   )
# ------------------------------------------------------------------------------#
#       2. Grafica de Vendedores por estado
# ------------------------------------------------------------------------------#
   vendedores_estado = pd.read_sql(
    """
    select g.state, count(s.seller_id) as nvendedores
    from sellers s
    JOIN geolocations g ON(s.zip_code = g.zip_code)
    group by g.state
    order by nvendedores desc
    limit 10;""",
    con=engine,
)

   fig_vendedores_estado = px.bar(
    vendedores_estado,
    x="state",
    y="nvendedores",
    # orientation="h",
    title="Top 10 Vendedores por Estado",
    color_discrete_sequence=["#1FF29F"] * len(vendedores_estado),
    template="plotly_white",
   )
   fig_vendedores_estado.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False)
   )
# ------------------------------------------------------------------------------#
#       3. Ubicaciones de las graficas
# ------------------------------------------------------------------------------#
   left_column, right_column = st.columns(2)

   left_column.plotly_chart(fig_clientes_estado, use_container_width=True)
   #middle_column.plotly_chart(fig, use_container_width=True)
   right_column.plotly_chart(fig_vendedores_estado, use_container_width=True)
# ------------------------------------------------------------------------------#

with tab2:
   st.header("Bienvenidos")
#-------------------------------------------------------------------------------#
#       4. Grafica de ordenes agrupadas por mes
# ------------------------------------------------------------------------------#
   ordenes_mes = pd.read_sql(
    """
    select month(o.approved_at) as mes, sum(oi.price) as ingresos
    from order_items oi
    JOIN orders o ON(oi.order_id = o.order_id)
    group by mes
    order by mes;""",
    con=engine,
   )

   fig_ordenes_mes = px.bar(
    ordenes_mes,
    x="mes",
    y="ingresos",
    # orientation="h",
    title="Total Ordenes Agrupadas por Mes",
    color_discrete_sequence=["#F1C11E"] * len(ordenes_mes),
    template="plotly_white",
)
   fig_ordenes_mes.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))
# ------------------------------------------------------------------------------#
#       5. Grafica de pie
# ------------------------------------------------------------------------------#
   relacion_status = pd.read_sql(
    """
    select year(purchase_timestamp) as anio, status, count(status) as total
    from orders
    where status = 'delivered' or status='canceled' or status='unavailable'
    group by anio, status;""",
    con=engine,
)
   estatus = relacion_status["status"]
   valores = relacion_status["total"]

   fig_pie = px.pie(
    values=valores,
    names=estatus,
    title="Relacion del estado de ordenes",
    color_discrete_sequence=px.colors.sequential.haline,
)
# ------------------------------------------------------------------------------#
#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
#       6. Ubicaciones de las graficas
# ------------------------------------------------------------------------------#
   left_column, right_column = st.columns(2)

   left_column.plotly_chart(fig_ordenes_mes, use_container_width=True)
   #middle_column.plotly_chart(fig, use_container_width=True)
   right_column.plotly_chart(fig_pie, use_container_width=True)

st.snow()

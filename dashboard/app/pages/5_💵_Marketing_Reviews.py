# ----LIBRERIAS--------------------------------------------------------------------------------------#
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

st.set_page_config(page_title="Marketing - Reviews", page_icon="📈", layout="wide")

st.sidebar.header("Marketing & reviews")

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
st.title(":mag_right: Visualizacion de análisis de Marketing y Reviews")
st.text("A continuación se observara los resultados del análisis")
st.markdown("***")
# ------------------------------------------------------------------------------#
#       1. Grafica de linea volumen de primer contacto con el vendedor por año-mes
#
# ------------------------------------------------------------------------------#
marketing_volumen = pd.read_sql(
    """
    select concat(year(first_contact_date), '-', month(first_contact_date)) as anio_mes, count(*) as volumen 
    from marketing_qualified_leads
    group by anio_mes
    order by first_contact_date asc;""",
    con=engine,
)

st.markdown("***")
line_chart = (
    alt.Chart(marketing_volumen)
    .mark_line()
    .encode(
        y=alt.Y("volumen", title="volumne(#)"), x=alt.X("anio_mes", title="Anio-Mes")
    )
    .properties(
        height=400,
        width=400,
        title="Distribucion de volumen primer contacto por año y mes",
    )
    .configure_title(fontSize=16)
    .configure_axis(titleFontSize=14, labelFontSize=12)
)

# st.altair_chart(line_chart, use_container_width=True)
# ------------------------------------------------------------------------------#
#       2. Grafica de barras del Volumen por canal de mercadeo
# ------------------------------------------------------------------------------#
marketing_origin = pd.read_sql(
    """
        select origin, count(*) as volumen
        from marketing_qualified_leads
        group by origin
        order by volumen desc;""",
    con=engine,
)

fig_marketing_origin = px.bar(
    marketing_origin,
    x="origin",
    y="volumen",
    # orientation="h",
    title="Volumen por canal de mercadeo",
    color_discrete_sequence=["#BC0330"] * len(marketing_origin),
    template="plotly_white",
)
fig_marketing_origin.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False)
)

# ------------------------------------------------------------------------------#
#        Ubicaciones de las graficas
# ------------------------------------------------------------------------------#
left_column, right_column = st.columns(2)

left_column.altair_chart(line_chart, use_container_width=True)
right_column.plotly_chart(fig_marketing_origin, use_container_width=True)
# middle_column.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------------#
#       6. Grafica volumen de cierre por lead type
# ------------------------------------------------------------------------------#
cierre_volumen_lead = pd.read_sql(
    """
    select lead_type, count(*) as volumen
    from closed_deals
    group by lead_type
    order by volumen desc
    limit 10; """,
    con=engine,
)

line_chart = (
    alt.Chart(cierre_volumen_lead)
    .mark_line()
    .encode(
        y=alt.Y("volumen", title="volumen(#)"), x=alt.X("lead_type", title="Lead Type")
    )
    .properties(
        height=400, width=400, title="Volumen de cierre por categoria de negocio"
    )
    .configure_title(fontSize=16)
    .configure_axis(titleFontSize=14, labelFontSize=12)
)
# ------------------------------------------------------------------------------#
#       4. Grafica cierre de acuerdo por segmento de negocio
# ------------------------------------------------------------------------------#
cierre_volumen_segm = pd.read_sql(
    """
    select business_segment, count(*) as volumen
        from closed_deals
        group by business_segment
        order by volumen desc
        limit 10; """,
    con=engine,
)


fig_cierre = px.funnel(
    cierre_volumen_segm,
    x="volumen",
    y="business_segment",
    # textposition = "inside",
    title="Top 10 cierre acuerdo por segmento de negocio",
    color_discrete_sequence=["#E3B7F9"] * len(cierre_volumen_segm),
    orientation="h",
    opacity=0.65,
)
# fig.show()
fig_cierre.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))
# ------------------------------------------------------------------------------#
#        Ubicaciones de las graficas
# ------------------------------------------------------------------------------#
left_column, right_column = st.columns(2)


left_column.plotly_chart(fig_cierre, use_container_width=True)
# middle_column.plotly_chart(fig, use_container_width=True)
right_column.altair_chart(line_chart, use_container_width=True)

# ------------------------------------------------------------------------------#
#       5. Grafica top 20 Fechas que tiene el mayor # de cierres
# ------------------------------------------------------------------------------#
cierre_volumen_fecha = pd.read_sql(
    """
    select won_date as fecha, count(*) as volumen
    from closed_deals
    group by won_date
    order by volumen desc
    limit 20; """,
    con=engine,
)

fig_cierre_volumen_fecha = px.bar(
    cierre_volumen_fecha,
    x="fecha",
    y="volumen",
    # orientation="h",
    title="Top 20 fechas volumen alto de cierre ",
    color_discrete_sequence=["#ECF622"] * len(cierre_volumen_fecha),
    template="plotly_white",
)
fig_marketing_origin.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False)
)


# ------------------------------------------------------------------------------#
#       3. Grafica de barras Promedio de score por categoria
# ------------------------------------------------------------------------------#
reviews_score_prom = pd.read_sql(
    """
    SELECT AVG(a.score) as prom_score, c.category_name AS categoria
    FROM order_reviews AS a
        INNER JOIN order_items AS b
        ON (a.order_id = b.order_id)
        INNER JOIN products AS c
        ON (b.product_id = c.product_id)
    GROUP BY categoria
    order by prom_score desc
    limit 15; """,
    con=engine,
)

fig_reviews_score_prom = px.bar(
    reviews_score_prom,
    x="prom_score",
    y="categoria",
    orientation="h",
    title="Top 15 Score por categoria",
    color_discrete_sequence=["#93F553"] * len(reviews_score_prom),
    template="plotly_white",
)
fig_reviews_score_prom.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False)
)


# ------------------------------------------------------------------------------#
#        Ubicaciones de las graficas
# ------------------------------------------------------------------------------#
left_column, right_column = st.columns(2)


left_column.plotly_chart(fig_cierre_volumen_fecha, use_container_width=True)
# middle_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig_reviews_score_prom, use_container_width=True)
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
#       5. Grafica top 20 Fechas que tiene el mayor # de cierres
# ------------------------------------------------------------------------------#
reviews_cant_score = pd.read_sql(
    """
SELECT count(*) as cant_reviews, score 
FROM order_reviews
GROUP BY score
order by cant_reviews desc; """,
    con=engine,
)

fig_reviews_cant_score = px.bar(
    reviews_cant_score,
    x="score",
    y="cant_reviews",
    # orientation="h",
    title="Cantidad de reviews por score",
    color_discrete_sequence=["#22A6F6"] * len(reviews_cant_score),
    template="plotly_white",
)
fig_reviews_cant_score.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False)
)
# ------------------------------------------------------------------------------#
#        Ubicaciones de las graficas
# ------------------------------------------------------------------------------#
left_column, middle_column, right_column = st.columns(3)


# left_column.plotly_chart()
middle_column.plotly_chart(fig_reviews_cant_score, use_container_width=True)
# right_column.plotly_chart()

# ------------------------------------------------------------------------------#
#
st.snow()

from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Marketing - Reviews", page_icon="📈", layout="wide")

st.sidebar.header("Marketing & reviews")


engine = create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)


st.title(":mag_right: Visualización de análisis de Marketing y Reviews")
st.text("A continuación se observara los resultados del análisis")
st.markdown("---")

tab1, tab2 = st.tabs(["Marketing ", "Reviews"])

with tab1:
    col_contactos, col_cerrados = st.columns([3, 2])

    with col_contactos:
        df_marketing = pd.read_sql(
            sql="""
            SELECT mql_id, first_contact_date, origin AS  Origen
            FROM marketing_qualified_leads;
            """,
            con=engine,
        )
        df_marketing["first_contact_date"] = pd.to_datetime(
            df_marketing["first_contact_date"]
        )
        df_marketing["año_mes"] = df_marketing["first_contact_date"].dt.to_period("M")
        df_grouped = (
            df_marketing.groupby(["Origen", "año_mes"])
            .aggregate({"mql_id": "count", "first_contact_date": "first"})
            .reset_index()
        )

        fig = px.line(
            data_frame=df_grouped,
            x="first_contact_date",
            y="mql_id",
            title="Cantidad de contactos por canal",
            color="Origen",
            labels={
                "first_contact_date": "Fecha de contacto",
                "mql_id": "Cantidad de contactos",
            },
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_cerrados:
        df_closed_deals = pd.read_sql(
            sql="""
            SELECT 
                mql.origin AS origen,
                count(cd.mql_id)/count(mql.mql_id)*100 AS porcentaje
            FROM marketing_qualified_leads AS mql
            LEFT JOIN closed_deals AS cd ON (cd.mql_id = mql.mql_id)
            GROUP BY mql.origin
            ORDER BY porcentaje DESC;
            """,
            con=engine,
        )

        fig = px.bar(
            data_frame=df_closed_deals,
            x="origen",
            y="porcentaje",
            title="Porcentaje de cierre por canal de contacto",
            labels={"origen": "Origen", "porcentaje": "Porcentaje de cierre"},
        )

        st.plotly_chart(figure_or_data=fig, use_container_width=True)


with tab2:
    col_1, col_2 = st.columns(2)

    with col_1:
        df_category_score = pd.read_sql(
            """
            SELECT 
                avg(a.score) as prom_score, 
                c.category_name AS categoria
            FROM order_reviews AS a
                LEFT JOIN order_items AS b ON (a.order_id = b.order_id)
                LEFT JOIN products AS c ON (b.product_id = c.product_id)
            GROUP BY categoria
            ORDER BY prom_score DESC
            LIMIT 10;
            """,
            con=engine,
        )

        fig = px.bar(
            df_category_score,
            x="prom_score",
            y="categoria",
            orientation="h",
            title="Top 10 puntuación por categoría",
            labels={"categoria": "Categoría", "prom_score": "Puntuación promedio"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_2:
        df_reviews = pd.read_sql(
            """
            SELECT ordr.score AS score, o.purchase_timestamp AS fecha
            FROM order_reviews AS ordr
            LEFT JOIN orders AS o ON (ordr.order_id = o.order_id)
            WHERE o.purchase_timestamp > date("2016-12-31") 
            AND o.purchase_timestamp < date("2018-09-01");
            """,
            con=engine,
        )

        df_reviews["fecha"] = pd.to_datetime(df_reviews["fecha"])
        df_reviews.set_index("fecha", inplace=True)
        df_reviews = df_reviews.resample("M").aggregate({"score": "mean"}).reset_index()

        fig = px.line(
            df_reviews,
            x="fecha",
            y="score",
            title="Evolución de la puntuación promedio",
            labels={"fecha": "Fecha", "score": "Puntuación promedio"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

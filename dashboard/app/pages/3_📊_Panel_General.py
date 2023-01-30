from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk


st.set_page_config(page_title="Panel General", page_icon=":📈", layout="wide")

st.title(":mag_right: Visualización de Datos Generales")
st.text("A continuación se observara los resultados del análisis")
st.markdown("---")

st.sidebar.header("Panel General")
st.sidebar.write("ACA VA UN TEXTO EXPLICATIVO DE LA PAGINA")

engine = create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

tab_ventas, tab_clientes, tab_vendedores = st.tabs(["Ventas", "Clientes", "Vendedores"])

with tab_ventas:

    col_ventas, col_categorias = st.columns([1, 1])

    with col_ventas:
        df_ingresos = pd.read_sql(
            """
            SELECT 
                o.order_id AS id,
                o.purchase_timestamp AS fecha,
                sum(oi.price) AS total
            FROM order_items AS oi
            JOIN orders AS o ON(oi.order_id = o.order_id)
            WHERE o.purchase_timestamp < date("2018-09-01")
            GROUP BY o.order_id
            ORDER BY o.purchase_timestamp;
            """,
            con=engine,
        )
        df_ingresos["fecha"] = pd.to_datetime(df_ingresos["fecha"])
        df_ingresos.set_index(keys="fecha", inplace=True)

        df_ingresos = df_ingresos.resample("M").sum()

        fig = px.line(
            data_frame=df_ingresos,
            x=df_ingresos.index,
            y="total",
            title="Evolución mensual de las ventas",
            labels={"fecha": "Fecha", "total": "Total de ventas"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_categorias:

        df_categorias = pd.read_sql(
            """
            SELECT 
                p.category_name AS categoria,
                sum(oi.price) AS total
            FROM order_items AS oi
            LEFT JOIN products AS p ON (oi.product_id = p.product_id)
            GROUP BY p.category_name
            ORDER BY sum(oi.price) DESC
            LIMIT 5;""",
            con=engine,
        )
        fig = px.bar(
            df_categorias,
            x="categoria",
            y="total",
            title="Top 5 ventas por categoría",
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)


with tab_clientes:

    col_graph, col_fig = st.columns([3, 2])
    with col_graph:

        df_customers = pd.read_sql(
            sql="""
            SELECT 
                count(c.unique_id) AS weight,
                g.latitude AS latitude,
            	g.longitude AS longitude,
            	min(g.state) AS estado
            FROM customers AS c
            LEFT JOIN geolocations AS g ON (c.zip_code = g.zip_code)
            GROUP BY g.latitude, g.longitude;
        """,
            con=engine,
        )

        view = pdk.data_utils.compute_view(df_customers[["longitude", "latitude"]])
        view.zoom = 3.3
        view.pitch = 30

        st.pydeck_chart(
            pdk.Deck(
                map_style="dark",
                initial_view_state=view,
                tooltip=True,
                layers=[
                    pdk.Layer(
                        type="HeatmapLayer",
                        data=df_customers,
                        get_position="[longitude, latitude]",
                        get_weight="weight",
                    )
                ],
            ),
            use_container_width=True,
        )

    with col_fig:
        fig = px.bar(
            data_frame=df_customers.groupby(by="estado")
            .sum()
            .reset_index()
            .sort_values("weight", ascending=False)
            .head(5),
            x="estado",
            y="weight",
            title="Top 5 de estados por cantidad de clientes",
            labels={"weight": "Cantidad clientes", "estado": "Estado"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab_vendedores:

    col_graph, col_fig = st.columns([3, 2])
    with col_graph:
        df_sellers = pd.read_sql(
            sql="""
            SELECT 
                count(s.seller_id) AS weight,
                g.latitude AS latitude,
                g.longitude AS longitude,
                min(g.state) AS estado
            FROM sellers AS s
            LEFT JOIN geolocations AS g ON (s.zip_code = g.zip_code)
            GROUP BY g.latitude, g.longitude;
        """,
            con=engine,
        )

        view = pdk.data_utils.compute_view(df_sellers[["longitude", "latitude"]])
        view.zoom = 3.3
        view.pitch = 30

        st.pydeck_chart(
            pdk.Deck(
                map_style="dark",
                initial_view_state=view,
                tooltip=True,
                layers=[
                    pdk.Layer(
                        type="HeatmapLayer",
                        data=df_sellers,
                        get_position="[longitude, latitude]",
                        get_weight="weight",
                    )
                ],
            )
        )

    with col_fig:
        fig = px.bar(
            data_frame=df_sellers.groupby(by="estado")
            .sum()
            .reset_index()
            .sort_values("weight", ascending=False)
            .head(5),
            x="estado",
            y="weight",
            title="Top 5 de estados por cantidad de vendedores",
            labels={"weight": "Cantidad vendedores", "estado": "Estado"},
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

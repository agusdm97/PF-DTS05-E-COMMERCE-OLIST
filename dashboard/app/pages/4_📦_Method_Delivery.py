import sqlalchemy as sql
import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk

st.set_page_config(page_title="Method Payment - Delivery", page_icon="", layout="wide")

st.title(":mag_right: Visualización de análisis de métodos de pago y Entregas")
st.text("A continuación se observara los resultados del análisis")
st.markdown("---")

st.sidebar.header("Method Payment & Delivery")
st.sidebar.write("ACA VA UN TEXTO EXPLICATIVO DE LA PAGINA")

engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)


tab_metodos, tab_envios, tab_vend_comp = st.tabs(
    ["Métodos de pago", "Envíos", "Conexión vendedor - cliente"]
)


with tab_metodos:
    col_metodos, col_cuotas = st.columns(2)

    with col_metodos:
        df_payments = pd.read_sql(
            "order_payments",
            con=engine,
        )

        fig = px.pie(
            data_frame=df_payments.groupby(by="type")
            .count()
            .reset_index()
            .rename(columns={"value": "cantidad"}),
            values="cantidad",
            names="type",
            title="Proporción por método de pago",
            # color_discrete_sequence=px.colors.sequential.Inferno,
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_cuotas:

        fig = px.bar(
            data_frame=df_payments.groupby(by="installments")
            .count()
            .reset_index()
            .rename(columns={"value": "cantidad"}),
            x="installments",
            y="cantidad",
            range_x=[0.4, df_payments["installments"].max()],
            title="Distribución de pagos por cantidad de cuotas",
            labels={
                "cantidad": "Cantidad de pagos",
                "installments": "Cantidad de cuotas",
            },
        )

        st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab_envios:
    col_dias, col_peso = st.columns(2)

    with col_dias:
        delivery_rango = pd.read_sql(
            """
                SELECT count(d.dias) AS 'cantidad',
                    CASE
                        WHEN dias  < 4 THEN '< 4'
                        WHEN dias < 7 THEN '4 - 6'
                        WHEN dias < 11 THEN '7 - 10'
                        WHEN dias < 16 THEN '11 - 15'
                        WHEN dias < 20 THEN '16 - 20'
                        ELSE '> 20'
                    END
                    AS rango_entregas   
                FROM (
                    SELECT 
                        datediff(o.delivered_customer_date, o.purchase_timestamp ) AS dias
                    FROM orders AS o
                    WHERE o.status = 'delivered'
                ) AS d
                GROUP BY rango_entregas
                ORDER BY  
                    CASE rango_entregas
                        WHEN '< 4' THEN 1
                        WHEN '4 - 6' THEN 2
                        WHEN '7 - 10' THEN 3
                        WHEN '11 - 15' THEN 4
                        WHEN '16 - 20' THEN 5
                        WHEN '> 20' THEN 6
                        ELSE 7
                    END;""",
            con=engine,
        )

        fig = px.bar(
            delivery_rango,
            x="rango_entregas",
            y="cantidad",
            title="Productos entregados según rango de días",
            labels={
                "rango_entregas": "Rango de dias",
                "cantidad": "Cantidad de envíos",
            },
        )

        st.plotly_chart(figure_or_data=fig, use_container_width=True)

    with col_peso:
        delivery_peso = pd.read_sql(
            """
            SELECT avg(d.freight_value) AS 'promedio_flete',
                CASE
                    WHEN d.weight_g  < 501 THEN '< 0,5'
                    WHEN d.weight_g < 1001 THEN '0,5 - 1'
                    WHEN d.weight_g < 5001 THEN '1 - 5'
                    WHEN d.weight_g < 10001 THEN '5 - 10'
                    WHEN d.weight_g < 20001 THEN '10 - 20'
                    ELSE '> 20'
                END
                as rango_peso
            FROM (SELECT i.product_id, i.freight_value, p.weight_g
                FROM order_items AS i
                LEFT JOIN products as p ON(i.product_id = p.product_id)
                    ) AS d
            GROUP BY rango_peso
            ORDER BY 
                CASE rango_peso
                    WHEN  '< 0,5' THEN 1
                    WHEN  '0,5 - 1' THEN 2
                    WHEN  '1 - 5' THEN 3
                    WHEN  '5 - 10' THEN 4
                    WHEN  '10 - 20' THEN 5
                    WHEN  '> 20' THEN 6
                    ELSE 7
                END;""",
            con=engine,
        )

        fig = px.bar(
            data_frame=delivery_peso,
            x="rango_peso",
            y="promedio_flete",
            title="Promedio valor flete por rango de peso",
            labels={
                "rango_peso": "Rango de peso [kg]",
                "promedio_flete": "Precio promedio del flete [R$]",
            },
        )
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab_vend_comp:
    col_graph, col_text = st.columns([3, 2])
    with col_graph:
        df_cust_sell = pd.read_sql(
            sql="""
            SELECT 
                avg(cg.latitude) AS c_latitude,
                avg(cg.longitude) AS c_longitude,
                avg(sg.latitude) AS s_latitude,
                avg(sg.longitude) AS s_longitude
            FROM order_items AS oi
            LEFT JOIN sellers AS s ON(oi.seller_id = s.seller_id)
            LEFT JOIN orders AS ord ON (oi.order_id = ord.order_id)
            LEFT JOIN customers AS c ON (ord.customer_id = c.customer_id)
            LEFT JOIN geolocations AS cg ON (c.zip_code = cg.zip_code)
            LEFT JOIN geolocations AS sg ON (s.zip_code = sg.zip_code)
            GROUP BY oi.product_id, oi.seller_id, ord.customer_id
            ORDER BY rand()
            LIMIT 10000;
            """,
            con=engine,
        )
        view = pdk.data_utils.compute_view(df_cust_sell[["c_longitude", "c_latitude"]])
        view.zoom = 3
        view.pitch = 30
        st.pydeck_chart(
            pdk.Deck(
                map_style="dark",
                initial_view_state=view,
                tooltip=True,
                layers=[
                    pdk.Layer(
                        "ArcLayer",
                        data=df_cust_sell,
                        get_source_position=["s_longitude", "s_latitude"],
                        get_target_position=["c_longitude", "c_latitude"],
                        get_source_color=[0, 255, 0, 80],
                        get_target_color=[255, 0, 0, 80],
                    )
                ],
            )
        )
    with col_text:
        st.text("ACA VA EL TEXTO QUE EXPLICA EL GRAFICO")

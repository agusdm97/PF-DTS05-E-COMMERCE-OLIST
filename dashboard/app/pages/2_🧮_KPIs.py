import streamlit as st
import sqlalchemy as sql
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="KPIs", page_icon="🧮", layout="wide")

st.sidebar.header("KPIs")
st.title(":mag_right: Visualización de Datos KPIs")
st.subheader('Key Performance Indicator - (Indicadores Clave de desempeño)')

st.sidebar.write(
    """Herramientas para medir el desempeño y el progreso de Olist
                en relación a sus objetivos estratégicos."""
)

# Conexión con el data warehouse
engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)


st.title(":mag_right: KPIs")


# KPI Variación porcentual del volumen de ventas por mes (VVV)
st.markdown("---")
st.markdown("#### Variación porcentual del volumen de ventas (VVV)")
st.text("Objetivo: Evaluar el cambio de porcentual de las ventas por mes")
st.text("Frecuencia de evaluación: Mensual")
st.text("Valor objetivo: 10%")

kpi_vvv = pd.read_sql(
    """ 
        SELECT date(CONCAT(CAST(s.año AS UNSIGNED), '/', CAST(s.mes AS UNSIGNED), "/1")) AS fecha, sum(s.total) AS total
        FROM (
	        SELECT avg(year(o.purchase_timestamp)) AS año, avg(month(o.purchase_timestamp)) AS mes, sum(i.price) AS total
            FROM orders AS o
            RIGHT JOIN order_items AS i ON (o.order_id = i.order_id)
            WHERE o.status != "canceled" AND o.status != "unavailable"
            GROUP BY o.order_id
        ) AS s
        GROUP BY s.año, s.mes
        HAVING s.año = 2017
        ORDER BY s.año, s.mes DESC;""",
    con=engine,
)

kpi_vvv["diff"] = kpi_vvv["total"].pct_change(periods=-1)

left_column, right_column = st.columns([1, 1])

with left_column:

    st.metric(
        label="Total de ventas en R$",
        value=int(kpi_vvv.loc[0, "total"]),
        delta=int(kpi_vvv.loc[0, "total"] - kpi_vvv.loc[1, "total"]),
    )

with right_column:

    st.metric(
        label="Variación porcentual",
        value=format(kpi_vvv.loc[0, "diff"], ".2%"),
        delta=format(kpi_vvv.loc[0, "diff"] - kpi_vvv.loc[1, "diff"], ".2%"),
    )


# KPI Puntuación neta del promotor (PN)
st.markdown("---")
st.markdown("#### Puntuación neta del promotor (PN)")
st.text("Objetivo: Medir la satisfacción del cliente")
st.text("Frecuencia de evaluación: Trimestral")
st.text("Valor objetivo: 60%")

kpi_pn = pd.read_sql(
    """ 
    SELECT
	    year(orders.delivered_customer_date) AS año,
        month(orders.delivered_customer_date) AS mes,
        SUM(CASE WHEN score > 3 THEN 1 ELSE 0 END) AS reviews_positivas,
        SUM(CASE WHEN score <= 3 THEN 1 ELSE 0 END) AS reviews_negativas,
        COUNT(*) AS total_reviews
    FROM order_reviews
    LEFT JOIN orders ON (order_reviews.order_id = orders.order_id)
    WHERE year(orders.delivered_customer_date) = 2017
    GROUP BY year(orders.delivered_customer_date), month(orders.delivered_customer_date)
    ORDER BY year(orders.delivered_customer_date), month(orders.delivered_customer_date) DESC
    LIMIT 2;
    """,
    con=engine,
)

pct_act_rp = kpi_pn.loc[0, "reviews_positivas"] / kpi_pn.loc[0, "total_reviews"]
pct_ant_rp = kpi_pn.loc[1, "reviews_positivas"] / kpi_pn.loc[1, "total_reviews"]

pct_act_rn = kpi_pn.loc[0, "reviews_negativas"] / kpi_pn.loc[0, "total_reviews"]
pct_ant_rn = kpi_pn.loc[1, "reviews_negativas"] / kpi_pn.loc[1, "total_reviews"]

pct_act_pn = pct_act_rp - pct_act_rn
pct_ant_pn = pct_ant_rp - pct_ant_rn

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.metric(
        label="Porcentaje Calificaciones Positivas",
        value=format(pct_act_rp, ".2%"),
        delta=format(pct_act_rp - pct_ant_rp, ".2%"),
    )

with middle_column:
    st.metric(
        label="Porcentaje Calificaciones Negativas",
        value=format(pct_act_rn, ".2%"),
        delta=format(pct_act_rn - pct_ant_rn, ".2%"),
    )

with right_column:
    st.metric(
        label="Puntuación Neta",
        value=format(pct_act_pn, ".2%"),
        delta=format(pct_act_pn - pct_ant_pn, ".2%"),
    )


# KPI Fidelidad del cliente
st.markdown("---")
st.markdown("#### Fidelidad del Cliente (FC)")
st.text("Objetivo: Medir la tasa de clientes que vuelven a comprar")
st.text("Frecuencia de evaluación: Trimestral")
st.text("Valor objetivo: 5%")

kpi_fc = pd.read_sql(
    sql=""" 
    WITH current_quarter AS ( SELECT 2017 AS year, 4 AS quarter)
    SELECT 
	    (SELECT year FROM current_quarter) AS año,
	    (SELECT quarter FROM current_quarter) AS mes, 
        COUNT(customers.unique_id) AS clientes_fieles
    FROM orders
    LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    AND quarter(orders.purchase_timestamp) = (SELECT quarter FROM current_quarter)
    AND customers.unique_id IN (
	    SELECT customers.unique_id 
        FROM orders 
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
	    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
	    AND quarter(orders.purchase_timestamp) = (SELECT quarter - 1 FROM current_quarter)
        AND orders.status != "canceled" AND orders.status != "unavailable") 
    AND orders.status != "canceled" AND orders.status != "unavailable"
    UNION 
    SELECT 
    	(SELECT year FROM current_quarter) AS año,
    	(SELECT quarter - 1 FROM current_quarter) AS mes, 
        COUNT(customers.unique_id) AS clientes_fieles
    FROM orders
    LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    AND quarter(orders.purchase_timestamp) = (SELECT quarter - 1 FROM current_quarter)
    AND customers.unique_id IN (
    	SELECT customers.unique_id 
        FROM orders 
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
    	WHERE  year(orders.purchase_timestamp) = (SELECT year FROM current_quarter)
    	AND quarter(orders.purchase_timestamp) = (SELECT quarter - 2 FROM current_quarter)
        AND orders.status != "canceled" AND orders.status != "unavailable") 
    AND orders.status != "canceled" AND orders.status != "unavailable";
    """,
    con=engine,
)

kpi_fc_total = pd.read_sql(
    sql=""" 
        SELECT 
        	year(orders.purchase_timestamp) AS año, 
            quarter(orders.purchase_timestamp) AS mes, 
            count(DISTINCT customers.unique_id) AS cantidad_total_clientes
        FROM orders
        LEFT JOIN customers ON (customers.customer_id = orders.customer_id)
        WHERE  year(orders.purchase_timestamp) = 2017
        AND orders.status != "canceled" AND orders.status != "unavailable"
        GROUP BY año, mes
        ORDER BY año, mes DESC
        LIMIT 2;
    """,
    con=engine,
)

pct_act_fc = (
    kpi_fc.loc[0, "clientes_fieles"] / kpi_fc_total.loc[0, "cantidad_total_clientes"]
)

pct_ant_fc = (
    kpi_fc.loc[1, "clientes_fieles"] / kpi_fc_total.loc[1, "cantidad_total_clientes"]
)

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.metric(
        label="Cantidad clientes fieles",
        value=int(kpi_fc.loc[0, "clientes_fieles"]),
        delta=int(kpi_fc.loc[0, "clientes_fieles"] - kpi_fc.loc[1, "clientes_fieles"]),
    )

with middle_column:
    st.metric(
        label="Cantidad clientes total",
        value=int(kpi_fc_total.loc[0, "cantidad_total_clientes"]),
        delta=int(
            kpi_fc_total.loc[0, "cantidad_total_clientes"]
            - kpi_fc_total.loc[1, "cantidad_total_clientes"]
        ),
    )

with right_column:
    st.metric(
        label="Porcentaje fidelidad de clientes",
        value=format(pct_act_fc, ".2%"),
        delta=format(pct_act_fc - pct_ant_fc, ".2%"),
    )


# KPI Tasa de Conversión (TC)
st.markdown("---")
st.markdown("#### Tasa de Conversión (TC)")
st.text(
    "Objetivo: Determinar la cantidad vendedores potenciales que se unen a la empresa"
)
st.text("Frecuencia de evaluación: Trimestral")
st.text("Valor objetivo: 15%")
kpi_tc = pd.read_sql(
    """ 
    SELECT 
        max(year(marketing_qualified_leads.first_contact_date)) AS año,
        max(quarter(marketing_qualified_leads.first_contact_date)) AS mes,
        count(marketing_qualified_leads.mql_id) AS cantidad_interesados,
        count(closed_deals.mql_id) AS cantidad_convertidos,
        count(closed_deals.mql_id)/count(marketing_qualified_leads.mql_id) AS tasa_conversion
    FROM marketing_qualified_leads
    LEFT JOIN closed_deals ON (marketing_qualified_leads.mql_id = closed_deals.mql_id)
    WHERE year(marketing_qualified_leads.first_contact_date) <= 2017
    AND quarter(marketing_qualified_leads.first_contact_date) <= 4
    UNION
    SELECT 
    	max(year(marketing_qualified_leads.first_contact_date)) AS año,
        max(quarter(marketing_qualified_leads.first_contact_date)) AS mes,
        count(marketing_qualified_leads.mql_id) AS cantidad_interesados,
        count(closed_deals.mql_id) AS cantidad_convertidos,
        count(closed_deals.mql_id)/count(marketing_qualified_leads.mql_id) AS tasa_conversion
    FROM marketing_qualified_leads
    LEFT JOIN closed_deals ON (marketing_qualified_leads.mql_id = closed_deals.mql_id)
    WHERE year(marketing_qualified_leads.first_contact_date) <= 2017
    AND quarter(marketing_qualified_leads.first_contact_date) <= 3;
    """,
    con=engine,
)

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.metric(
        label="Cantidad de interesados",
        value=int(kpi_tc.loc[0, "cantidad_interesados"]),
        delta=int(
            kpi_tc.loc[0, "cantidad_interesados"]
            - kpi_tc.loc[1, "cantidad_interesados"]
        ),
    )

with middle_column:
    st.metric(
        label="Cantidad de convertidos",
        value=int(kpi_tc.loc[0, "cantidad_convertidos"]),
        delta=int(
            kpi_tc.loc[0, "cantidad_convertidos"]
            - kpi_tc.loc[1, "cantidad_convertidos"]
        ),
    )

with right_column:
    st.metric(
        label="Tasa de conversión",
        value=format(kpi_tc.loc[0, "tasa_conversion"], ".2%"),
        delta=format(
            kpi_tc.loc[0, "tasa_conversion"] - kpi_tc.loc[1, "tasa_conversion"], ".2%"
        ),
    )


# KPI Puntualidad de la entrega (PE)
st.markdown("---")
st.markdown("#### Puntualidad de la Entrega (PE)")
st.text("Objetivo: Medir el porcentaje de entregas que se realizan a tiempo.")
st.text("Frecuencia de evaluación: Mensual")
st.text("Valor objetivo: 95%")

kpi_pe = pd.read_sql(
    """ 
    SELECT 
    	year(ord.fecha) AS año,
        month(ord.fecha) AS mes,
        sum(ord.a_tiempo) AS cantidad_a_tiempo,
        count(*) AS cantidad_total,
        sum(ord.a_tiempo)/count(*) AS puntualidad
    FROM (
    	SELECT
    		purchase_timestamp AS fecha,
            (CASE WHEN datediff(estimated_delivery_date, delivered_customer_date) >= 0 THEN 1 ELSE 0 END) AS a_tiempo
    	FROM orders
        WHERE status = "delivered" AND year(purchase_timestamp) = 2017
    ) AS ord
    GROUP BY año, mes
    ORDER BY año, mes DESC
    LIMIT 2;
    """,
    con=engine,
)


left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.metric(
        label="Cantidad total de pedidos",
        value=int(kpi_pe.loc[0, "cantidad_total"]),
        delta=int(kpi_pe.loc[0, "cantidad_total"] - kpi_pe.loc[1, "cantidad_total"]),
    )

with middle_column:
    st.metric(
        label="Cantidad de pedidos entregados puntualmente",
        value=int(kpi_pe.loc[0, "cantidad_a_tiempo"]),
        delta=int(
            kpi_pe.loc[0, "cantidad_a_tiempo"] - kpi_pe.loc[1, "cantidad_a_tiempo"]
        ),
    )

with right_column:
    st.metric(
        label="Puntualidad de Entrega",
        value=format(kpi_pe.loc[0, "puntualidad"], ".2%"),
        delta=format(
            kpi_pe.loc[0, "puntualidad"] - kpi_pe.loc[1, "puntualidad"], ".2%"
        ),
    )

# KPI: Tiempo total del proceso (TTP)
st.markdown("---")
st.markdown("#### Tiempo total del proceso (TTP)")
st.text("Objetivo: Optimizar los tiempos de compra y envío.")
st.text("Frecuencia de evaluación: Mensual")
st.text("Valor objetivo: 8 días")

kpi_ttp = pd.read_sql(
    sql="""
        SELECT 
            year(purchase_timestamp) AS año,
            month(purchase_timestamp) AS mes,
            avg(datediff(delivered_customer_date,purchase_timestamp)) AS tiempo_prom
        FROM orders
        WHERE year(purchase_timestamp) = 2017 AND status = "delivered"
        GROUP BY año, mes
        ORDER BY año, mes DESC;
    """,
    con=engine,
)

graf_col, kpi_col = st.columns([2, 1])

with graf_col:
    fig = px.area(
        data_frame=kpi_ttp,
        x="mes",
        y="tiempo_prom",
        title="Tiempo promedio de envío",
        range_y=[6, 16],
        labels={"mes": "Mes", "tiempo_prom": "Tiempo promedio"},
    )
    st.plotly_chart(figure_or_data=fig)

with kpi_col:
    st.metric(
        label="Puntualidad de Entrega",
        value=round(float(kpi_ttp.loc[0, "tiempo_prom"]), 2),
        delta=round(
            float(kpi_ttp.loc[0, "tiempo_prom"] - kpi_ttp.loc[1, "tiempo_prom"]), 2
        ),
        delta_color="inverse",
    )
st.markdown("---")

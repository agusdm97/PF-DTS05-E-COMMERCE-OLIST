import streamlit as st
import pandas as pd
import sqlalchemy as sql
import pickle as pkl
import datetime as dt
import plotly.express as px


st.title("Forecasting Sales")
tab1, tab2 = st.tabs(["ARIMA", "Prophet"])

engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

with open("models/total_model.pkl", "rb") as f:
    total_model = pkl.load(f)

with open("models/model_prophet.pkl", "rb") as f:
    model_prophet = pkl.load(f)

df_history = pd.read_sql(
    """
    SELECT
        o.purchase_timestamp AS time,
        oi.price AS sales
    FROM orders AS o 
    LEFT JOIN order_items AS oi ON (o.order_id = oi.order_id)
    """,
    con=engine,
)
df_history.dropna(inplace=True)
df_history["time"] = pd.to_datetime(df_history["time"])
df_history.set_index("time", inplace=True)
df_history_w = df_history["sales"].resample("W").sum().reset_index()
df_history_w["type"] = "history"

future = [dt.date(2018, 9, 9) + dt.timedelta(days=7) * i for i in range(1, 40)]


with tab1:
    date = st.select_slider("Seleccione la fecha de predicción:", options=future, key=1)

    forecast_arima = total_model.predict(start=87, end=date, dynamic=True)
    forecast_arima = forecast_arima.reset_index()
    forecast_arima.rename(
        columns={"index": "time", "predicted_mean": "sales"}, inplace=True
    )
    forecast_arima["type"] = "forecast"
    df = pd.concat([df_history_w, forecast_arima.loc[1:]], axis=0, ignore_index=True)

    fig = px.line(
        data_frame=df,
        x="time",
        y="sales",
        color="type",
        title="Predicción de ventas",
        labels={"time": "Fecha", "sales": "Ventas"},
    )
    st.plotly_chart(figure_or_data=fig, use_container_width=True)

with tab2:
    date = st.select_slider("Seleccione la fecha de predicción:", options=future, key=2)
    weeks = future.index(date)

    future_prophet = model_prophet.make_future_dataframe(periods=weeks + 23, freq="W")
    forecast_prophet = model_prophet.predict(future_prophet)

    forecast_prophet = forecast_prophet[["ds", "yhat"]]
    forecast_prophet.rename(columns={"ds": "time", "yhat": "sales"}, inplace=True)
    forecast_prophet["type"] = "forecast"
    df = pd.concat([df_history_w, forecast_prophet.loc[88:]], axis=0, ignore_index=True)

    fig = px.line(
        data_frame=df,
        x="time",
        y="sales",
        color="type",
        title="Predicción de ventas",
        labels={"time": "Fecha", "sales": "Ventas"},
    )
    st.plotly_chart(figure_or_data=fig, use_container_width=True)

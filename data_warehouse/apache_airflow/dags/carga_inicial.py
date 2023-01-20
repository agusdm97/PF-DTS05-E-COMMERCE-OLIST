from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sqlalchemy as sql

from etl import (
    geolocation,
    customer,
    seller,
    product,
    marketing_qualified_lead,
    closed_deal,
    order,
    order_item,
    order_payment,
    order_review,
)

engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

paths = {
    "zip_codes": "datasets/br_zip_code.csv",
    "closed_deals": "datasets/olist_closed_deals_dataset.csv",
    "customers": "datasets/olist_customers_dataset.csv",
    "geolocations": "datasets/olist_geolocation_dataset.csv",
    "marketing_qualified_leads": "datasets/olist_marketing_qualified_leads_dataset.csv",
    "order_items": "datasets/olist_order_items_dataset.csv",
    "order_payments": "datasets/olist_order_payments_dataset.csv",
    "order_reviews": "datasets/olist_order_reviews_dataset.csv",
    "orders": "datasets/olist_orders_dataset.csv",
    "products": "datasets/olist_products_dataset.csv",
    "sellers": "datasets/olist_sellers_dataset.csv",
}


def geolocation_etl(paths, engine):

    geolocation.etl(
        data_path=paths.get("geolocations"),
        zip_code_data_path=paths.get("zip_codes"),
        customer_data_path=paths.get("customers"),
        seller_data_path=paths.get("sellers"),
        engine=engine,
    )


def marketing_qualified_leads_etl(paths, engine):

    marketing_qualified_lead.etl(
        data_path=paths.get("marketing_qualified_leads"),
        engine=engine,
    )


def products_etl(paths, engine):

    product.etl(
        data_path=paths.get("products"),
        engine=engine,
    )


def closed_deals_etl(paths, engine):

    closed_deal.etl(
        data_path=paths.get("closed_deals"),
        engine=engine,
    )


def customers_etl(paths, engine):

    customer.etl(
        data_path=paths.get("customers"),
        engine=engine,
    )


def sellers_etl(paths, engine):

    seller.etl(
        data_path=paths.get("sellers"),
        engine=engine,
    )


def orders_etl(paths, engine):

    order.etl(
        data_path=paths.get("orders"),
        engine=engine,
    )


def order_items_etl(paths, engine):

    order_item.etl(
        data_path=paths.get("order_items"),
        engine=engine,
    )


def order_payments_etl(paths, engine):

    order_payment.etl(
        data_path=paths.get("order_payments"),
        engine=engine,
    )


def order_reviews_etl(paths, engine):

    order_review.etl(
        data_path=paths.get("order_reviews"),
        engine=engine,
    )


default_args = {
    "owner": "Data Insights",
    "retries": 5,
    "retry_delay": timedelta(minutes=2),
}

op_kwargs = {
    "paths": paths,
    "engine": engine,
}

with DAG(
    dag_id="carga_inicial_v2",
    description="DAG inicial de la ETL",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@once",
    default_args=default_args,
) as dag:
    task_1 = PythonOperator(
        task_id="geolocation_etl", python_callable=geolocation_etl, op_kwargs=op_kwargs
    )
    task_2 = PythonOperator(
        task_id="marketing_qualified_leads_etl",
        python_callable=marketing_qualified_leads_etl,
        op_kwargs=op_kwargs,
    )
    task_3 = PythonOperator(
        task_id="products_etl", python_callable=products_etl, op_kwargs=op_kwargs
    )
    task_4 = PythonOperator(
        task_id="closed_deals_etl",
        python_callable=closed_deals_etl,
        op_kwargs=op_kwargs,
    )
    task_5 = PythonOperator(
        task_id="customers_etl", python_callable=customers_etl, op_kwargs=op_kwargs
    )
    task_6 = PythonOperator(
        task_id="sellers_etl", python_callable=sellers_etl, op_kwargs=op_kwargs
    )
    task_7 = PythonOperator(
        task_id="orders_etl", python_callable=orders_etl, op_kwargs=op_kwargs
    )
    task_8 = PythonOperator(
        task_id="order_items_etl", python_callable=order_items_etl, op_kwargs=op_kwargs
    )
    task_9 = PythonOperator(
        task_id="order_payments_etl",
        python_callable=order_payments_etl,
        op_kwargs=op_kwargs,
    )
    task_10 = PythonOperator(
        task_id="order_reviews_etl",
        python_callable=order_reviews_etl,
        op_kwargs=op_kwargs,
    )

    task_1.set_downstream([task_5, task_6])
    task_2.set_downstream(task_4)
    task_5.set_downstream(task_7)
    task_8.set_upstream([task_3, task_6, task_7])
    task_9.set_upstream(task_7)
    task_10.set_upstream(task_7)

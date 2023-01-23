from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sqlalchemy as sql
from minio import Minio
from minio.error import S3Error
from time import sleep

from etl_module import (
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

client = Minio(
    endpoint="minio:9000",
    access_key="root",
    secret_key="password",
    secure=False,
)

engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)

paths = {
    "zip_codes": "temp/br_zip_code.csv",
    "closed_deals": "temp/olist_closed_deals_dataset.csv",
    "customers": "temp/olist_customers_dataset.csv",
    "geolocations": "temp/olist_geolocation_dataset.csv",
    "marketing_qualified_leads": "temp/olist_marketing_qualified_leads_dataset.csv",
    "order_items": "temp/olist_order_items_dataset.csv",
    "order_payments": "temp/olist_order_payments_dataset.csv",
    "order_reviews": "temp/olist_order_reviews_dataset.csv",
    "orders": "temp/olist_orders_dataset.csv",
    "products": "temp/olist_products_dataset.csv",
    "sellers": "temp/olist_sellers_dataset.csv",
}


def file_sensor(file_name: str, bucket_name: str, client: Minio):
    while True:
        if client.bucket_exists(bucket_name):
            try:
                client.fget_object(
                    bucket_name=bucket_name,
                    object_name=file_name,
                    file_path=f"temp/{file_name}",
                )
            except S3Error:
                print(
                    f"The file {file_name} does not exist in the bucket {bucket_name}"
                )
            else:
                break
        else:
            print(f"The bucket {bucket_name} does not exist")
        sleep(20)


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
    dag_id="carga_inicial",
    description="DAG inicial de la ETL",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@once",
    default_args=default_args,
) as dag:
    s_geolocations = PythonOperator(
        task_id="geolocation_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_geolocation_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    s_customers = PythonOperator(
        task_id="customer_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_customers_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    s_sellers = PythonOperator(
        task_id="seller_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_sellers_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    s_zip_codes = PythonOperator(
        task_id="zip_code_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "br_zip_code.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_geolocations = PythonOperator(
        task_id="geolocation_etl", python_callable=geolocation_etl, op_kwargs=op_kwargs
    )

    s_mql = PythonOperator(
        task_id="marketing_qualified_leads_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_marketing_qualified_leads_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_mql = PythonOperator(
        task_id="marketing_qualified_leads_etl",
        python_callable=marketing_qualified_leads_etl,
        op_kwargs=op_kwargs,
    )

    s_products = PythonOperator(
        task_id="products_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_products_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_products = PythonOperator(
        task_id="products_etl", python_callable=products_etl, op_kwargs=op_kwargs
    )

    s_closed_deals = PythonOperator(
        task_id="closed_deals_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_closed_deals_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_closed_deals = PythonOperator(
        task_id="closed_deals_etl",
        python_callable=closed_deals_etl,
        op_kwargs=op_kwargs,
    )

    t_customers = PythonOperator(
        task_id="customers_etl", python_callable=customers_etl, op_kwargs=op_kwargs
    )

    t_sellers = PythonOperator(
        task_id="sellers_etl", python_callable=sellers_etl, op_kwargs=op_kwargs
    )

    s_orders = PythonOperator(
        task_id="orders_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_orders_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_orders = PythonOperator(
        task_id="orders_etl", python_callable=orders_etl, op_kwargs=op_kwargs
    )

    s_order_items = PythonOperator(
        task_id="order_items_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_order_items_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_order_items = PythonOperator(
        task_id="order_items_etl", python_callable=order_items_etl, op_kwargs=op_kwargs
    )

    s_order_payments = PythonOperator(
        task_id="order_payments_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_order_payments_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_order_payments = PythonOperator(
        task_id="order_payments_etl",
        python_callable=order_payments_etl,
        op_kwargs=op_kwargs,
    )

    s_order_reviews = PythonOperator(
        task_id="order_reviews_sensor",
        python_callable=file_sensor,
        op_kwargs={
            "file_name": "olist_order_reviews_dataset.csv",
            "bucket_name": "airflow",
            "client": client,
        },
    )

    t_order_reviews = PythonOperator(
        task_id="order_reviews_etl",
        python_callable=order_reviews_etl,
        op_kwargs=op_kwargs,
    )

    t_geolocations.set_upstream([s_geolocations, s_sellers, s_customers, s_zip_codes])
    t_geolocations.set_downstream([t_sellers, t_customers])

    t_customers.set_downstream(s_orders)
    t_orders.set_upstream(s_orders)
    t_order_payments.set_upstream(s_order_payments)
    t_order_reviews.set_upstream(s_order_reviews)
    t_orders.set_downstream([s_order_payments, s_order_reviews])

    t_products.set_upstream(s_products)

    t_order_items.set_upstream(s_order_items)
    s_order_items.set_upstream([t_orders, t_sellers, t_products])

    t_mql.set_upstream(s_mql)
    t_mql.set_downstream(s_closed_deals)
    t_closed_deals.set_upstream(s_closed_deals)

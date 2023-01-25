from typing import Any
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sqlalchemy as sql
from minio import Minio
from time import sleep
import pandas as pd
import os


client = Minio(
    endpoint="minio:9000",
    access_key="root",
    secret_key="password",
    secure=False,
)

engine = sql.create_engine(
    "mysql+pymysql://root:password@mysql:3306/data_warehouse_olist?charset=utf8mb4"
)


def files_sensor(bucket_name: str, client: Minio, **kwargs):
    previous_objects = []
    present_objects = []
    minutes = 0
    while True:
        if client.bucket_exists(bucket_name):
            objects = client.list_objects(bucket_name)
            for obj in objects:
                present_objects.append(obj.object_name)

            if present_objects:
                if present_objects == previous_objects:
                    minutes += 1
                previous_objects = present_objects.copy()
                present_objects.clear()
            else:
                minutes = 0

            if minutes == 4:
                for file_name in previous_objects:
                    client.fget_object(
                        bucket_name=bucket_name,
                        object_name=file_name,
                        file_path=f"temp/{file_name}",
                    )
                    kwargs["ti"].xcom_push(key=file_name, value=f"temp/{file_name}")
                    print(f"The file {file_name} was downloaded into temp/{file_name}")
                break
        else:
            print(f"The bucket {bucket_name} does not exist")
        sleep(60)


def check_primary_key(
    file_name: str, primary_key: str, engine: sql.engine.Engine, **kwargs
):
    data_path = kwargs["ti"].xcom_pull(key=file_name, task_ids="files_sensor")

    if data_path is None:
        return True

    df = pd.read_csv(filepath_or_buffer=data_path, usecols=[primary_key])

    table_name = file_name.split(".")[0]

    df_pk = pd.read_sql(f"SELECT {primary_key} FROM {table_name};", con=engine)

    assert (
        len(df_pk[df_pk[primary_key].isin(df[primary_key])]) == 0
    ), f"The file {file_name} violates the primary key constrain of {table_name}"


def check_foreign_keys(
    file_name: str,
    foreign_keys: Any,
    engine: sql.engine.Engine,
    **kwargs,
):
    data_path = kwargs["ti"].xcom_pull(key=file_name, task_ids="files_sensor")

    if data_path is None:
        return True

    cols = []
    retries = 4

    for _, column_name in foreign_keys:
        cols.append(column_name)

    df = pd.read_csv(filepath_or_buffer=data_path, usecols=cols)
    while retries != 0:
        for table_name, column_name in foreign_keys:
            df_fk = pd.read_sql(f"SELECT {column_name} FROM {table_name};", con=engine)

            if len(df[df[column_name].isin(df_fk[column_name])]) != len(df):
                retries -= 1
                break
        else:
            break
        sleep(20)


def load_data(file_name: str, engine: sql.engine.Engine, **kwargs):

    data_path = kwargs["ti"].xcom_pull(key=file_name, task_ids="files_sensor")

    if data_path is None:
        return True

    df = pd.read_csv(filepath_or_buffer=data_path, parse_dates=True)

    table_name = file_name.split(".")[0]

    df.to_sql(
        name=table_name,
        con=engine,
        index=False,
        if_exists="append",
    )

    os.unlink(data_path)


default_args = {
    "owner": "Data Insights",
    "retries": 5,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="carga_incremental",
    description="DAG de carga incremental",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:
    t_files_sensor = PythonOperator(
        task_id="files_sensor",
        python_callable=files_sensor,
        provide_context=True,
        op_kwargs={
            "bucket_name": "test",
            "client": client,
        },
    )

    cpk_geolocations = PythonOperator(
        task_id="cpk_geolocations",
        python_callable=check_primary_key,
        provide_context=True,
        op_kwargs={
            "file_name": "geolocations.csv",
            "primary_key": "zip_code",
            "engine": engine,
        },
    )

    l_geolocations = PythonOperator(
        task_id="l_geolocations",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "geolocations.csv",
            "engine": engine,
        },
    )

    cpk_customers = PythonOperator(
        task_id="cpk_customers",
        python_callable=check_primary_key,
        provide_context=True,
        op_kwargs={
            "file_name": "customers.csv",
            "primary_key": "customer_id",
            "engine": engine,
        },
    )

    cfk_customers = PythonOperator(
        task_id="cfk_customers",
        python_callable=check_foreign_keys,
        provide_context=True,
        op_kwargs={
            "file_name": "customers.csv",
            "foreign_keys": [("geolocations", "zip_code")],
            "engine": engine,
        },
    )

    l_customers = PythonOperator(
        task_id="l_customers",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "customers.csv",
            "engine": engine,
        },
    )

    cpk_sellers = PythonOperator(
        task_id="cpk_sellers",
        python_callable=check_primary_key,
        provide_context=True,
        op_kwargs={
            "file_name": "sellers.csv",
            "primary_key": "seller_id",
            "engine": engine,
        },
    )

    cfk_sellers = PythonOperator(
        task_id="cfk_sellers",
        python_callable=check_foreign_keys,
        provide_context=True,
        op_kwargs={
            "file_name": "sellers.csv",
            "foreign_keys": [("geolocations", "zip_code")],
            "engine": engine,
        },
    )

    l_sellers = PythonOperator(
        task_id="l_sellers",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "sellers.csv",
            "engine": engine,
        },
    )

    cpk_products = PythonOperator(
        task_id="cpk_products",
        python_callable=check_primary_key,
        provide_context=True,
        op_kwargs={
            "file_name": "products.csv",
            "primary_key": "product_id",
            "engine": engine,
        },
    )

    l_products = PythonOperator(
        task_id="l_products",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "products.csv",
            "engine": engine,
        },
    )

    cpk_marketing_qualified_leads = PythonOperator(
        task_id="cpk_marketing_qualified_leads",
        python_callable=check_primary_key,
        provide_context=True,
        op_kwargs={
            "file_name": "marketing_qualified_leads.csv",
            "primary_key": "mql_id",
            "engine": engine,
        },
    )

    l_marketing_qualified_leads = PythonOperator(
        task_id="l_marketing_qualified_leads",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "marketing_qualified_leads.csv",
            "engine": engine,
        },
    )

    cfk_closed_deals = PythonOperator(
        task_id="cfk_closed_deals",
        python_callable=check_foreign_keys,
        provide_context=True,
        op_kwargs={
            "file_name": "closed_deals.csv",
            "foreign_keys": [("marketing_qualified_leads", "mql_id")],
            "engine": engine,
        },
    )

    l_closed_deals = PythonOperator(
        task_id="l_closed_deals",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "closed_deals.csv",
            "engine": engine,
        },
    )

    cpk_orders = PythonOperator(
        task_id="cpk_orders",
        python_callable=check_primary_key,
        provide_context=True,
        op_kwargs={
            "file_name": "orders.csv",
            "primary_key": "order_id",
            "engine": engine,
        },
    )

    cfk_orders = PythonOperator(
        task_id="cfk_orders",
        python_callable=check_foreign_keys,
        provide_context=True,
        op_kwargs={
            "file_name": "orders.csv",
            "foreign_keys": [("customers", "customer_id")],
            "engine": engine,
        },
    )

    l_orders = PythonOperator(
        task_id="l_orders",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "orders.csv",
            "engine": engine,
        },
    )

    cfk_order_items = PythonOperator(
        task_id="cfk_order_items",
        python_callable=check_foreign_keys,
        provide_context=True,
        op_kwargs={
            "file_name": "order_items.csv",
            "foreign_keys": [
                ("orders", "order_id"),
                ("products", "product_id"),
                ("sellers", "seller_id"),
            ],
            "engine": engine,
        },
    )

    l_order_items = PythonOperator(
        task_id="l_order_items",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "order_items.csv",
            "engine": engine,
        },
    )

    cfk_order_payments = PythonOperator(
        task_id="cfk_order_payments",
        python_callable=check_foreign_keys,
        provide_context=True,
        op_kwargs={
            "file_name": "order_payments.csv",
            "foreign_keys": [
                ("orders", "order_id"),
            ],
            "engine": engine,
        },
    )

    l_order_payments = PythonOperator(
        task_id="l_order_payments",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "order_payments.csv",
            "engine": engine,
        },
    )

    cfk_order_reviews = PythonOperator(
        task_id="cfk_order_reviews",
        python_callable=check_foreign_keys,
        provide_context=True,
        op_kwargs={
            "file_name": "order_reviews.csv",
            "foreign_keys": [
                ("orders", "order_id"),
            ],
            "engine": engine,
        },
    )

    l_order_reviews = PythonOperator(
        task_id="l_order_reviews",
        python_callable=load_data,
        provide_context=True,
        op_kwargs={
            "file_name": "order_reviews.csv",
            "engine": engine,
        },
    )

    t_files_sensor.set_downstream(
        [
            cpk_geolocations,
            cpk_customers,
            cfk_customers,
            cpk_sellers,
            cfk_sellers,
            cpk_products,
            cpk_marketing_qualified_leads,
            cfk_closed_deals,
            cpk_orders,
            cfk_orders,
            cfk_order_items,
            cfk_order_reviews,
            cfk_order_payments,
        ]
    )
    l_geolocations.set_upstream(cpk_geolocations)
    l_customers.set_upstream([cpk_customers, cfk_customers])
    l_sellers.set_upstream([cpk_sellers, cfk_sellers])
    l_products.set_upstream(cpk_products)
    l_marketing_qualified_leads.set_upstream(cpk_marketing_qualified_leads)
    l_closed_deals.set_upstream(cfk_closed_deals)
    l_orders.set_upstream([cpk_orders, cfk_orders])
    l_order_items.set_upstream(cfk_order_items)
    l_order_reviews.set_upstream(cfk_order_reviews)
    l_order_payments.set_upstream(cfk_order_payments)

import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:
    """
    Esta función realiza una ETL en un archivo CSV y carga los datos en una tabla de una base de datos.

    Args:
    - data_path (str): La ruta del archivo CSV a leer.
    - engine (sqlalchemy.engine.Engine): El objeto Engine de SQLAlchemy para conectarse a la base de datos.

    Returns: None
    """

    # Leer archivo CSV
    df = pd.read_csv(
        filepath_or_buffer=data_path,
        date_parser=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    # Renombrar las columnas
    df.rename(
        columns={
            "order_status": "status",
            "order_purchase_timestamp": "purchase_timestamp",
            "order_approved_at": "approved_at",
            "order_delivered_carrier_date": "delivered_carrier_date",
            "order_delivered_customer_date": "delivered_customer_date",
            "order_estimated_delivery_date": "estimated_delivery_date",
        },
        inplace=True,
    )
    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "orders" si no existe
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`orders` (
                `order_id` VARCHAR(45) NOT NULL,
                `customer_id` VARCHAR(45) NOT NULL,
                `status` VARCHAR(45) NOT NULL,
                `purchase_timestamp` DATE NOT NULL,
                `approved_at` DATE,
                `delivered_carrier_date` DATE,
                `delivered_customer_date` DATE,
                `estimated_delivery_date` DATE,
                PRIMARY KEY (`order_id`),
                FOREIGN KEY (`customer_id`) REFERENCES `data_warehouse_olist`.`customers` (`customer_id`)
                );
                """
        )

    # Cargar los datos en la tabla "orders"
    df.to_sql(
        name="orders",
        con=engine,
        index=False,
        if_exists="append",
    )

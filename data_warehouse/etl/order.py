import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.columns = df.columns.str.removeprefix("order_")

    cols = [
        "purchase_timestamp",
        "approved_at",
        "delivered_carrier_date",
        "delivered_customer_date",
        "estimated_delivery_date",
    ]

    for col in cols:
        df[col] = pd.to_datetime(df[col])

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`orders` (
                `id` VARCHAR(45) NOT NULL,
                `customer_id` VARCHAR(45) NOT NULL,
                `status` VARCHAR(45) NOT NULL,
                `purchase_timestamp` DATE NOT NULL,
                `approved_at` DATE,
                `delivered_carrier_date` DATE,
                `delivered_customer_date` DATE,
                `estimated_delivery_date` DATE,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`customer_id`) REFERENCES `data_warehouse_olist`.`customers` (`id`)
                );
                """
        )

    df.to_sql(
        name="orders",
        con=engine,
        index=False,
        if_exists="append",
    )

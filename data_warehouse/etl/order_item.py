import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.drop(columns=["shipping_limit_date"], inplace=True)

    df.rename(columns={"order_item_id": "item_id"}, inplace=True)

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`order_items` (
                `order_id` VARCHAR(45) NOT NULL,
                `item_id` VARCHAR(45) NOT NULL,
                `product_id` VARCHAR(45) NOT NULL,
                `seller_id` VARCHAR(45) NOT NULL,
                `price` DECIMAL(10,2) NOT NULL,
                `freight_value` DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (`order_id`) REFERENCES `data_warehouse_olist`.`orders` (`id`),
                FOREIGN KEY (`product_id`) REFERENCES `data_warehouse_olist`.`products` (`id`),
                FOREIGN KEY (`seller_id`) REFERENCES `data_warehouse_olist`.`sellers` (`id`)
                );
                """
        )

    df.to_sql(
        name="order_items",
        con=engine,
        index=False,
        if_exists="append",
    )

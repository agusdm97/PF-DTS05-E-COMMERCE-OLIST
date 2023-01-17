import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.columns = df.columns.str.removeprefix("payment_")

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`order_payments` (
                `order_id` VARCHAR(45) NOT NULL,
                `sequential` INT NOT NULL,
                `type` VARCHAR(45) NOT NULL,
                `installments` INT NOT NULL,
                `value` DECIMAL (10,2) NOT NULL,
                FOREIGN KEY (`order_id`) REFERENCES `data_warehouse_olist`.`orders` (`id`)
                );
                """
        )

    df.to_sql(
        name="order_payments",
        con=engine,
        index=False,
        if_exists="append",
    )

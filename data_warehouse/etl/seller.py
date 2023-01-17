import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.drop(columns=["seller_city", "seller_state"], inplace=True)

    df.columns = df.columns.str.removeprefix("seller_").str.removesuffix("_prefix")

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`sellers` (
                `id` VARCHAR(45) NOT NULL,
                `zip_code` INT NOT NULL,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`zip_code`) REFERENCES `data_warehouse_olist`.`geolocations` (`zip_code`)
                );
                """
        )

    df.to_sql(
        name="sellers",
        con=engine,
        index=False,
        if_exists="append",
    )

import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.drop(columns=["product_name_lenght", "product_description_lenght"], inplace=True)

    df.columns = df.columns.str.removeprefix("product_")

    df["category_name"].fillna("other", inplace=True)
    df["photos_qty"].fillna(0, inplace=True)
    df["weight_g"].fillna(0, inplace=True)
    df["length_cm"].fillna(0, inplace=True)
    df["height_cm"].fillna(0, inplace=True)
    df["width_cm"].fillna(0, inplace=True)

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`products` (
                `id` VARCHAR(45) NOT NULL,
                `category_name` VARCHAR(50) NOT NULL,
                `photos_qty` INT NOT NULL,
                `weight_g` INT NOT NULL,
                `length_cm` INT NOT NULL,
                `height_cm` INT NOT NULL,
                `width_cm` INT NOT NULL,
                PRIMARY KEY (`id`)
                );
                """
        )

    df.to_sql(
        name="products",
        con=engine,
        index=False,
        if_exists="append",
    )

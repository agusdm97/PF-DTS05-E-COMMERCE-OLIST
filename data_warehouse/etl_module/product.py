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
        usecols=[
            "product_id",
            "product_category_name",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
    )

    # Renombrar columnas
    df.rename(
        columns={
            "product_id": "id",
            "product_category_name": "category_name",
            "product_photos_qty": "photos_qty",
            "product_weight_g": "weight_g",
            "product_length_cm": "length_cm",
            "product_height_cm": "height_cm",
            "product_width_cm": "width_cm",
        },
        inplace=True,
    )

    # Rellenar valores faltantes
    df["category_name"].fillna("other", inplace=True)
    df["photos_qty"].fillna(0, inplace=True)
    df["weight_g"].fillna(0, inplace=True)
    df["length_cm"].fillna(0, inplace=True)
    df["height_cm"].fillna(0, inplace=True)
    df["width_cm"].fillna(0, inplace=True)

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "products" si no existe
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

    # Cargar los datos en la tabla "products"
    df.to_sql(
        name="products",
        con=engine,
        index=False,
        if_exists="append",
    )

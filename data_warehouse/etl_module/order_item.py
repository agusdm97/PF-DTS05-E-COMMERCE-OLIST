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
    df = pd.read_csv(filepath_or_buffer=data_path)

    # Eliminar columna "shipping_limit_date"
    df.drop(columns=["shipping_limit_date"], inplace=True)

    # Renombrar columna "order_item_id" a "item_id"
    df.rename(columns={"order_item_id": "item_id"}, inplace=True)

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "order_items" si no existe
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

    # Cargar los datos en la tabla "order_items"
    df.to_sql(
        name="order_items",
        con=engine,
        index=False,
        if_exists="append",
    )

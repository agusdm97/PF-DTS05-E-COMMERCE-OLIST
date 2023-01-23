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
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
        ],
    )

    # Renombrar columnas
    df.rename(
        columns={
            "review_score": "score",
            "review_comment_title": "comment_title",
            "review_comment_message": "comment_message",
        },
        inplace=True,
    )

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "order_reviews" si no existe
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`order_reviews` (
                `review_id` VARCHAR(45) NOT NULL,
                `order_id` VARCHAR(45) NOT NULL,
                `score` INT NOT NULL,
                `comment_title` VARCHAR(55),
                `comment_message` VARCHAR(255),
                FOREIGN KEY (`order_id`) REFERENCES `data_warehouse_olist`.`orders` (`order_id`)
                );
                """
        )

    # Cargar los datos en la tabla "order_reviews"
    df.to_sql(
        name="order_reviews",
        con=engine,
        index=False,
        if_exists="append",
    )

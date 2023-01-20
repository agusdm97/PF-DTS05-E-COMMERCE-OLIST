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

    # Renombrar columnas
    df.rename(
        columns={
            "payment_sequential": "sequential",
            "payment_type": "type",
            "payment_installments": "installments",
            "payment_value": "value",
        },
        inplace=True,
    )

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "order_payments" si no existe
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

    # Cargar los datos en la tabla "order_payments"
    df.to_sql(
        name="order_payments",
        con=engine,
        index=False,
        if_exists="append",
    )

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
        usecols=["customer_id", "customer_unique_id", "customer_zip_code_prefix"],
    )

    # Renombrar las columnas
    df.rename(
        columns={
            "customer_id": "id",
            "customer_unique_id": "unique_id",
            "customer_zip_code_prefix": "zip_code",
        },
        inplace=True,
    )

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "customers" si no existe
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`customers` (
                `id` VARCHAR(45) NOT NULL,
                `unique_id` VARCHAR(45) NOT NULL,
                `zip_code` INT NOT NULL,
                PRIMARY KEY (`id`),
                FOREIGN KEY (`zip_code`) REFERENCES `data_warehouse_olist`.`geolocations` (`zip_code`)
                );
                """
        )
    # Cargar los datos en la tabla "customers"
    df.to_sql(
        name="customers",
        con=engine,
        index=False,
        if_exists="append",
    )

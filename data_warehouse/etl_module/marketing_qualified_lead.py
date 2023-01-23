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
        usecols=["mql_id", "first_contact_date", "origin"],
        parse_dates=["first_contact_date"],
    )

    # Rellenar valores faltantes en la columna origin
    df["origin"].fillna("other", inplace=True)

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "marketing_qualified_leads" si no existe
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`marketing_qualified_leads` (
                `mql_id` VARCHAR(45) NOT NULL,
                `first_contact_date` DATE NOT NULL,
                `origin` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`mql_id`)
                );
                """
        )

    # Cargar los datos en la tabla "marketing_qualified_leads"
    df.to_sql(
        name="marketing_qualified_leads",
        con=engine,
        index=False,
        if_exists="append",
    )

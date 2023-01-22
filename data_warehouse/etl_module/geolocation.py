import pandas as pd
import sqlalchemy as sql


def etl(
    data_path: str,
    zip_code_data_path: str,
    customer_data_path: str,
    seller_data_path: str,
    engine: sql.engine.Engine,
) -> None:
    """
    Esta función realiza una ETL en varios archivos CSV y carga los datos en una tabla de una base de datos.

    Args:
    - data_path (str): La ruta del archivo CSV de geolocations.
    - zip_code_data_path (str): La ruta del archivo CSV de códigos postales.
    - customer_data_path (str): La ruta del archivo CSV de clientes.
    - seller_data_path (str): La ruta del archivo CSV de vendedores.
    - engine (sqlalchemy.engine.Engine): El objeto Engine de SQLAlchemy para conectarse a la base de datos.

    Returns: None
    """

    # Leer archivo CSV de geolocations
    df_geolocations = pd.read_csv(
        filepath_or_buffer=data_path,
        usecols=[
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_state",
        ],
    )

    # Leer archivo CSV de códigos postales
    df_zip_codes = pd.read_csv(filepath_or_buffer=zip_code_data_path)

    # Extraer el prefijo de código postal
    df_zip_codes["zip_code"] = df_zip_codes["zip_code"].str.split("-", expand=True)[0]
    df_zip_codes["zip_code"] = pd.to_numeric(df_zip_codes["zip_code"])

    # Leer archivo CSV de clientes
    df_customers = pd.read_csv(
        filepath_or_buffer=customer_data_path,
        usecols=["customer_zip_code_prefix", "customer_state"],
    )

    # Filtra los clientes que no tienen zip_code en geolocations
    df_customers_missing = df_customers[
        ~df_customers["customer_zip_code_prefix"].isin(
            df_geolocations["geolocation_zip_code_prefix"]
        )
    ]
    del df_customers

    # Leer archivo CSV de vendedores
    df_sellers = pd.read_csv(
        filepath_or_buffer=seller_data_path,
        usecols=["seller_zip_code_prefix", "seller_state"],
    )

    # Filtra los vendedores que no tienen zip_code en geolocations
    df_sellers_missing = df_sellers[
        ~df_sellers["seller_zip_code_prefix"].isin(
            df_geolocations["geolocation_zip_code_prefix"]
        )
    ]
    del df_sellers

    # Unir dataframes
    df_geolocations = pd.concat(
        objs=[df_geolocations, df_customers_missing, df_sellers_missing]
    )

    # Asignar valores de clientes faltantes a geolocations
    filter_ = (
        df_geolocations["geolocation_zip_code_prefix"].isna()
        & df_geolocations["customer_zip_code_prefix"].notna()
    )
    df_geolocations.loc[filter_, "geolocation_zip_code_prefix"] = df_geolocations.loc[
        filter_, "customer_zip_code_prefix"
    ]
    df_geolocations.loc[filter_, "geolocation_state"] = df_geolocations.loc[
        filter_, "customer_state"
    ]

    # Asignar valores de vendedores faltantes a geolocations
    filter_ = (
        df_geolocations["geolocation_zip_code_prefix"].isna()
        & df_geolocations["seller_zip_code_prefix"].notna()
    )
    df_geolocations.loc[filter_, "geolocation_zip_code_prefix"] = df_geolocations.loc[
        filter_, "seller_zip_code_prefix"
    ]
    df_geolocations.loc[filter_, "geolocation_state"] = df_geolocations.loc[
        filter_, "seller_state"
    ]

    # Eliminar columnas innecesarias
    df_geolocations.drop(
        columns=[
            "customer_zip_code_prefix",
            "seller_zip_code_prefix",
            "customer_state",
            "seller_state",
        ],
        inplace=True,
    )

    # Cambia el tipo de float64 a int64
    df_geolocations["geolocation_zip_code_prefix"] = df_geolocations[
        "geolocation_zip_code_prefix"
    ].astype("int64")

    # Ordenar los dataframes
    df_zip_codes.sort_values(by="zip_code", inplace=True)
    df_geolocations.sort_values(by="geolocation_zip_code_prefix", inplace=True)

    # Unir dataframes
    df = pd.merge_asof(
        left=df_geolocations,
        right=df_zip_codes,
        left_on="geolocation_zip_code_prefix",
        right_on="zip_code",
        direction="backward",
    )

    del df_geolocations
    del df_zip_codes

    # Eliminar columnas innecesarias
    df.drop(
        columns=[
            "zip_code",
        ],
        inplace=True,
    )

    # Reemplazarla valores faltantes en las columnas de latitud y longitud
    filter_ = df["geolocation_lat"].isna() & df["geolocation_lng"].isna()

    df.loc[filter_, "geolocation_lat"] = df.loc[filter_, "latitude"]
    df.loc[filter_, "geolocation_lng"] = df.loc[filter_, "longitude"]

    # Calcula la variación porcentual de los valores originales con los de referencia
    df["latitude_%"] = (
        abs((df["geolocation_lat"] - df["latitude"]) / df["latitude"]) * 100
    )
    df["longitude_%"] = (
        abs((df["geolocation_lng"] - df["longitude"]) / df["longitude"]) * 100
    )

    # Reemplaza los valores que difieren mas de un 1% con los valores de referencia
    filter_ = df["latitude_%"] > 1
    df.loc[filter_, "geolocation_lat"] = df.loc[filter_, "latitude"]

    filter_ = df["longitude_%"] > 1
    df.loc[filter_, "geolocation_lng"] = df.loc[filter_, "longitude"]

    # Eliminar columnas innecesarias
    df.drop(
        columns=["latitude", "longitude", "latitude_%", "longitude_%"], inplace=True
    )

    # Agrupa por zip_code y saca el promedio de la latitud y la longitud
    df = (
        df.groupby("geolocation_zip_code_prefix")
        .aggregate(
            func={
                "geolocation_lat": "mean",
                "geolocation_lng": "mean",
                "geolocation_state": "first",
                "city_name": "first",
            }
        )
        .reset_index()
    )

    # Renombra las columnas
    df.rename(
        columns={
            "geolocation_lat": "latitude",
            "geolocation_lng": "longitude",
            "geolocation_state": "state",
            "city_name": "city",
            "geolocation_zip_code_prefix": "zip_code",
        },
        inplace=True,
    )

    # Conectarse a la base de datos
    with engine.connect() as conn:
        # Crear tabla "geolocations" si no existe
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`geolocations` (
                `zip_code` INT NOT NULL,
                `city` VARCHAR(45) NOT NULL,
                `state` VARCHAR(45) NOT NULL,
                `latitude` DECIMAL(7,5) NOT NULL,
                `longitude` DECIMAL(7,5) NOT NULL,
                PRIMARY KEY (`zip_code`)
                );
            """
        )

    # Cargar los datos en la tabla "geolocations"
    df.to_sql(
        name="geolocations",
        con=engine,
        index=False,
        if_exists="append",
    )

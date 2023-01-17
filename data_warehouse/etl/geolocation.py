import pandas as pd
import sqlalchemy as sql


def etl(
    data_path: str,
    zip_code_data_path: str,
    customer_data_path: str,
    seller_data_path: str,
    engine: sql.engine.Engine,
) -> None:

    df_geolocations = pd.read_csv(filepath_or_buffer=data_path)
    df_zip_codes = pd.read_csv(filepath_or_buffer=zip_code_data_path)

    df_zip_codes["zip_code_prefix"] = df_zip_codes["zip_code"].str.split(
        "-", expand=True
    )[0]
    df_zip_codes["zip_code_prefix"] = pd.to_numeric(df_zip_codes["zip_code_prefix"])
    df_zip_codes.sort_values(by="zip_code_prefix", inplace=True)

    df_zip_codes["zip_code_prefix_shift"] = df_zip_codes["zip_code_prefix"].shift(
        periods=-1, fill_value=999999
    )

    df_customers = pd.read_csv(filepath_or_buffer=customer_data_path)
    df_customers_missing = df_customers[
        ~df_customers["customer_zip_code_prefix"].isin(
            df_geolocations["geolocation_zip_code_prefix"]
        )
    ]
    del df_customers

    df_sellers = pd.read_csv(filepath_or_buffer=seller_data_path)
    df_sellers_missing = df_sellers[
        ~df_sellers["seller_zip_code_prefix"].isin(
            df_geolocations["geolocation_zip_code_prefix"]
        )
    ]
    del df_sellers

    df_geolocations = pd.concat(
        objs=[df_geolocations, df_customers_missing, df_sellers_missing]
    )

    df_geolocations.drop(
        columns=[
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "seller_id",
            "seller_city",
        ],
        inplace=True,
    )

    filter_1 = (
        df_geolocations["geolocation_zip_code_prefix"].isna()
        & df_geolocations["customer_zip_code_prefix"].notna()
    )
    df_geolocations.loc[filter_1, "geolocation_zip_code_prefix"] = df_geolocations.loc[
        filter_1, "customer_zip_code_prefix"
    ]
    df_geolocations.loc[filter_1, "geolocation_state"] = df_geolocations.loc[
        filter_1, "customer_state"
    ]

    filter_2 = (
        df_geolocations["geolocation_zip_code_prefix"].isna()
        & df_geolocations["seller_zip_code_prefix"].notna()
    )
    df_geolocations.loc[filter_2, "geolocation_zip_code_prefix"] = df_geolocations.loc[
        filter_2, "seller_zip_code_prefix"
    ]
    df_geolocations.loc[filter_2, "geolocation_state"] = df_geolocations.loc[
        filter_2, "seller_state"
    ]

    df_geolocations.drop(
        columns=[
            "customer_zip_code_prefix",
            "seller_zip_code_prefix",
            "customer_state",
            "seller_state",
        ],
        inplace=True,
    )

    for row in df_zip_codes.iterrows():
        filter_ = (
            df_geolocations["geolocation_zip_code_prefix"] >= row[1]["zip_code_prefix"]
        ) & (
            df_geolocations["geolocation_zip_code_prefix"]
            < row[1]["zip_code_prefix_shift"]
        )
        df_geolocations.loc[filter_, "geolocation_zip_code_prefix_range"] = row[1][
            "zip_code_prefix"
        ]

    df = pd.merge(
        left=df_geolocations,
        right=df_zip_codes,
        how="left",
        left_on="geolocation_zip_code_prefix_range",
        right_on="zip_code_prefix",
    )

    del df_geolocations
    del df_zip_codes

    df.drop(
        columns=[
            "zip_code",
            "zip_code_prefix",
            "zip_code_prefix_shift",
            "geolocation_zip_code_prefix_range",
            "geolocation_city",
        ],
        inplace=True,
    )

    filter_ = df["geolocation_lat"].isna() & df["geolocation_lng"].isna()

    df.loc[filter_, "geolocation_lat"] = df.loc[filter_, "latitude"]
    df.loc[filter_, "geolocation_lng"] = df.loc[filter_, "longitude"]

    df["latitude_%"] = (
        abs((df["geolocation_lat"] - df["latitude"]) / df["latitude"]) * 100
    )
    df["longitude_%"] = (
        abs((df["geolocation_lng"] - df["longitude"]) / df["longitude"]) * 100
    )
    filter_ = df["latitude_%"] > 1
    df.loc[filter_, "geolocation_lat"] = df.loc[filter_, "latitude"]

    filter_ = df["longitude_%"] > 1
    df.loc[filter_, "geolocation_lng"] = df.loc[filter_, "longitude"]

    df.drop(
        columns=["latitude", "longitude", "latitude_%", "longitude_%"], inplace=True
    )

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

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`geolocations` (
                `zip_code` INT NOT NULL,
                `city` VARCHAR(45) NOT NULL,
                `state` VARCHAR(45) NOT NULL,
                `latitude` DECIMAL(7,5) NOT NULL,
                `longitude` DECIMAL(7,5) NOT NULL,
                PRIMARY KEY (`zip_code`));
            """
        )

    df.to_sql(
        name="geolocations",
        con=engine,
        index=False,
        if_exists="append",
    )

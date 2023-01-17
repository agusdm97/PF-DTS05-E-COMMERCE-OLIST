import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.drop(
        columns=[
            "seller_id",
            "sdr_id",
            "sr_id",
            "lead_behaviour_profile",
            "has_company",
            "has_gtin",
            "average_stock",
            "declared_product_catalog_size",
            "declared_monthly_revenue",
        ],
        inplace=True,
    )

    df["won_date"] = pd.to_datetime(df["won_date"])

    df["business_segment"].fillna("other", inplace=True)
    df["lead_type"].fillna("other", inplace=True)
    df["business_type"].fillna("other", inplace=True)

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`closed_deals` (
                `mql_id` VARCHAR(45) NOT NULL,
                `won_date` DATE NOT NULL,
                `business_segment` VARCHAR(45) NOT NULL,
                `lead_type` VARCHAR(45) NOT NULL,
                `business_type` VARCHAR(45) NOT NULL,
                FOREIGN KEY (`mql_id`) REFERENCES `data_warehouse_olist`.`marketing_qualified_leads` (`id`)
                );
                """
        )

    df.to_sql(
        name="closed_deals",
        con=engine,
        index=False,
        if_exists="append",
    )

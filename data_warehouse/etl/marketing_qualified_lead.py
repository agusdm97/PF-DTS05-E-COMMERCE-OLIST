import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.drop(columns=["landing_page_id"], inplace=True)

    df["first_contact_date"] = pd.to_datetime(df["first_contact_date"])

    df.columns = df.columns.str.removeprefix("mql_")

    df["origin"].fillna("other", inplace=True)

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`marketing_qualified_leads` (
                `id` VARCHAR(45) NOT NULL,
                `first_contact_date` DATE NOT NULL,
                `origin` VARCHAR(45) NOT NULL,
                PRIMARY KEY (`id`)
                );
                """
        )

    df.to_sql(
        name="marketing_qualified_leads",
        con=engine,
        index=False,
        if_exists="append",
    )

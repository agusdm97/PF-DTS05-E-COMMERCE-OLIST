import pandas as pd
import sqlalchemy as sql


def etl(data_path: str, engine: sql.engine.Engine) -> None:

    df = pd.read_csv(filepath_or_buffer=data_path)

    df.drop(columns=["review_creation_date", "review_answer_timestamp"], inplace=True)

    df.columns = df.columns.str.removeprefix("review_")

    with engine.connect() as conn:
        conn.execute(
            """         
            CREATE TABLE IF NOT EXISTS `data_warehouse_olist`.`order_reviews` (
                `id` VARCHAR(45) NOT NULL,
                `order_id` VARCHAR(45) NOT NULL,
                `score` INT NOT NULL,
                `comment_title` VARCHAR(55),
                `comment_message` VARCHAR(255),
                FOREIGN KEY (`order_id`) REFERENCES `data_warehouse_olist`.`orders` (`id`)
                );
                """
        )

    df.to_sql(
        name="order_reviews",
        con=engine,
        index=False,
        if_exists="append",
    )

import sqlalchemy as sql
import warnings

from etl import (
    geolocation,
    customer,
    seller,
    product,
    marketing_qualified_lead,
    closed_deal,
    order,
    order_item,
    order_payment,
    order_review,
)


warnings.filterwarnings("ignore", category=sql.exc.RemovedIn20Warning)

engine = sql.create_engine(
    "mysql+pymysql://root:password@localhost:3307/data_warehouse_olist?charset=utf8mb4"
)

with engine.connect() as conn:
    conn.execute(
        """
        USE data_warehouse_olist;
    """
    )
geolocation.etl(
    data_path="data_warehouse/datasets/olist_geolocation_dataset.csv",
    zip_code_data_path="data_warehouse/datasets/br_zip_code.csv",
    customer_data_path="data_warehouse/datasets/olist_customers_dataset.csv",
    seller_data_path="data_warehouse/datasets/olist_sellers_dataset.csv",
    engine=engine,
)
customer.etl(data_path="data_warehouse/datasets/olist_customers_dataset.csv", engine=engine)
seller.etl(data_path="data_warehouse/datasets/olist_sellers_dataset.csv", engine=engine)
product.etl(data_path="data_warehouse/datasets/olist_products_dataset.csv", engine=engine)
marketing_qualified_lead.etl(
    data_path="data_warehouse/datasets/olist_marketing_qualified_leads_dataset.csv", engine=engine
)
closed_deal.etl(data_path="data_warehouse/datasets/olist_closed_deals_dataset.csv", engine=engine)
order.etl(data_path="data_warehouse/datasets/olist_orders_dataset.csv", engine=engine)
order_item.etl(data_path="data_warehouse/datasets/olist_order_items_dataset.csv", engine=engine)
order_payment.etl(data_path="data_warehouse/datasets/olist_order_payments_dataset.csv", engine=engine)
order_review.etl(data_path="data_warehouse/datasets/olist_order_reviews_dataset.csv", engine=engine)

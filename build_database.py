import pandas as pd
from sqlalchemy import create_engine

# ---- SETTINGS: change YOUR_PASSWORD to your real MySQL password ----
password = "bhargu07"
csv_path = r"C:\Users\Bhargavi\Data analytics projects\Flagship Project\Sample - Superstore.csv"

df = pd.read_csv(csv_path, encoding="latin1")
print("Rows read from CSV:", len(df))

df.columns = [
    "row_id", "order_id", "order_date", "ship_date", "ship_mode",
    "customer_id", "customer_name", "segment", "country", "city",
    "state", "postal_code", "region", "product_id", "category",
    "sub_category", "product_name", "sales", "quantity", "discount", "profit"
]

df["product_id"] = df["product_id"].str.strip()
df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")

customers = df[["customer_id", "customer_name", "segment"]].drop_duplicates(subset="customer_id")
products = df[["product_id", "product_name", "category", "sub_category"]].drop_duplicates(subset="product_id")
orders = df[["row_id", "order_id", "order_date", "ship_date", "ship_mode",
             "customer_id", "product_id", "country", "city", "state",
             "postal_code", "region", "sales", "quantity", "discount", "profit"]]

print("Customers:", len(customers), "| Products:", len(products), "| Orders:", len(orders))

engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/superstore_analytics")

customers.to_sql("customers", con=engine, if_exists="replace", index=False)
products.to_sql("products", con=engine, if_exists="replace", index=False)
orders.to_sql("orders", con=engine, if_exists="replace", index=False)

print("Done! Database built successfully.")
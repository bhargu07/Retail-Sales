import pandas as pd
from sqlalchemy import create_engine

password = "bhargu07"
engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/superstore_analytics")

df = pd.read_sql("SELECT * FROM sales_master", con=engine)
print("Rows fetched:", len(df))

output_path = r"C:\Users\Bhargavi\Data analytics projects\Flagship Project\sales_master_export.csv"
df.to_csv(output_path, index=False)
print("Saved to:", output_path)
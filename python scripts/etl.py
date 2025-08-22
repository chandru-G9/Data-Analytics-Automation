from sqlalchemy import create_engine
import urllib
import pandas as pd
import json
import logging
import os

# Load config
config_path=r"C:\Users\chand\OneDrive\Desktop\Data analytics\Configuration\config.json"
with open(config_path) as f:
    config = json.load(f)
    db_config = config["db"]
    csv_file = config["paths"]["csv_file"]
    logs_folder = config["paths"]["log_folder"]

#logging setup
log_path = os.path.join(logs_folder, "etl.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# CSV read & cleaning
df = pd.read_csv(csv_file)

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# Convert datatypes
df["order_number"] = df["order_number"].astype(str).str.strip()
df["product_key"] = df["product_key"].astype(int)
df["customer_key"] = df["customer_key"].astype(int)
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["shipping_date"] = pd.to_datetime(df["shipping_date"], errors="coerce")
df["due_date"] = pd.to_datetime(df["due_date"], errors="coerce")
df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce").astype(int)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype(int)
df["price"] = pd.to_numeric(df["price"], errors="coerce").astype(int)
df.dropna(inplace=True)

# Connect to SQL Server
params = urllib.parse.quote_plus(
    f"DRIVER={{{db_config['driver']}}};"
    f"SERVER={db_config['server']};"
    f"DATABASE={db_config['database']};"
    f"Trusted_Connection={db_config['trusted_connection']};"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

# Filter new rows
existing_ids = pd.read_sql("SELECT order_number FROM dbo.fact_sales", engine)
existing_ids = existing_ids['order_number'].str.strip()
new_rows = df[~df['order_number'].isin(existing_ids)]

if(new_rows.empty):
    print("No new rows to insert.")
    logging.info("No new rows to insert.")
else:
    print(f"New rows to insert: {len(new_rows)}")
    logging.info(f"New rows to insert: {len(new_rows)}")
# Insert in chunks WITHOUT method='multi'
    new_rows.to_sql(
    name="fact_sales",
    schema="dbo",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=500   # small enough to stay below SQL Server parameter limit
    )

    logging.info("Sales data loaded successfully!")

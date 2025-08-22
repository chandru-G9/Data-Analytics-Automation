import os
import pandas as pd
from sqlalchemy import create_engine
import urllib
import logging
import json

# ----------------- Load config -----------------
config_path = r"C:\Users\chand\OneDrive\Desktop\Data analytics\Configuration\config.json"
with open(config_path) as f:
    config = json.load(f)
    db_config = config["db"]
    logs_folder = config["paths"]["log_folder"]
    reports_folder = config["paths"]["report_folder"]
    sql_folder = config["paths"]["sql_folder"]

# ----------------- Setup folders -----------------
#logs_folder = r"C:\Users\chand\OneDrive\Desktop\Data analytics\logs"
#reports_folder = r"C:\Users\chand\OneDrive\Desktop\Data analytics\Reports"

os.makedirs(logs_folder, exist_ok=True)
os.makedirs(reports_folder, exist_ok=True)

# ----------------- Setup logging -----------------
log_path = os.path.join(logs_folder, "report_generation.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------- Connect to SQL Server -----------------
params = urllib.parse.quote_plus(
    f"DRIVER={{{db_config['driver']}}};"
    f"SERVER={db_config['server']};"
    f"DATABASE={db_config['database']};"
    f"Trusted_Connection={db_config['trusted_connection']};"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# ----------------- Function to load queries from file -----------------
def load_queries_from_file(file_path):
    queries = {}
    with open(file_path, "r") as f:
        content = f.read()
    # Split queries by comments starting with --
    blocks = [q.strip() for q in content.split("--") if q.strip()]
    for block in blocks:
        lines = block.splitlines()
        kpi_name = lines[0].strip().replace(" ", "_")  # first line after -- as name
        sql_query = "\n".join(lines[1:]).strip()       # rest is the query
        queries[kpi_name] = sql_query
    return queries

# ----------------- Execute all SQL files -----------------

for sql_file in os.listdir(sql_folder):
    if sql_file.endswith(".sql"):
        file_path = os.path.join(sql_folder, sql_file)
        category_name = os.path.splitext(sql_file)[0]  # use filename as category
        category_folder = os.path.join(reports_folder, category_name)  # <-- FIXED
        os.makedirs(category_folder, exist_ok=True)

        queries = load_queries_from_file(file_path)
        for kpi_name, query in queries.items():
            try:
                df = pd.read_sql(query, engine)
                file_path_excel = os.path.join(category_folder, f"{kpi_name}.xlsx")
                df.to_excel(file_path_excel, index=False)
                print(f"{kpi_name} saved in {category_folder}")
                logging.info(f"{kpi_name} saved successfully in {category_folder}")
            except Exception as e:
                print(f"[ERROR] {kpi_name} failed: {e}")
                logging.error(f"Failed to save {kpi_name} in {category_folder}: {str(e)}")

logging.info("All KPI reports generated successfully!")

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clean_transactions.parquet"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_USER = "postgres"
DB_PASSWORD = "YOUR_NEW_PASSWORD"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "dubai_retail_intelligence"


# ============================================================
# DATABASE CONNECTION
# ============================================================

connection_string = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}"
)

engine = create_engine(connection_string)


# ============================================================
# LOAD DATA
# ============================================================

def main():

    print("Loading cleaned Parquet dataset...")

    df = pd.read_parquet(DATA_FILE)

    print(f"Rows loaded from Parquet: {len(df):,}")

    # Rename columns to match PostgreSQL table
    df = df.rename(
        columns={
            "id": "transaction_id",
            "workstationgroupid": "workstation_group_id",
            "operatorid": "operator_id",
            "date": "transaction_date",
        }
    )

    # Load into PostgreSQL
    print("\nLoading data into PostgreSQL...")

    df.to_sql(
        "fact_transactions",
        engine,
        schema="analytics",
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi",
    )

    print("\nData successfully loaded!")

    print(f"Rows inserted: {len(df):,}")


if __name__ == "__main__":
    main()
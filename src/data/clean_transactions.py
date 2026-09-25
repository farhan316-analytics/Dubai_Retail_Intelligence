from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "pos_transactions.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "clean_transactions.parquet"


def load_data():
    """Load the raw POS transaction dataset."""
    df = pd.read_csv(RAW_FILE)

    print(f"Loaded {len(df):,} transactions")

    return df


def clean_data(df):
    """Clean and standardize POS transaction data."""

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Convert timestamps
    df["begin_date_time"] = pd.to_datetime(
        df["begin_date_time"],
        errors="coerce"
    )

    df["end_date_time"] = pd.to_datetime(
        df["end_date_time"],
        errors="coerce"
    )

    # Remove exact duplicate transactions
    df = df.drop_duplicates()

    # Remove invalid records
    df = df[
        (df["amount"] >= 0) &
        (df["basket_size"] >= 0)
    ].copy()

    # Create transaction duration in seconds
    df["transaction_duration_seconds"] = (
        df["end_date_time"] - df["begin_date_time"]
    ).dt.total_seconds()

    # Create useful time attributes
    df["date"] = df["begin_date_time"].dt.date
    df["year"] = df["begin_date_time"].dt.year
    df["month"] = df["begin_date_time"].dt.month
    df["year_month"] = df["begin_date_time"].dt.to_period("M").astype(str)
    df["day_of_week"] = df["begin_date_time"].dt.day_name()
    df["hour"] = df["begin_date_time"].dt.hour

    # Payment method
    df["payment_method"] = "Unknown"

    df.loc[
        (df["t_cash"] == True) & (df["t_card"] == False),
        "payment_method"
    ] = "Cash"

    df.loc[
        (df["t_cash"] == False) & (df["t_card"] == True),
        "payment_method"
    ] = "Card"

    return df


def save_data(df):
    """Save cleaned data as Parquet."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print(f"Saved cleaned dataset to: {OUTPUT_FILE}")


def main():
    df = load_data()

    print("\nCleaning data...")
    df = clean_data(df)

    print(f"Final rows: {len(df):,}")
    print(f"Final columns: {len(df.columns)}")

    print("\nMissing values:")
    print(df.isna().sum())

    save_data(df)


if __name__ == "__main__":
    main()
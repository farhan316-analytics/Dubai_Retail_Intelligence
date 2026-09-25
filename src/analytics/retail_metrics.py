from pathlib import Path
import pandas as pd


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
# LOAD DATA
# ============================================================

def load_data():
    """Load the cleaned transaction dataset."""
    df = pd.read_parquet(DATA_FILE)
    return df


# ============================================================
# CORE SALES KPIs
# ============================================================

def calculate_sales_kpis(df):
    """Calculate core retail sales KPIs."""

    kpis = {
        "total_revenue": df["amount"].sum(),
        "transaction_count": len(df),
        "average_transaction_value": df["amount"].mean(),
        "median_transaction_value": df["amount"].median(),
        "average_basket_size": df["basket_size"].mean(),
    }

    return kpis


# ============================================================
# PAYMENT ANALYTICS
# ============================================================

def calculate_payment_metrics(df):
    """Calculate payment-method transaction metrics."""

    payment_metrics = (
        df.groupby("payment_method")
        .agg(
            transactions=("id", "count"),
            revenue=("amount", "sum"),
            average_transaction=("amount", "mean"),
        )
        .reset_index()
    )

    payment_metrics["transaction_share_pct"] = (
        payment_metrics["transactions"]
        / len(df)
        * 100
    )

    payment_metrics["revenue_share_pct"] = (
        payment_metrics["revenue"]
        / df["amount"].sum()
        * 100
    )

    return payment_metrics


# ============================================================
# WORKSTATION PERFORMANCE
# ============================================================

def calculate_workstation_performance(df):
    """Calculate performance by workstation group."""

    workstation = (
        df.groupby("workstationgroupid")
        .agg(
            transactions=("id", "count"),
            revenue=("amount", "sum"),
            average_transaction=("amount", "mean"),
            average_basket_size=("basket_size", "mean"),
        )
        .reset_index()
    )

    workstation["revenue_share_pct"] = (
        workstation["revenue"]
        / df["amount"].sum()
        * 100
    )

    return workstation.sort_values(
        "revenue",
        ascending=False
    )


# ============================================================
# OPERATOR PERFORMANCE
# ============================================================

def calculate_operator_performance(df):
    """Calculate performance by operator."""

    operator = (
        df.groupby("operatorid")
        .agg(
            transactions=("id", "count"),
            revenue=("amount", "sum"),
            average_transaction=("amount", "mean"),
            average_basket_size=("basket_size", "mean"),
        )
        .reset_index()
    )

    return operator.sort_values(
        "revenue",
        ascending=False
    )


# ============================================================
# DAILY PERFORMANCE
# ============================================================

def calculate_daily_performance(df):
    """Calculate daily retail performance."""

    daily = (
        df.groupby("date")
        .agg(
            transactions=("id", "count"),
            revenue=("amount", "sum"),
            average_transaction=("amount", "mean"),
        )
        .reset_index()
    )

    return daily.sort_values("date")


# ============================================================
# MONTHLY PERFORMANCE
# ============================================================

def calculate_monthly_performance(df):
    """Calculate monthly retail performance."""

    monthly = (
        df.groupby("year_month")
        .agg(
            transactions=("id", "count"),
            revenue=("amount", "sum"),
            average_transaction=("amount", "mean"),
        )
        .reset_index()
    )

    return monthly.sort_values("year_month")


# ============================================================
# HOURLY PERFORMANCE
# ============================================================

def calculate_hourly_performance(df):
    """Calculate performance by hour of day."""

    hourly = (
        df.groupby("hour")
        .agg(
            transactions=("id", "count"),
            revenue=("amount", "sum"),
            average_transaction=("amount", "mean"),
        )
        .reset_index()
    )

    return hourly.sort_values("hour")


# ============================================================
# DAY OF WEEK PERFORMANCE
# ============================================================

def calculate_day_of_week_performance(df):
    """Calculate performance by day of week."""

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    daily = (
        df.groupby("day_of_week")
        .agg(
            transactions=("id", "count"),
            revenue=("amount", "sum"),
            average_transaction=("amount", "mean"),
        )
        .reset_index()
    )

    daily["day_of_week"] = pd.Categorical(
        daily["day_of_week"],
        categories=day_order,
        ordered=True,
    )

    return daily.sort_values("day_of_week")


# ============================================================
# TRANSACTION DURATION
# ============================================================

def calculate_transaction_duration(df):
    """Calculate transaction-duration statistics."""

    duration = df["transaction_duration_seconds"]

    return {
        "average_duration_seconds": duration.mean(),
        "median_duration_seconds": duration.median(),
        "minimum_duration_seconds": duration.min(),
        "maximum_duration_seconds": duration.max(),
    }


# ============================================================
# DATA QUALITY VALIDATION
# ============================================================

def validate_time_fields(df):
    """Validate timestamp and derived time fields."""

    validation = {
        "missing_begin_datetime": df["begin_date_time"].isna().sum(),
        "missing_end_datetime": df["end_date_time"].isna().sum(),
        "negative_duration": (
            df["transaction_duration_seconds"] < 0
        ).sum(),
        "zero_duration": (
            df["transaction_duration_seconds"] == 0
        ).sum(),
    }

    return validation


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading cleaned transaction data...")

    df = load_data()

    print(f"Transactions loaded: {len(df):,}")


    # --------------------------------------------------------
    # SALES KPIs
    # --------------------------------------------------------

    kpis = calculate_sales_kpis(df)

    print("\n========== SALES KPIs ==========")

    for metric, value in kpis.items():
        print(f"{metric}: {value:,.2f}")


    # --------------------------------------------------------
    # PAYMENT ANALYTICS
    # --------------------------------------------------------

    payment = calculate_payment_metrics(df)

    print("\n========== PAYMENT ANALYTICS ==========")
    print(payment.to_string(index=False))


    # --------------------------------------------------------
    # WORKSTATION PERFORMANCE
    # --------------------------------------------------------

    workstation = calculate_workstation_performance(df)

    print("\n========== WORKSTATION PERFORMANCE ==========")
    print(workstation.to_string(index=False))


    # --------------------------------------------------------
    # OPERATOR PERFORMANCE
    # --------------------------------------------------------

    operator = calculate_operator_performance(df)

    print("\n========== TOP 10 OPERATORS ==========")
    print(operator.head(10).to_string(index=False))


    # --------------------------------------------------------
    # DAILY PERFORMANCE
    # --------------------------------------------------------

    daily = calculate_daily_performance(df)

    print("\n========== DAILY PERFORMANCE ==========")
    print(daily.head(10).to_string(index=False))


    # --------------------------------------------------------
    # MONTHLY PERFORMANCE
    # --------------------------------------------------------

    monthly = calculate_monthly_performance(df)

    print("\n========== MONTHLY PERFORMANCE ==========")
    print(monthly.to_string(index=False))


    # --------------------------------------------------------
    # HOURLY PERFORMANCE
    # --------------------------------------------------------

    hourly = calculate_hourly_performance(df)

    print("\n========== HOURLY PERFORMANCE ==========")
    print(hourly.to_string(index=False))


    # --------------------------------------------------------
    # DAY OF WEEK PERFORMANCE
    # --------------------------------------------------------

    day_of_week = calculate_day_of_week_performance(df)

    print("\n========== DAY OF WEEK PERFORMANCE ==========")
    print(day_of_week.to_string(index=False))


    # --------------------------------------------------------
    # TRANSACTION DURATION
    # --------------------------------------------------------

    duration = calculate_transaction_duration(df)

    print("\n========== TRANSACTION DURATION ==========")

    for metric, value in duration.items():
        print(f"{metric}: {value:,.2f}")


    # --------------------------------------------------------
    # DATA QUALITY VALIDATION
    # --------------------------------------------------------

    validation = validate_time_fields(df)

    print("\n========== TIME FIELD VALIDATION ==========")

    for metric, value in validation.items():
        print(f"{metric}: {value:,}")


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    main()
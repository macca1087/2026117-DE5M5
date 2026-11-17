import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# SQL Server connection for the local development VM.
SQL_SERVER = "localhost"
SQL_DATABASE = "LibraryDB"
SQL_DRIVER = "ODBC Driver 17 for SQL Server"

odbc_string = (
    f"DRIVER={{{SQL_DRIVER}}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": odbc_string},
)
engine = create_engine(connection_url)


def format_columns(df):
    """Standardise column names to lowercase snake_case."""
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)
    )
    print("Converted column names to snake_case")
    return df


def drop_missing_rows(df):
    """Drop rows that contain one or more missing values."""
    cleaned_df = df.dropna()
    print(f"Dropped {len(df) - len(cleaned_df)} rows with missing values")
    return cleaned_df


def remove_quotes(df, column_name):
    """Remove quote characters and surrounding whitespace from a column."""
    df[column_name] = (
        df[column_name]
        .astype("string")
        .str.replace('"', "", regex=False)
        .str.strip()
    )
    print(f"Removed quotes from {column_name}")
    return df


def parse_date_column(df, column_name):
    """Parse dates in day/month/year format; invalid values become NaT."""
    df[column_name] = pd.to_datetime(
        df[column_name],
        format="%d/%m/%Y",
        errors="coerce",
    )
    print(f"Parsed dates in {column_name}")
    return df


def convert_to_nullable_int(df, column_name):
    """Convert a column to pandas' nullable integer type."""
    df[column_name] = df[column_name].astype("Int64")
    print(f"Converted {column_name} to nullable integers")
    return df


def calculate_days_borrowed(df, returned_column, checkout_column):
    """Calculate the number of days between checkout and return."""
    print("Calculated days borrowed")
    return (df[returned_column] - df[checkout_column]).dt.days


def write_to_sql(df, table_name):
    """Append a DataFrame to a table in the configured SQL Server database."""
    with engine.begin() as connection:
        df.to_sql(
            name=table_name,
            con=connection,
            schema="dbo",
            if_exists="append",
            index=False,
        )
    print(f"Wrote {len(df)} rows to dbo.{table_name}")


def save_outputs(df, csv_path, table_name):
    """Save cleaned data to CSV and SQL Server."""
    df.to_csv(csv_path, index=False)
    print(f"Wrote cleaned data to {csv_path}")
    write_to_sql(df, table_name)


def clean_books():
    """Load, clean, and save the book-loan data."""
    df = pd.read_csv("data/03_Library Systembook.csv")
    print("Read book-loan data")

    df = format_columns(df)
    df = drop_missing_rows(df)
    df = remove_quotes(df, "book_checkout")

    for column in ("book_checkout", "book_returned"):
        df = parse_date_column(df, column)

    for column in ("id", "customer_id"):
        df = convert_to_nullable_int(df, column)

    df["days_borrowed"] = calculate_days_borrowed(
        df,
        returned_column="book_returned",
        checkout_column="book_checkout",
    )
    df = convert_to_nullable_int(df, "days_borrowed")

    save_outputs(
        df,
        "data/03_Library Systembook_cleaned.csv",
        "systembook",
    )


def clean_customers():
    """Load, clean, and save the customer data."""
    df = pd.read_csv("data/03_Library SystemCustomers.csv")
    print("Read customer data")

    df = format_columns(df)
    df = drop_missing_rows(df)
    df = convert_to_nullable_int(df, "customer_id")

    save_outputs(
        df,
        "data/03_Library SystemCustomers_cleaned.csv",
        "customers",
    )


def clean_pipeline():
    """Run all data-cleaning steps."""
    clean_books()
    clean_customers()


if __name__ == "__main__":
    clean_pipeline()

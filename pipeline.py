import pandas as pd
from sqlalchemy import create_engine, inspect, text
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
        df.columns.str.strip().str.lower().str.replace(r"\\s+", "_", regex=True)
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
    """Insert only records whose key is not already in the SQL table."""
    table_keys = {"systembook": "id", "customers": "customer_id"}
    if table_name not in table_keys:
        raise ValueError(f"Unexpected SQL table: {table_name}")

    key_column = table_keys[table_name]
    if df[key_column].isna().any():
        raise ValueError(f"{key_column} cannot be missing when writing {table_name}")
    if df[key_column].duplicated().any():
        raise ValueError(f"Duplicate {key_column} values found in {table_name} input")

    with engine.begin() as connection:
        table_exists = inspect(connection).has_table(table_name, schema="dbo")
        if table_exists:
            query = text(f"SELECT [{key_column}] FROM [dbo].[{table_name}]")
            existing_keys = {row[0] for row in connection.execute(query)}
            rows_to_insert = df.loc[~df[key_column].isin(existing_keys)]
        else:
            existing_keys = set()
            rows_to_insert = df

        if not table_exists or not rows_to_insert.empty:
            rows_to_insert.to_sql(
                name=table_name,
                con=connection,
                schema="dbo",
                if_exists="append",
                index=False,
            )

    skipped_count = len(df) - len(rows_to_insert)
    print(
        f"Inserted {len(rows_to_insert)} new rows into dbo.{table_name}; "
        f"skipped {skipped_count} existing keys"
    )


def save_outputs(df, csv_path, table_name):
    """Save cleaned data to CSV and insert new records into SQL Server."""
    df.to_csv(csv_path, index=False)
    print(f"Wrote cleaned data to {csv_path}")
    write_to_sql(df, table_name)


def clean_books():
    """Load, clean, and save the book-loan data."""
    df = pd.read_csv("data/03_Library Systembook.csv")
    print("Read book-loan data")

    df = format_columns(df)
    df = drop_missing_rows(df)

    date_columns = ("book_checkout", "book_returned")
    for column in date_columns:
        df = remove_quotes(df, column)
        df = parse_date_column(df, column)

    df["date_issue"] = df[list(date_columns)].isna().any(axis=1)
    print(f"Flagged {int(df['date_issue'].sum())} rows with invalid dates")

    for column in ("id", "customer_id"):
        df = convert_to_nullable_int(df, column)

    df["days_borrowed"] = calculate_days_borrowed(
        df,
        returned_column="book_returned",
        checkout_column="book_checkout",
    )
    df = convert_to_nullable_int(df, "days_borrowed")
    df["valid_loan_flag"] = df["days_borrowed"].ge(0).astype("boolean")
    print(f"Flagged {int(df['valid_loan_flag'].eq(False).sum())} negative durations")

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

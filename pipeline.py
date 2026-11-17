import pandas as pd


# functions

# cols to underscore
def format_cols(df):
    df.columns = (
            df.columns
                .str.strip()
                        .str.lower()
                            .str.replace(r"\s+", "_", regex=True)
                            )
    print(f"converted col_names to underscore")
    return df

# drop na
def dropna(df):
    df = df.dropna()
    print(f"dropped null records")
    return df
    

# remove quotes from book checkout
def remove_quotes(df):
    df["book_checkout"] = (
            df["book_checkout"]
                .astype("string")
                        .str.replace('"', "", regex=False)
                            .str.strip()
                            )
    print(f"removed quotes")
    return df
# format date

def format_date(df,col):
    df[col] = pd.to_datetime(
        df[col],
            format="%d/%m/%Y",
                errors="coerce"
                )
    print(f"formatted dates for col {col}")
    return df

# format ids
def format_ints(df,col):
    df[col] = df[col].astype("Int64")
    print(f"formatted ints for col {col}")
    return df

 # calculate date
def calculate_date(df,returned,checkout):
    print(f"calculated days")
    return (df[returned] - df[checkout]).dt.days  
     

def clean_df ():
    # read in csv
    df_raw = pd.read_csv('data/03_Library Systembook.csv')
    print(f"Read in csv")
    #  create a working copy
    df = df_raw

    # cols to underscore
    df = format_cols(df)
    # drop na
    df = dropna(df)
    # remove quotes from book checkout
    df = remove_quotes(df)

    # correct date cols
    date_cols = ['book_checkout',  'book_returned']

    for c in date_cols:
        format_date(df,c)

    # correct id  cols
    id_cols = ['id', 'customer_id']

    for c in  id_cols:
        format_ints(df,c)

    # calculate date
    df['days_borrowed'] = calculate_date(df,'book_returned',  'book_checkout')
    format_ints(df,'days_borrowed')

    # write to csv
    df.to_csv('data/03_Library Systembook_cleaned.csv')
    print(f"written clean data to csv")


# DF 2 transformation-----------------------

# read in csv
def clean_df2():
    df2_raw = pd.read_csv('data/03_Library SystemCustomers.csv')
    print(f"read in csv 2")
    # create a working copy
    df2 = df2_raw
    # format cols
    df2 = format_cols(df2)
    # drop na
    df2 = dropna(df2)
    # format ints
    df2 = format_ints(df2,'customer_id')
    df2['customer_id'] = df2['customer_id'].astype("Int64")
    # write to csv
    df2.to_csv('data/03_Library SystemCustomers_cleaned.csv')
    print(f"written clean data to csv2")

def clean_pipeline():
    clean_df()
    clean_df2()

if __name__ == "__main__":
    # Main capability triggered IF this is run as an executable.
    clean_pipeline()
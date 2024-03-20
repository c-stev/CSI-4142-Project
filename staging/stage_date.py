import pandas as pd


def get_df():
    df = pd.read_csv('../data/date_data.csv')
    return df


def get_staged_df():
    df = pd.read_csv('../data/date_data.csv')
    # Converting the Date column to a datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    # Removing any potential leading and trailing spaces
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    return df

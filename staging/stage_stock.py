import pandas as pd


def get_df():
    df = pd.read_csv('../data/financial_data.csv')
    return df


def get_staged_df():
    df = pd.read_csv('../data/financial_data.csv')
    # Removing useless columns
    df = df.drop(columns=['Dividends', 'Stock Splits'])
    # Impossible for volume to be fractional, so adjusting data type to int64
    df['Volume'] = df['Volume'].astype('int64')
    # Removing any potential leading and trailing spaces
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    return df

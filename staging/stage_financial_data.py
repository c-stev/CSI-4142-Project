import pandas as pd
import extract.financial_data_extract as src


def get_df():
    df = pd.read_csv('../data/financial_data.csv')
    return df


def get_staged_df():
    src.extract_financial_data()
    df = pd.read_csv('../data/financial_data.csv')
    # Removing useless columns
    df = df.drop(columns=['Dividends', 'Stock Splits'])
    # Impossible for volume to be fractional, so adjusting data type to int64
    df['Volume'] = df['Volume'].astype('int64')
    # Removing any potential leading and trailing spaces
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    # Generate IDs
    df['Financial_Data_ID'] = range(1, len(df) + 1)
    df.set_index('Financial_Data_ID', inplace=True)
    return df

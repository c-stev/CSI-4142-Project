import pandas as pd
import extract.financial_data_extract as src
from os.path import dirname, abspath
import staging.stage_company as companies


def get_df():
    source_dir = dirname(dirname(abspath(__file__)))
    df = pd.read_csv(source_dir + '/data/financial_data.csv')
    return df


def get_staged_df():
    source_dir = dirname(dirname(abspath(__file__)))
    src.extract_financial_data()
    df = pd.read_csv(source_dir + '/data/financial_data.csv')
    # Removing rows whose companies yfinance cannot find
    df = df[~df['Ticker'].isin(companies.get_null_tickers())]
    # Making Date into datetime format
    df['Date'] = pd.to_datetime(df['Date'])
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
    # Setting all columns to lowercase (for PostgreSQL)
    df.columns = df.columns.str.lower()
    # Removing rows whose date exceeds 2022-01-01
    df = df[df['date'] <= '2022-01-01']
    return df

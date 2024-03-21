import pandas as pd
import extract.company_extract as src
from os.path import dirname, abspath


def get_df():
    source_dir = dirname(dirname(abspath(__file__)))
    df = pd.read_csv(source_dir + '/data/company_data.csv')
    return df


def get_staged_df():
    source_dir = dirname(dirname(abspath(__file__)))
    src.extract_companies()
    df = pd.read_csv(source_dir + '/data/company_data.csv')
    # Renaming columns
    df = df.rename(columns={'ticker': 'Ticker', 'name': 'Company', 'sector': 'Sector', 'country': 'Country'})
    # Removing rows whose country is '?' (since yfinance cannot find it)
    for index, row in df.iterrows():
        if row['Country'] == '?':
            df.drop(index, inplace=True)
    # Removing any potential leading and trailing spaces
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    # Generate IDs
    df['Company_ID'] = range(1, len(df) + 1)
    df.set_index('Company_ID', inplace=True)
    return df

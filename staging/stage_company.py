import pandas as pd


def get_df():
    df = pd.read_csv('../data/company_data.csv')
    return df


def get_staged_df():
    df = pd.read_csv('../data/company_data.csv')
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
    df['Financial_Data_ID'] = range(1, len(df) + 1)
    df.set_index('Financial_Data_ID', inplace=True)
    return df

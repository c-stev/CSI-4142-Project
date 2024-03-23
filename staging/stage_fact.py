import pandas as pd
import staging.stage_company as companies
import staging.stage_country as countries
import staging.stage_date as dates
import staging.stage_financial_data as financial_data
import numpy as np


def extract_rows_with_null(df):
    # Find rows with any null values
    null_rows = df[df.isnull().any(axis=1)]
    return null_rows


def get_staged_df():
    df_companies = companies.get_staged_df()
    df_countries = countries.get_staged_df()
    df_dates = dates.get_staged_df()
    df_financial_data = financial_data.get_staged_df()
    # Merging all dimensional dataframes
    df = pd.merge(df_financial_data, df_dates[['date', 'date_id']], on='date', how='left')
    df = pd.merge(df, df_companies[['ticker', 'company_id', 'country']], on='ticker', how='left')
    df = pd.merge(df, df_countries[['country', 'date', 'country_id']], on=['country', 'date'], how='left')
    # Setting all IDS to ints
    df['company_id'] = df['company_id'].astype(int)
    df['country_id'] = df['country_id'].astype(int)
    # Calculating measures (volatility = Parkinson's Volatility Formula)
    df['returns'] = df['open'] - df['close']
    volatility = []
    for i in range(len(df)):
        high = df.iloc[i]['high']
        low = df.iloc[i]['low']
        vol = np.sqrt((1/(4*np.log(2)))*((np.log(high/low))**2))
        volatility.append(vol)
    df['volatility'] = volatility
    # Removing useless columns
    df.drop(['ticker', 'date', 'open', 'close', 'high', 'low', 'volume', 'country'], axis=1, inplace=True)
    return df

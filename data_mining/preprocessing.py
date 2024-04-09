import staging.stage_country as country
import staging.stage_company as company
import staging.stage_financial_data as financial
import staging.stage_date as date
import staging.stage_fact as fact
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler


# Checks if a dataframe contains any missing values
def has_missing_values(df):
    return df.isnull().sum().sum() > 0


# Since ticker has too many unique values, OHE can't process it correctly; dataframe generated to translate
def generate_ticker_table():
    df_company = company.get_staged_df()
    ticker_to_int, ticker_count = {}, 1
    for ticker in df_company['ticker'].unique():
        ticker_to_int[ticker] = ticker_count
        ticker_count += 1
    # Converting the dictionary to a dataframe
    ticker_df = pd.DataFrame(list(ticker_to_int.items()), columns=['ticker', 'ticker_id'])
    return ticker_df


# Since sector has too many unique values, OHE can't process it correctly; dataframe generated to translate
def generate_sector_table():
    df_company = company.get_staged_df()
    sector_to_int, sector_count = {}, 1
    for sector in df_company['sector'].unique():
        sector_to_int[sector] = sector_count
        sector_count += 1
    # Converting the dictionary to a dataframe
    sector_df = pd.DataFrame(list(sector_to_int.items()), columns=['sector', 'sector_id'])
    return sector_df


# Removing useless/redundant data before officially going through OHE
def filter_data(df):
    # Encoding the ticker column (OHE can't d o it properly)
    if 'ticker' in df.columns:
        ticker_df = generate_ticker_table()
        df = df.merge(ticker_df, on='ticker', how='left')
        df.drop(columns=['ticker'], inplace=True)
        df.rename(columns={'ticker_id': 'ticker'}, inplace=True)
        df['ticker'] = df['ticker'].astype(int)
    # Encoding the sector column (OHE can't do it properly)
    if 'sector' in df.columns:
        sector_df = generate_sector_table()
        df = df.merge(sector_df, on='sector', how='left')
        df.drop(columns=['sector'], inplace=True)
        df.rename(columns={'sector_id': 'sector'}, inplace=True)
        df['sector'] = df['sector'].astype(int)
    # Removing redundant columns
    columns_to_remove = ['code', 'quarter', 'month_string', 'day_string', 'company', 'day', 'month', 'year']
    for col in columns_to_remove:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    # Pre-encoding the datetime object since OHE doesn't consider it an object (then removing the original 'date')
    if 'date' in df.columns:
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df.drop(columns=['date'], inplace=True)
    # Reordering columns (date stuff coming first)
    if 'day' in df.columns:
        new_order = ['year', 'month', 'day'] + [col for col in df.columns if col not in ['year', 'month', 'day']]
        df = df[new_order]
    return df


# Encoding categorical attributes
def encode_categorical(df):
    encoder = OneHotEncoder()
    # Extracting a list of object-based columns (to be encoded)
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    # Encoding the data
    encoded_data = encoder.fit_transform(df[categorical_columns])
    # Adding the encoded data to a new dataframe
    df_encoded = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out(categorical_columns))
    # Removing categorical columns from the original dataframe and adding the encoded ones
    new_df = df.drop(columns=categorical_columns)
    new_df = pd.concat([new_df, df_encoded], axis=1)
    return new_df


# Normalizing key values found in specific dataframes
def normalize_df(df):
    if 'returns' in df:
        scaler = MinMaxScaler()
        normalize_columns = ['volatility', 'returns']
        df[normalize_columns] = scaler.fit_transform(df[normalize_columns])
        return df
    if 'financial_data_id' in df:
        scaler = MinMaxScaler()
        normalize_columns = ['open', 'close', 'high', 'low', 'volume']
        df[normalize_columns] = scaler.fit_transform(df[normalize_columns])
    if 'population' in df:
        scaler = MinMaxScaler()
        normalize_columns = ['population', 'gdp', 'inflation', 'employment', 'unemployment']
        df[normalize_columns] = scaler.fit_transform(df[normalize_columns])
    return df


def process(df):
    df = filter_data(df)
    df = encode_categorical(df)
    df = normalize_df(df)
    return df


def get_processed_data():
    # Extracting all previously-staged dataframes
    df_country = country.get_staged_df()
    df_company = company.get_staged_df()
    df_date = date.get_staged_df()
    df_financial = financial.get_staged_df()
    df_fact = fact.get_staged_df()
    # Processing and returning the dataframes
    return process(df_country), process(df_company), process(df_date), process(df_financial), process(df_fact)

import preprocessing
import pandas as pd
from sklearn.model_selection import train_test_split


# Combines all staged dataframes into one "super" dataframe, and splits it for the classification task
def split_data():
    # Getting all pre-processed dataframes
    df_country, df_company, df_date, df_financial, df_fact = preprocessing.get_processed_data()
    # Merging all dataframes
    df = df_fact.merge(df_country, on='country_id').drop(columns=['year', 'month', 'day', 'interpolated',
                                                                  'country_Ireland', 'country_Switzerland',
                                                                  'country_United Kingdom', 'country_United States'])
    df = df.merge(df_company, on='company_id').drop(columns=['ticker'])
    df = df.merge(df_financial, on='financial_data_id').drop(columns=['year', 'month', 'day'])
    df = df.merge(df_date, on='date_id').drop(columns=['weekday'])
    # Adding a new column to serve as our target variable (will be stored numerically)
    df['target'] = (df['returns'] > 0).astype(int)
    # Splitting up the data
    # Incomplete
    return df


split_data().to_csv('result.csv', index=False)

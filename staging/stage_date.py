import pandas as pd
import extract.date_extract as src
from os.path import dirname, abspath


def get_df():
    source_dir = dirname(dirname(abspath(__file__)))
    df = pd.read_csv(source_dir + '/data/date_data.csv')
    return df


def get_staged_df():
    source_dir = dirname(dirname(abspath(__file__)))
    src.extract_dates()
    df = pd.read_csv(source_dir + '/data/date_data.csv')
    # Converting the Date column to a datetime object
    df['Date'] = pd.to_datetime(df['Date'])
    # Removing any potential leading and trailing spaces
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    # Generate IDs
    df['Date_ID'] = range(1, len(df) + 1)
    df.set_index('Date_ID', inplace=True)
    # Adding a 'Day_String' and 'Weekday' column
    df['Day_String'] = df['Date'].dt.day_name()
    df['Weekday'] = df['Date'].dt.dayofweek < 5
    return df


x = get_staged_df()
x.to_csv('output.csv')

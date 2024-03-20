import pandas as pd
import stage_company as companies


def get_df():
    df = pd.read_csv('../data/country_data.csv')
    return df


def get_staged_df():
    df = pd.read_csv('../data/country_data.csv')
    # Removing Countries not hosting an S&P 500 company (irrelevant data)
    unique_countries = companies.get_df()['country'].unique().tolist()
    for index, row in df.iterrows():
        if row['Country'] not in unique_countries:
            df.drop(index, inplace=True)
    # Faulty data in 2023 and 2024 so they are removed
    df = df[~df['Year'].isin([2023, 2024])]
    # Setting each 'Year' to {Year}-01-01
    df['Date'] = pd.to_datetime(df['Year'], format='%Y').dt.year.astype(str) + '-01-01'
    df.drop(columns=['Year'], inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.set_index('Date', inplace=True)
    # Interpolating values between years to make the granularity consistent with the whole project
    df = df.groupby('Country').resample('D').asfreq()
    unique_countries.remove('?')
    new_df = pd.DataFrame(columns=df.columns)
    for country in unique_countries:
        temp_df = df.loc[country]
        for attribute in df.columns.tolist():
            if attribute in ['Code', 'Country']:
                temp_df[attribute] = temp_df[attribute].mode()[0]
            else:
                temp_df[attribute] = temp_df[attribute].interpolate(method='time')
        new_df = pd.concat([new_df, temp_df])
    df = new_df.reset_index().rename(columns={'index': 'Date'})
    # Setting a max of 3 floating point digits to simplify data
    df = df.round(3)
    # Removing any potential leading and trailing spaces
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
    return df

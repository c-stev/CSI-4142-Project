import csv
import wbdata
from os.path import exists, dirname, abspath

# Define the indicators
indicators = {
    'Population': 'SP.POP.TOTL',
    'GDP': 'NY.GDP.MKTP.CD',
    'Inflation': 'FP.CPI.TOTL.ZG',
    'Employment': 'SL.EMP.TOTL.SP.ZS',
    'Unemployment': 'SL.UEM.TOTL.ZS'
}


# Function to get data from the World Bank API
def get_data(country_code):
    data = []
    name = wbdata.get_data(indicator='SP.POP.TOTL', country=country_code, date='2000')[0]['country']['value']
    for year in range(2000, 2025):
        temp = {'Code': country_code, 'Year': year, 'Country': name}
        for indicator in indicators:
            try:
                value = wbdata.get_data(indicators[indicator], country=country_code, date=str(year))[0]['value']
            except TypeError:
                print(f"Cannot get data for {indicators[indicator]} for {country_code} in {year}")
            temp.update({indicator: value})
        data.append(temp)

    return data


def extract_countries():
    source_dir = dirname(dirname(abspath(__file__)))
    if not exists(source_dir + '/data/country_data.csv'):
        # Read the country codes from the CSV
        with open(source_dir + '/data/src/countries.csv', mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            country_codes = [row['Code'] for row in reader]

        # Fetch the data for each country and write to a new CSV
        with open(source_dir + '/data/country_data.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Code', 'Year', 'Country', 'Population', 'GDP', 'Inflation', 'Employment', 'Unemployment']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for code in country_codes:
                print(f"Pulling data for country code: {code}")
                country_data = get_data(code)
                for row in country_data:
                    writer.writerow(row)

        print("File 'country_data.csv' successfully created!")
    else:
        print("country_data.csv already exists! Skipping...")

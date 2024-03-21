import csv
import yfinance as yf
from os.path import exists, dirname, abspath


# Makes use of yfinance and obtains the company country
def get_data(symbol, name, sector):
    ticker = yf.Ticker(symbol)
    country = ticker.info.get('country', '?')
    data = {'ticker': symbol.strip(), 'name': name.strip(), 'sector': sector.strip(), 'country': country.strip()}
    return data


def extract_companies():
    source_dir = dirname(dirname(abspath(__file__)))
    if not exists(source_dir + '/data/company_data.csv'):
        print("Pulling data from Yahoo! Finance...")

        # Writes the obtained data from the source file and yfinance to a new company_data.csv file
        with open(source_dir + '/data/company_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['ticker', 'name', 'sector', 'country'])
            writer.writeheader()

            # Reads the original file and obtain the symbol and sector data
            with open(source_dir + '/data/src/SP500.csv', mode='r', encoding='utf-8') as sp500:
                reader = csv.DictReader(sp500)
                for row in reader:
                    row_data = get_data(row['Symbol'], row['Name'], row['Sector'])
                    writer.writerow(row_data)

        print("File 'company_data.csv' successfully created!")
    else:
        print('company_data.csv already exists! Skipping...')

import csv
import yfinance as yf
from os.path import exists, dirname, abspath


# Makes use of yfinance and obtains the company country
def get_data(symbol):
    ticker = yf.Ticker(symbol)
    hist_data = ticker.history(start='2000-01-01', end='2024-01-01')
    data = []
    for index, row in hist_data.iterrows():
        data.append({
            'Ticker': symbol.strip(),
            'Date': index.strftime('%Y-%m-%d'),
            'Open': row['Open'],
            'Close': row['Close'],
            'High': row['High'],
            'Low': row['Low'],
            'Volume': row['Volume'],
            'Dividends': row['Dividends'],
            'Stock Splits': row['Stock Splits']
        })
    return data


def extract_financial_data():
    source_dir = dirname(dirname(abspath(__file__)))
    if not exists(source_dir + '/data/financial_data.csv'):
        print("Pulling data from Yahoo! Finance...")

        # Writes the obtained data from the source file and yfinance to a new company_data.csv file
        with open(source_dir + '/data/financial_data.csv', mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['Ticker', 'Date', 'Open', 'Close', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Reads the original file and obtain the symbol and sector data
            with open(source_dir + '/data/src/SP500.csv', mode='r', encoding='utf-8') as sp500:
                reader = csv.DictReader(sp500)
                for row in reader:
                    row_data = get_data(row['Symbol'])
                    for data_row in row_data:
                        writer.writerow(data_row)

        print("File 'financial_data_extract.csv' successfully created!")
    else:
        print('financial_data.csv already exists! Skipping...')

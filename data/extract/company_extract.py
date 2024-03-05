import csv
import yfinance as yf


def get_data(ticker_str, sector):
    ticker = yf.Ticker(ticker_str)
    data = {
        'ticker': ticker_str.strip(),
        'name': ticker.info.get('longName', '?').strip(),
        'industry': ticker.info.get('industry', '?').strip(),
        'sector': sector.strip(),
        'country': ticker.info.get('country', '?').strip()
    }
    return data


print("Pulling data from Yahoo! Finance...")

with open('../../data/companies.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['ticker', 'name', 'industry', 'sector', 'country'])
    writer.writeheader()

    with open('src/SP500.csv', mode='r', encoding='utf-8') as sp500:
        reader = csv.DictReader(sp500)
        for row in reader:
            data = get_data(row['Symbol'], row['Sector'])
            writer.writerow(data)


print("File 'companies.csv' successfully created!")

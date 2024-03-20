import csv
from datetime import datetime, timedelta
from os.path import exists


def extract_dates():
    if not exists('../data/date_data.csv'):
        with open('../data/date_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Date', 'Year', 'Quarter', 'Month', 'Month_String', 'Day'])
            writer.writeheader()

            start_date = datetime(2000, 1, 1)
            end_date = datetime(2024, 1, 1)

            current_date = start_date
            while current_date < end_date:
                writer.writerow({
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Year': current_date.year,
                    'Quarter': (current_date.month - 1)//3 + 1,
                    'Month': current_date.month,
                    'Month_String': current_date.strftime('%B'),
                    'Day': current_date.day
                })
                current_date += timedelta(days=1)
    else:
        print('date_data.csv already exists! Skipping...')

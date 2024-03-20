import country_extract
import company_extract
import date_extract
import financial_data_extract


def extract_all_files():
    country_extract.extract_countries()
    date_extract.extract_dates()
    financial_data_extract.extract_financial_data()
    company_extract.extract_companies()
    print('Extraction complete!')

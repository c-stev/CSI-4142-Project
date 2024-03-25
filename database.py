import psycopg2
from sqlalchemy import create_engine
import staging.stage_country as stage_country
import staging.stage_company as stage_company
import staging.stage_date as stage_date
import staging.stage_financial_data as stage_fd
import staging.stage_fact as stage_fact


def create_database():
    engine = create_engine('postgresql+psycopg2://postgres:Group43@localhost:5432/postgres')

    connection = psycopg2.connect(host="localhost", dbname="postgres",user= "postgres", password="Group43", port=5432)

    cur = connection.cursor()

    #Drop all the Tables if they exist
    cur.execute("""
        DROP TABLE IF EXISTS fact_stock_analysis;
        DROP TABLE IF EXISTS dim_country;
        DROP TABLE IF EXISTS dim_company;
        DROP TABLE IF EXISTS dim_date;
        DROP TABLE IF EXISTS dim_financial;          
    """)

    #Create the Table for the country dimension
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_country (
            Country_ID serial PRIMARY KEY, 
            date DATE,
            Code VARCHAR(4),
            Country VARCHAR(64),
            Population INTEGER,
            GDP FLOAT,
            Inflation FLOAT,
            Employment FLOAT,
            Unemployment FLOAT,
            Interpolated BOOL    
        );
    """)

    #Create the Table for the company dimension
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_company (
            company_id serial PRIMARY KEY, 
            ticker VARCHAR(5),
            company VARCHAR(64),
            sector VARCHAR(64),
            country VARCHAR(64)
        );
    """)

    #Create the Table for the date dimension
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id serial PRIMARY KEY, 
            date DATE, 
            year INTEGER,
            quarter INTEGER,
            month INTEGER,
            month_string VARCHAR(32),
            day INTEGER,
            day_string VARCHAR(32),
            weekday BOOL
        );
    """)

    #Create the Table for the financial dimension
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dim_financial (
            financial_data_id serial PRIMARY KEY,
            ticker VARCHAR(5),
            date DATE,
            open FLOAT,
            close FLOAT, 
            high FLOAT,
            low FLOAT,
            volume BIGINT
        );
    """)

    #Create the fact Table for the stock analysis dimension
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fact_stock_analysis(
            date_id INTEGER REFERENCES dim_date(date_id),
            company_id INTEGER REFERENCES dim_company(company_id),
            country_id INTEGER REFERENCES dim_country(country_id),
            financial_data_id INTEGER REFERENCES dim_financial(financial_data_id),
            returns FLOAT,
            volatility FLOAT,
            CONSTRAINT pk PRIMARY KEY(
                date_id, company_id, country_id, 
                financial_data_id
            )
        );
    """)

    connection.commit()

    #get all the data frames
    f_country = stage_country.get_staged_df()
    f_country.set_index('country_id', inplace=True)

    f_company = stage_company.get_staged_df()
    f_company.set_index('company_id', inplace=True)

    f_date = stage_date.get_staged_df()
    f_date.set_index('date_id', inplace=True)

    f_financial = stage_fd.get_staged_df()
    f_financial.set_index('financial_data_id', inplace=True)

    f_fact = stage_fact.get_staged_df()
    

    #append the data from all the data frames to their respected tables 
    f_country.to_sql("dim_country", con=engine, method='multi',if_exists='append', index=True, index_label="country_id",dtype=None)
    f_company.to_sql("dim_company", con=engine, method='multi',if_exists='append', index=True, index_label="company_id",dtype=None)
    f_date.to_sql("dim_date", con=engine, method='multi',if_exists='append', index=True, index_label="date_id",dtype=None)
    f_financial.to_sql("dim_financial", con=engine, method='multi',if_exists='append', index=True, index_label="financial_data_id",dtype=None)
    f_fact.to_sql("fact_stock_analysis", con=engine, method='multi',if_exists='append', index=False, index_label=None,dtype=None)

    #close/dispose of all of the connections to the database 
    engine.dispose()
    cur.close()
    connection.close()
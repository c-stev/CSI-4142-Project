# Analyzing Financial Sector Trends with Yahoo! Finance

## Team Members
1. Cole Stevens
2. William Beaupre
3. Emiliano Bustamante

## Project Description
Yahoo! Finance is a powerful source of financial information, including but not limited to stocks, bonds, currencies,
and cryptocurrencies. For this endeavour, publicly traded company data within various sectors will be examined. These sectors
include, but are not limited to, Healthcare, Technology, Financial Services, and more. This information will be
extracted, analyzed, and compared with the other sectors to gain more of an understanding of the relative
stability, volatility, and profitability of each sector. The conclusions that will eventually be drawn will offer valuable
insights that will aid decision-making, trend-analysis, and market understanding.

## Running the project
To run the project you need to create a PostgreSQL database and leave all the options to the default. The server name and 
username should be the same (postgres). The database should be on the local host and port 5432. Within database/database.py, 
please replace all instances of 'password' with your actual database password (lines 11 and 13)

## Directory

| Section                | Description                                                                                            |
|------------------------|--------------------------------------------------------------------------------------------------------|
| [Data](./data)         | This section contains all source CSVs, as well as the CSVs that are generated from the extract folder. |
| [Database](./database) | This section contains code that will import all of the staged data into your PostgreSQL database, as well as run some pre-defined queries to demonstrate the capabilities of the data. |
| [Extract](./extract)   | This section contains code that uses APIs to scrape web data and saves everything locally as a CSV. |
| [Reports](./reports)   | This section contains all of the deliverable reports performed by the team.                             |
| [Staging](./staging)   | This section contains the files that take the CSVs (both downloaded raw or generated through the extract folder) and perform staging operations on it to make it suitable for use in an actual database. |
                |


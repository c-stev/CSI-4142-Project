import json

import pandas as pd
from sqlalchemy import create_engine, text


def execute_query(query):
    # Connecting to the DB
    engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/postgres')
    connection = engine.connect()
    sql_query = text(query)

    # Executing the query
    result = connection.execute(sql_query)

    # Convert the resultant table to a dataframe
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

    # Closing the connection
    connection.close()

    return df


# Path to the JSON file containing the queries
json_file_path = 'queries.json'

# Read queries from the JSON file
with open(json_file_path, 'r') as f:
    queries = json.load(f)

# Execute each query and print the result
for query_key, single_query in queries.items():
    print("Query " + query_key + ":")
    print(execute_query(single_query), "\n")


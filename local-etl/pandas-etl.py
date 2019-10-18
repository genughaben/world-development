import configparser
import pandas as pd
import numpy as np
from tqdm import tqdm
from sql_queries import commodities_staging_table_insert
from time import time
from sqlalchemy import create_engine


def process_commodities(engine, filepath):
    """Processes song files.
     Creates and executes insert queries for songs and artists table.
    Arguments:
    cur -- cursor on a database connection
    filepath -- a path to a json file
    """
    start_time = time()
    conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
    # open song file
    df = pd.read_csv(filepath)

    for idx in tqdm(df.index, total=df.shape[0], position=0, leave=True):
        row = df.loc[idx]

        #commodity_data = row[['country_or_area', 'year','comm_code','commodity','flow','trade_usd','weight_kg','quantity_name','quantity','category']].tolist()

        query = commodities_staging_table_insert % (row['country_or_area'].replace("'", "''"),
                                                    int(row['year'])  if int(row['year']) else 'NULL',
                                                    str(row['comm_code']),
                                                    row['commodity'],
                                                    row['flow'],
                                                    float(row['trade_usd']) if ~np.isnan(row['trade_usd']) else 'NULL',
                                                    float(row['weight_kg']) if ~np.isnan(row['weight_kg']) else 'NULL',
                                                    row['quantity_name'],
                                                    float(row['quantity']) if ~np.isnan(row['quantity']) else 'NULL',
                                                    row['category'])
        try:
            conn.execute(query)
        except:
            print(f"Could not run query: {query}")

    conn.close()
    end_time = time() - start_time
    print(f'duration of commodity processing: {end_time}')


def main():
    """ETLs main data processing function.
    Creates database connection and cursor and processes song and log data.
    """

    config = configparser.ConfigParser()
    config.read('config.cfg')
    input_data = config['PATH']['COMMODITIES_DATA']

    db_prop = config['POSTGRESQL']
    user = db_prop['username']
    password = db_prop['password']
    dbname = db_prop['dbname']

    engine_connection_string = f'postgresql://{user}:{password}@127.0.0.1:5432/{dbname}'
    print(engine_connection_string)
    engine = create_engine(engine_connection_string)
    process_commodities(engine, filepath=input_data)
    engine.close()


if __name__ == "__main__":
    main()
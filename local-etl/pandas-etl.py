import configparser
import pandas as pd
from .sql_queries import commodities_staging_table_insert
from time import time
from sqlalchemy import create_engine


def process_commodities(conn, filepath):
    """Processes song files.
     Creates and executes insert queries for songs and artists table.
    Arguments:
    cur -- cursor on a database connection
    filepath -- a path to a json file
    """
    start_time = time()

    cur = conn.cur()
    # open song file
    df = pd.read_csv(filepath)

    df.to_sql("commodities_staging", conn, if_exists='replace')

    # insert commodity staging
    for idx in df.index:
        row = df.loc[idx]
        commodity_data = row[['country_or_area', 'year','comm_code','commodity','flow','trade_usd','weight_kg','quantity_name','quantity','category']].tolist()

        query = commodities_staging_table_insert % (row['country_or_area'],
                                                    int(row['year'])  if int(row['year']) else None,
                                                    str(row['comm_code']),
                                                    row['commodity'],
                                                    row['flow'],
                                                    float(row['trade_usd']) if float(row['trade_usd']) else None,
                                                    float(row['weight_kg']) if float(row['weight_kg']) else None,
                                                    row['quantity_name'],
                                                    float(row['quantity']) if float(row['quantity']) else None,
                                                    row['category'])
        cur.execute(query)
        conn.commit()

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
    dbname = db_prop['dbname']

    engine = create_engine(f'postgresql://{user}@127.0.0.1:5432/{dbname}')
    process_commodities(engine, filepath=input_data)
    engine.close()


if __name__ == "__main__":
    main()
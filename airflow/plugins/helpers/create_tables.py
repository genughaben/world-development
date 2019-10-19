import sys
from helpers.sql_queries import create_table_queries, drop_table_queries

def drop_tables(redshift):
    '''
    Executes table drops for a given db connection and an associated cursor.
    Drop statements are defined in sql_queries drop_table_queries.
    :param cur:
    :param conn:
    :return:
    '''
    error = "none"
    for query in drop_table_queries:
        try:
            redshift.run(query)
        except Exception as e:
            print(f"Error on creating tables. Current query: {query}")
            print(e)
            error = 'error'
            sys.exit(1)

    print(f"Finished: tables dropped. Error status: {error}")


def create_tables(redshift):
    '''
    Executes table create for a given db connection and an associated cursor.
    Create statements are defined in sql_queries create_table_queries.
    :param cur:
    :param conn:
    :return:
    '''
    error = "none"
    for query in create_table_queries:
        try:
            redshift.run(query)
        except Exception as e:
            print(f"Error on creating tables. Current query: {query}")
            print(e)
            error = 'error'
            sys.exit(1)

    print(f"Finished: tables created. Error status: {error}")


def main(redshift):
    '''
    Execute drop and create tables as prepartion for ETL.
    :return:
    '''

    drop_tables(redshift)
    create_tables(redshift)



def re_create_database_schema(redshift):
    main(redshift)
import psycopg2
from sql_queries import create_table_queries, drop_table_queries




def create_database():
    """Creates database.
    Connects to database. Drops existing and recreates database.
    """
    # connect to default database
    try:
        conn.close()
    except:
        pass

    conn = psycopg2.connect("host=127.0.0.1 dbname=dummy user=genughaben password=")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS world")
    cur.execute("CREATE DATABASE world WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=world user=genughaben password=")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """Drops tables.
    Drops all tables using pre-defined drop table queries.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Creates tables
    Creates all tables using pre-defined drop table queries.
    """

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """ETLs main data structures creataion.
    Drops and recreates all tables and databases.
    """

    try:
        conn.close()
    except:
        pass

    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
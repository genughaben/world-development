# DROP TABLES

commodities_staging_table_drop = "DROP TABLE IF EXISTS commodities_staging;"

# CREATE TABLES

# Staging Tables

commodities_staging_table_create = ("""
    CREATE TABLE IF NOT EXISTS commodities_staging (
        id              SERIAL PRIMARY KEY,
        country_or_area VARCHAR,
        year            SMALLINT,
        comm_code       VARCHAR(6),
        commodity       VARCHAR,
        flow            VARCHAR(9),
        trade_usd       FLOAT,
        weight_kg       FLOAT,
        quantity_name   VARCHAR,
        quantity        FLOAT,
        category        VARCHAR
    );
""")

commodities_staging_table_insert = ("""INSERT INTO commodities_staging (country_or_area, year, comm_code, commodity, flow, trade_usd, weight_kg, quantity_name, quantity, category) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, '%s', %s, '%s');""")


create_table_queries = [commodities_staging_table_create]
drop_table_queries = [commodities_staging_table_drop]

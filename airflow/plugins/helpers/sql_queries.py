staging_commodities_table_drop = "DROP TABLE IF EXISTS commodities_staging;"


# CREATE TABLES

# Staging Tables

staging_commodities_table_create = ("""
    CREATE TABLE IF NOT EXISTS commodities_staging (
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

create_table_queries = [staging_commodities_table_create]
drop_table_queries = [staging_commodities_table_drop]
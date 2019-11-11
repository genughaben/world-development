staging_commodities_table_drop  = "DROP TABLE IF EXISTS commodities_staging;"
staging_temperature_table_drop  = "DROP TABLE IF EXISTS temperature_staging;"
dim_countries_table             = "DROP TABLE IF EXISTS country_or_area;"


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

staging_temperature_table_create = ("""
    CREATE TABLE IF NOT EXISTS temperature_staging (
        year                INT,
        country_or_area     VARCHAR,
        temperature         FLOAT,
        uncertainty         FLOAT
    );
""")


dim_countries_table_create = ("""
    CREATE TABLE IF NOT EXISTS country_or_area (
        country_or_area_id      SERIAL  PRIMARY KEY,
        country_or_area         VARCHAR
    );
""")

create_table_queries    = [ staging_commodities_table_create, staging_temperature_table_create, \
                            dim_countries_table_create ]
drop_table_queries      = [staging_commodities_table_drop, staging_temperature_table_drop, dim_countries_table]
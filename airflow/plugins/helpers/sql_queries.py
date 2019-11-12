staging_commodities_table_drop  = "DROP TABLE IF EXISTS commodities_staging;"
staging_temperature_table_drop  = "DROP TABLE IF EXISTS temperature_staging;"
dim_countries_table_drop        = "DROP TABLE IF EXISTS country_or_area;"
dim_flows_table_drop            = "DROP TABLE IF EXISTS flows;"
dim_quantities_table_drop       = "DROP TABLE IF EXISTS quantities;"
dim_categories_table_drop       = "DROP TABLE IF EXISTS categories;"
dim_commodities_table_drop      = "DROP TABLE IF EXISTS commodities;"
fact_temperatures_table_drop    = "DROP TABLE IF EXISTS temperatures;"
fact_trades_table_drop          = "DROP TABLE IF EXISTS trades"


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


# Dimensions Tables

dim_countries_table_create = ("""
    CREATE TABLE IF NOT EXISTS country_or_area (
        country_or_area_id      SERIAL  PRIMARY KEY,
        country_or_area         VARCHAR
    );
""")

dim_flows_table_create = ("""
    CREATE TABLE IF NOT EXISTS flows (
        flow_id             SERIAL PRIMARY KEY,
        flow_type           VARCHAR
    );
""")

dim_quantities_table_create = ("""
    CREATE TABLE IF NOT EXISTS quantities (
        quantity_id        SERIAL PRIMARY KEY,
        quantity_name       VARCHAR
    );
""")

dim_categories_table_create = ("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id         SERIAL PRIMARY KEY,
        category_name       VARCHAR
    );
""")

dim_commodities_table_create = ("""
    CREATE TABLE IF NOT EXISTS commodities (
        commodity_id        SERIAL PRIMARY KEY,
        commodity_name      VARCHAR,
        commodity_code      VARCHAR, 
        category_id         INT
    );
""")


# Facts Tables

fact_temperatures_table_create = ("""
    CREATE TABLE IF NOT EXISTS temperatures (
        temperature_id      SERIAL PRIMARY KEY,
        year                INT,
        country_or_area_id  INT,
        temperature         FLOAT,
        uncertainty         FLOAT
    );
""")

fact_trades_table_create = ("""
    CREATE TABLE IF NOT EXISTS trades (
        trades_id           SERIAL PRIMARY KEY,
        year                INT,
        country_or_area_id  INT,
        flow_id             INT,
        commodity_id        INT,
        quantity_id         INT,
        quantity_amount     FLOAT,
        trade_usd           FLOAT,
        weight_kg           FLOAT,
        temperature_id      INT
    );
""")


# Table Inserts

dim_flows_table_insert = ("""
    INSERT INTO flows (
        flow_type
    )
    SELECT DISTINCT
        flow                AS flow_type
    FROM commodities_staging;
""")

dim_quantities_table_insert = ("""
    INSERT INTO quantities (
        quantity_name
    )
    SELECT DISTINCT
        quantity_name
    FROM commodities_staging;
""")

dim_categories_table_insert = ("""
    INSERT INTO categories (
        category_name
    )
    SELECT DISTINCT
        category            AS category_name
    FROM commodities_staging;
""")

dim_commodities_table_insert = ("""
    INSERT INTO commodities (
        commodity_name,
        commodity_code,
        category_id
    )
    SELECT DISTINCT
        cs.commodity        AS commodity_name,
        cs.comm_code        AS commodity_code,
        c.category_id 
    FROM commodities_staging cs JOIN 
         categories c ON cs.category = c.category_name;
""")

fact_temperatures_table_insert = ("""
    INSERT INTO temperatures (
        year,
        country_or_area_id,
        temperature,
        uncertainty
    ) 
    SELECT DISTINCT
        ts.year,
        c.country_or_area_id,
        ts.temperature,
        ts.uncertainty
    FROM temperature_staging ts LEFT OUTER JOIN country_or_area c
    ON ts.country_or_area = c.country_or_area;
""")

fact_trades_table_insert = ("""
    INSERT INTO trades (
        year,
        country_or_area_id,
        flow_id,
        commodity_id,
        quantity_id,
        quantity_amount,
        trade_usd,
        weight_kg,
        temperature_id
    )
    SELECT DISTINCT 
        tmp.year, 
        tmp.country_or_area_id,
        tmp.flow_id,
        tmp.commodity_id,
        tmp.quantity_id,
        tmp.quantity_amount,
        tmp.trade_usd,
        tmp.weight_kg,
        tt.temperature_id
    FROM (
        SELECT 
            cs.year,
            ca.country_or_area_id,  
            f.flow_id,
            c.commodity_id,
            q.quantity_id,
            cs.quantity                 AS quantity_amount,  
            cs.trade_usd,   
            cs.weight_kg
        FROM commodities_staging as cs                                         JOIN
            flows as f         ON cs.flow              = f.flow_type           JOIN
            quantities q       ON cs.quantity_name     = q.quantity_name       JOIN
            commodities c        ON (cs.commodity      = c.commodity_name      AND
                                     cs.comm_code      = c.commodity_code )    JOIN
            country_or_area ca ON cs.country_or_area   = ca.country_or_area 
        ) tmp LEFT JOIN ( select temperature_id, year, country_or_area_id
                            from (
                               select *,
                                      row_number() over (partition by year, country_or_area_id) as row_number
                               from temperatures
                               ) as rows
                            where row_number = 1
        ) tt ON (tmp.year = tt.year AND tmp.country_or_area_id = tt.country_or_area_id);
""")


test_check_for_duplicates = """
select count(*)
from (
SELECT 
    country_or_area,
    year,      
    comm_code,    
    commodity,  
    flow,  
    trade_usd,   
    weight_kg,   
    quantity_name,   
    quantity,
    COUNT(*)
FROM commodities_staging
GROUP BY  
    country_or_area,
    year,      
    comm_code,    
    commodity,  
    flow,  
    trade_usd,   
    weight_kg,   
    quantity_name,   
    quantity
HAVING COUNT(*) = 1
) as foo;
"""

test_trades_selection = """
        SELECT count(*)
        FROM (
            SELECT 
                cs.year,
                ca.country_or_area_id,  
                c.commodity_id,  
                f.flow_id,  
                cs.trade_usd,   
                cs.weight_kg,   
                q.quantity_id,
                cs.quantity
            FROM commodities_staging as cs                                         JOIN
                flows as f         ON cs.flow              = f.flow_type           JOIN
                quantities q       ON cs.quantity_name     = q.quantity_name       JOIN
                commodities c        ON (cs.commodity      = c.commodity_name      AND
                                         cs.comm_code      = c.commodity_code )    JOIN
                country_or_area ca ON cs.country_or_area   = ca.country_or_area 
            ) tmp LEFT JOIN ( select temperature_id, year, country_or_area_id
                                from (
                                   select *,
                                          row_number() over (partition by year, country_or_area_id) as row_number
                                   from temperatures
                                   ) as rows
                                where row_number = 1
            ) tt ON (tmp.year = tt.year AND tmp.country_or_area_id = tt.country_or_area_id);
            
            
        SELECT count(*)    
        FROM commodities_staging as cs                                         JOIN
            flows as f         ON cs.flow              = f.flow_type           JOIN
            quantities q       ON cs.quantity_name     = q.quantity_name       JOIN
            country_or_area ca ON cs.country_or_area   = ca.country_or_area LEFT OUTER JOIN
            temperatures t          ON tmp.year = t.year AND tmp.country_or_area_id = t.country_or_area_id;
            commodities c      ON cs.commodity         = c.commodity_name      LEFT OUTER JOIN
            
        ) tmp LEFT OUTER JOIN        
"""

create_table_queries    = [ staging_commodities_table_create, staging_temperature_table_create, \
                            dim_countries_table_create, dim_flows_table_create, dim_quantities_table_create, \
                            dim_categories_table_create, dim_commodities_table_create, fact_temperatures_table_create, \
                            fact_trades_table_create ]

drop_table_queries      = [ staging_commodities_table_drop, staging_temperature_table_drop, dim_countries_table_drop, \
                            dim_flows_table_drop, dim_quantities_table_drop, dim_categories_table_drop, \
                            dim_commodities_table_drop, fact_temperatures_table_drop, fact_trades_table_drop ]

insert_table_queries = {
    'flows'             : dim_flows_table_insert,
    'quantities'        : dim_quantities_table_insert,
    'categories'        : dim_categories_table_insert,
    'commodities'       : dim_commodities_table_insert,
    'temperatures'      : fact_temperatures_table_insert,
    'trades'            : fact_trades_table_insert
}


expected_table_counts = {
    'flows'             : 4,
    'quantities'        : 12,
    'categories'        : 98,
    'country_or_area'   : 249,
    'commodities'       : 5039,
    'temperatures'      : 46606,
    'trades'            : 8225145
}
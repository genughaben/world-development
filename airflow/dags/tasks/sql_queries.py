
# translate_country_labels

update_temperature_country_labels_query = ("""
    UPDATE temperature_staging
    SET country_or_area = '%s' 
    WHERE country_or_area = '%s';
""")

copy_temperature_country_labels_query = ("""
    INSERT INTO temperature_staging (year, country_or_area, temperature, uncertainty)
        SELECT year, '%s', temperature, uncertainty FROM temperature_staging WHERE country_or_area = '%s';
""")

update_commodites_country_labels_query = ("""
    UPDATE commodities_staging
    SET country_or_area = '%s' 
    WHERE country_or_area = '%s';
""")


# create_common_countries_table

drop_dimension_countries_table = """
    DROP TABLE IF EXISTS country_or_area;
"""

create_dimension_countries_table = ("""
    CREATE TABLE IF NOT EXISTS country_or_area (
        country_or_area_id      SERIAL  PRIMARY KEY,
        country_or_area         VARCHAR
    );
""")
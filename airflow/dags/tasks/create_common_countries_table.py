import pandas as pd
from functools import reduce
import operator
import warnings
warnings.filterwarnings('ignore')
from airflow.hooks.postgres_hook import PostgresHook
#from sql_queries import drop_dimension_countries_table, create_dimension_countries_table

def create_common_countries_table():
    postgres_hook = PostgresHook(postgres_conn_id='postgres', schema='world')
    engine = postgres_hook.get_sqlalchemy_engine()
    conn = postgres_hook.get_conn()

    min_year_commodities = postgres_hook.get_first("select min(year) from commodities_staging;")[0]
    max_year_commodities = postgres_hook.get_first("select max(year) from commodities_staging;")[0]

    min_year_commodities = int(min_year_commodities)
    max_year_commodities = int(max_year_commodities)

    print(f"commodities year range: from: {min_year_commodities} to {max_year_commodities}")

    get_countries_from_commodities_staging = "select distinct(country_or_area) from commodities_staging;"
    get_countries_from_temperature_staging = f"select distinct(country_or_area) from temperature_staging where year >= {min_year_commodities} and year <= {max_year_commodities};"

    print(get_countries_from_temperature_staging)

    commodities_countries_records = postgres_hook.get_records(get_countries_from_commodities_staging)
    temperature_countries_records = postgres_hook.get_records(get_countries_from_temperature_staging)

    commodities_countries_list = list(reduce(operator.concat, commodities_countries_records))
    temperature_countries_list = list(reduce(operator.concat, temperature_countries_records))

    commodities_countries_list.sort()
    temperature_countries_list.sort()

    commodities_countries_set = set(commodities_countries_list)
    temperature_countries_set = set(temperature_countries_list)

    print(commodities_countries_list)
    print(temperature_countries_list)
    print(f"commodities_countries count: {len(commodities_countries_list)} and uniques: {len(commodities_countries_set)}")
    print(f"temperature_countries count: {len(temperature_countries_list)} and uniques: {len(temperature_countries_set)}")

    print(f"elements in commodities - not in temperatures: { commodities_countries_set - temperature_countries_set }")
    print(f"elements in temperatures - not in commodities: { temperature_countries_set - commodities_countries_set }")

    common_country_set = commodities_countries_set.union(temperature_countries_set)
    print(f"common_country_set: {common_country_set}")

    table="country_or_area"

    country_or_area_df = pd.DataFrame(list(common_country_set), columns=['country_or_area'])
    country_or_area_df.to_sql(table, engine, index=False, if_exists="append")
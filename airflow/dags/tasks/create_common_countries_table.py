import pandas as pd
from functools import reduce
import operator
import warnings
warnings.filterwarnings('ignore')
from airflow.hooks.postgres_hook import PostgresHook


def create_common_countries_table():
    table = "country_or_area"
    postgres_hook = PostgresHook(postgres_conn_id='postgres', schema='world')
    engine = postgres_hook.get_sqlalchemy_engine()

    min_year_commodities = postgres_hook.get_first("select min(year) from commodities_staging;")[0]
    max_year_commodities = postgres_hook.get_first("select max(year) from commodities_staging;")[0]

    get_countries_from_commodities_staging = "select distinct(country_or_area) from commodities_staging;"
    get_countries_from_temperature_staging = f"select distinct(country_or_area) from temperature_staging where year >= {min_year_commodities} and year <= {max_year_commodities};"

    commodities_countries_records = postgres_hook.get_records(get_countries_from_commodities_staging)
    temperature_countries_records = postgres_hook.get_records(get_countries_from_temperature_staging)

    commodities_countries_set = set(reduce(operator.concat, commodities_countries_records))
    temperature_countries_set = set(reduce(operator.concat, temperature_countries_records))

    common_country_set = commodities_countries_set.union(temperature_countries_set)
    print(f"common_country_set: {common_country_set}")

    country_or_area_df = pd.DataFrame(list(common_country_set), columns=['country_or_area'])
    country_or_area_df.to_sql(table, engine, index=False, if_exists="append")
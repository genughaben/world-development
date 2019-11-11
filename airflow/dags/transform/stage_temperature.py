
#general
import warnings
warnings.filterwarnings('ignore')
from airflow.hooks.postgres_hook import PostgresHook
# data
import pandas as pd


def stage_global_temperatures():
    postgres_hook = PostgresHook(postgres_conn_id='postgres')
    engine = postgres_hook.get_sqlalchemy_engine()

    print(dir(postgres_hook))
    print("engine")
    print(dir(engine))

    table = "temperature_staging"
    # path to file on client system
    file_path = "/usr/local/airflow/dags/data/GlobalLandTemperaturesByCountry.csv"

    df = pd.read_csv(file_path)
    print(f"Raw row count: {len(df)}.")

    check_cols_for_nan = ['dt', 'AverageTemperature', 'Country']
    print(f"Drop rows with nans in columns: {check_cols_for_nan}.")

    df_no_nans = df.dropna(subset=check_cols_for_nan)

    print(f"Count of non-nan rows: {len(df)}")

    # remove duplicate countries, remove regions that have been colonies in the past

    df_no_dup = df_no_nans[~df_no_nans['Country'].isin(
        ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
         'United Kingdom', 'Africa', 'South America'])]

    df_no_dup = df_no_dup.replace(
        ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
        ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

    # add year column and change its type to int

    df_no_dup['year'] = df_no_dup['dt'].str[:4]
    df_no_dup_with_year = df_no_dup.astype({'year': 'int32'})

    # aggregate (mean) temp and uncertainty by year and country

    surface_temp_by_year_and_country = df_no_dup_with_year \
                                            .groupby(['year', 'Country'],as_index=False) \
                                            .agg({ 'AverageTemperature': 'mean', \
                                                   'AverageTemperatureUncertainty': 'mean' \
                                                 })

    surface_temp_by_year_and_country = surface_temp_by_year_and_country.rename(
        columns={"Country": "country_or_area", "AverageTemperature": "temperature",
                 "AverageTemperatureUncertainty": "uncertainty"})

    surface_temp_by_year_and_country.to_sql(table, engine, index=False, if_exists="replace")
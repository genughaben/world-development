import warnings
import boto3
import os
import numpy as np
import configparser
warnings.filterwarnings('ignore')
from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd


def stage_global_temperatures():
    '''
    Staging of temperature data into temperature_staging table.

    Reads GlobalLandTemperaturesByCountry.csv from S3, applies some transformation steps and loads the data into a
    PostgreSQL DB
    '''

    postgres_hook = PostgresHook(postgres_conn_id='postgres')
    engine = postgres_hook.get_sqlalchemy_engine()

    table = "temperature_staging"
    # path to file on client system

    CONFIG_PATH = os.path.expanduser('~/config.cfg')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    s3 = boto3.client(
        's3',
        region_name='eu-central-1',
        aws_access_key_id=config['AWS']['KEY'],
        aws_secret_access_key=config['AWS']['SECRET']
    )

    s3_path = s3.get_object(Bucket='world-development', Key='input_data/GlobalLandTemperaturesByCountry.csv')['Body']

    #file_path = "/usr/local/airflow/dags/data/GlobalLandTemperaturesByCountry.csv"

    df = pd.read_csv(s3_path)
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

    df = df_no_dup_with_year \
                                            .groupby(['year', 'Country'],as_index=False) \
                                            .agg({ 'AverageTemperature': 'mean', \
                                                   'AverageTemperatureUncertainty': 'mean' \
                                                 })

    df = df.rename(
        columns={"Country": "country_or_area", "AverageTemperature": "temperature",
                 "AverageTemperatureUncertainty": "uncertainty"})

    df['rank'] = np.nan

    # add temperature rank for every year by temperature: 1: hottest -> coldest.

    years = df['year'].unique()

    for year in years:
        year_data = df[df['year'] == year]
        sorted_year_data = year_data.sort_values('temperature')
        sorted_year_data['rank'] = sorted_year_data['temperature'].rank(ascending=False)

        for i in sorted_year_data.index:
            rank = sorted_year_data.at[i, 'rank']
            df.at[i, 'rank'] = rank

    df.to_sql(table, engine, index=False, if_exists="replace")
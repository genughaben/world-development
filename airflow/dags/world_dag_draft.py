import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from transform.stage_temperature import stage_global_temperatures
from transform.translate_country_labels import translate_country_labels
from transform.create_common_countries_table import create_common_countries_table

from airflow.operators import (CreateDatabaseSchema, StageToRedshiftOperator)


default_args = {
    'owner': "world",
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': datetime.timedelta(minutes=5),
    'catchup_by_default': False,
    'email_on_retry': False,
    'max_active_runs': 1,
}

dag = DAG(
    "world_dag_draft",
    schedule_interval='@yearly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1)
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)
#
# re_create_db_schema = CreateDatabaseSchema(
#     task_id="Drop_and_create_db_schema",
#     redshift_conn_id="postgres",
#     to_exec=True,
#     dag=dag
# )
#
# stage_commodities_task = BashOperator(
#     task_id='stage_commodities_data',
#     bash_command='/usr/local/airflow/spark/{{params.script_path}} /usr/local/airflow/dags/spark/ /root/',
#     params={'script_path': 'stage_commodities.sh'},
#     dag=dag
# )
#
# stage_global_temperatures_task = PythonOperator(
#     task_id="stage_global_temperatures",
#     python_callable=stage_global_temperatures,
#     dag=dag
# )
#
# translate_country_labels_task = PythonOperator(
#     task_id="translate_country_labels",
#     python_callable=translate_country_labels,
#     dag=dag
# )
#
# create_common_countries_table_task = PythonOperator(
#     task_id='create_common_countries_table',
#     python_callable=create_common_countries_table,
#     dag=dag
# )

dim_flow_table_drop = "DROP TABLE IF EXISTS flows;"
dim_quantities_table_drop = "DROP TABLE IF EXISTS quantities;"
dim_categories_table_drop = "DROP TABLE IF EXISTS categories;"
dim_commodities_table_drop = "DROP TABLE IF EXISTS commodities;"

dim_flow_table_create = ("""
    CREATE TABLE IF NOT EXISTS flows (
        flow_id             SERIAL PRIMARY KEY,
        flow_type           VARCHAR
    );
""")

dim_quantities_table_create = ("""
    CREATE TABLE IF NOT EXISTS quantities (
        quantitiy_id        SERIAL PRIMARY KEY,
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
        commodity_code      VARCHAR 
    );
""")

dim_flow_table_insert = ("""
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
        commodity_code
    )
    SELECT DISTINCT
        commodity           AS commodity_name,
        comm_code           AS commodity_code
    FROM commodities_staging;
""")


fact_temperatures_table_drop = "DROP TABLE IF EXISTS temperatures; "

fact_temperatures_table_create = ("""
    CREATE TABLE IF NOT EXISTS temperatures (
        temperature_id      SERIAL PRIMARY KEY,
        year                INT,
        country_or_area_id  INT,
        temperature         FLOAT,
        uncertainty         FLOAT
    );
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


fact_temperatures_table_drop = "DROP TABLE trades"

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
""")


# todo: finish and test :

fact_trades_table_insert = ("""
    INSERT INTO trades (
        trades_id,
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
        se.ts                 AS start_time,
        se.userId             AS user_id,
        se.level,
        so.song_id            AS song_id,
        se.artist             AS artist_id,
        se.sessionId          AS session_id,
        se.location,
        se.userAgent          AS user_agent
    FROM staging_events se, staging_songs so 
    WHERE se.song = so.title AND page = 'NextSong';
""")



quality_check = {
    'flows'              : 4,
    'quantities'        : 12,
    'categories'        : 98,
    'country_or_ares'   : 249,
    'commodities'       : 5039,
    'temperatures'      : 46606,
}


start_operator


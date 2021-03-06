import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from tasks.stage_temperature import stage_global_temperatures
from tasks.update_and_copy_countries import update_temperature_countries, copy_temperature_countries, \
                                            update_commodity_countries
from tasks.create_common_countries_table import create_common_countries_table

from airflow.operators import (CreateDatabaseSchema, LoadTableOperator, DataQualityOperator, \
                               UpdateTableRowsOperator, CopyTableRowsOperator)

'''
World DAG - Airflow DAG

Orchestrates the whole process of ETL of temperature and commodities data, data schema creation and data import.
'''

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
    "world_dag",
    schedule_interval='@yearly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1)
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

re_create_db_schema = CreateDatabaseSchema(
    task_id="Recreate_db_schema",
    postgres_conn_id="postgres",
    to_exec=True,
    dag=dag
)

stage_commodities_task = BashOperator(
    task_id='stage_commodities',
    bash_command='/usr/local/airflow/spark/{{params.script_path}} /usr/local/airflow/dags/spark/ /root/',
    params={'script_path': 'stage_commodities.sh'},
    dag=dag
)

stage_global_temperatures_task = PythonOperator(
    task_id="stage_temperatures",
    python_callable=stage_global_temperatures,
    dag=dag
)

update_temperature_countries_task = UpdateTableRowsOperator(
    task_id="update_temperature_countries",
    postgres_conn_id="postgres",
    table="temperature_staging",
    column="country_or_area",
    update_dict=update_temperature_countries,
    dag=dag
)

copy_temperature_countries_task = CopyTableRowsOperator(
    task_id="copy_temperature_countries",
    postgres_conn_id="postgres",
    table="temperature_staging",
    column="country_or_area",
    copy_dict=copy_temperature_countries,
    dag=dag
)

update_commodity_countries_task = UpdateTableRowsOperator(
    task_id="update_commodity_countries",
    postgres_conn_id="postgres",
    table="commodities_staging",
    column="country_or_area",
    update_dict=update_commodity_countries,
    dag=dag
)

create_common_countries_table_task = PythonOperator(
    task_id='create_common_countries_table',
    python_callable=create_common_countries_table,
    dag=dag
)

load_flows_table = LoadTableOperator(
    task_id="Load_dim_flows_table",
    postgres_conn_id="postgres",
    table="flows",
    dag=dag
)

load_quantities_table = LoadTableOperator(
    task_id="Load_dim_quantities_table",
    postgres_conn_id="postgres",
    table="quantities",
    dag=dag
)

load_categories_table = LoadTableOperator(
    task_id="Load_dim_categories_table",
    postgres_conn_id="postgres",
    table="categories",
    dag=dag
)

load_commodities_table = LoadTableOperator(
    task_id="Load_dim_commodities_table",
    postgres_conn_id="postgres",
    table="commodities",
    dag=dag
)

load_temperatures_table = LoadTableOperator(
    task_id="Load_fact_temperatures_table",
    postgres_conn_id="postgres",
    table="temperatures",
    dag=dag
)

load_trades_table = LoadTableOperator(
    task_id="Load_fact_trades_table",
    postgres_conn_id="postgres",
    table="trades",
    dag=dag
)

check_data_quality_task = DataQualityOperator(
    task_id="Check_data_quality",
    postgres_conn_id="postgres",
    tables=['flows','quantities', 'categories', 'country_or_area', 'commodities', 'temperatures', 'trades'],
    dag=dag
)

end_operator = DummyOperator(task_id='End_execution',  dag=dag)

start_operator >> re_create_db_schema
re_create_db_schema >> stage_commodities_task
re_create_db_schema >> stage_global_temperatures_task

stage_commodities_task >> update_temperature_countries_task
stage_global_temperatures_task >> update_temperature_countries_task

update_temperature_countries_task >> copy_temperature_countries_task
copy_temperature_countries_task >> update_commodity_countries_task

update_commodity_countries_task >> create_common_countries_table_task
create_common_countries_table_task >> load_temperatures_table

stage_commodities_task >> load_flows_table
stage_commodities_task >> load_quantities_table
stage_commodities_task >> load_categories_table
load_categories_table >> load_commodities_table

load_temperatures_table >> load_trades_table
update_commodity_countries_task >> load_trades_table
load_flows_table >> load_trades_table
load_quantities_table >> load_trades_table
load_categories_table >> load_trades_table
load_commodities_table >> load_trades_table

load_trades_table       >> check_data_quality_task
check_data_quality_task >> end_operator
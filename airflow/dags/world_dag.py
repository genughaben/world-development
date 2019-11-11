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
    "world_dag",
    schedule_interval='@yearly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1)
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

re_create_db_schema = CreateDatabaseSchema(
    task_id="Drop_and_create_db_schema",
    redshift_conn_id="postgres",
    to_exec=True,
    dag=dag
)

stage_commodities_task = BashOperator(
    task_id='stage_commodities_data',
    bash_command='/usr/local/airflow/spark/{{params.script_path}} /usr/local/airflow/dags/spark/ /root/',
    params={'script_path': 'stage_commodities.sh'},
    dag=dag
)

stage_global_temperatures_task = PythonOperator(
    task_id="stage_global_temperatures",
    python_callable=stage_global_temperatures,
    dag=dag
)

translate_country_labels_task = PythonOperator(
    task_id="translate_country_labels",
    python_callable=translate_country_labels,
    dag=dag
)

create_common_countries_table_task = PythonOperator(
    task_id='create_common_countries_table',
    python_callable=create_common_countries_table,
    dag=dag
)

start_operator >> re_create_db_schema
re_create_db_schema >> stage_commodities_task
re_create_db_schema >> stage_global_temperatures_task
stage_commodities_task >> translate_country_labels_task
stage_global_temperatures_task >> translate_country_labels_task
translate_country_labels_task >> create_common_countries_table_task

# stage_global_temperatures_task = BashOperator(
#     task_id='stage_global_temperatures',
#     bash_command='/usr/local/airflow/spark/{{params.script_path}} /usr/local/airflow/dags/spark/ /root/',
#     params={'script_path': 'stage_commodities.sh'},
#     dag=dag
# )

# load_global_temperature_task = BashOperator(
#     task_id='load_global_temperatures',
#
# )

# load_commodities_tables_task = BashOperator(
#     task_id='load_commodities_tables',
#     bash_command='/usr/local/airflow/spark/{{params.script_path}} /usr/local/airflow/dags/spark/ /root/',
#     params={'script_path': 'load_commodities_tables.sh'},
#     dag=dag
# )


#start_operator >> generate_common_countries_table_task #translate_country_labels_task
#translate_country_labels_task >> generate_common_countries_table_task

# start_operator >> stage_global_temperatures_task

# start_operator >> stage_commodities_task
# stage_commodities_task >> load_commodities_tables_task
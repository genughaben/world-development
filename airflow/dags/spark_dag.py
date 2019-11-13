import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

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
    "spark_dag",
    schedule_interval='@weekly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1)
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

show_folder_contents_task = BashOperator(
    task_id='show_folder_contents_task',
    bash_command='ls *',
    dag=dag
)


spark_task = BashOperator(
    task_id='spark_task',
    bash_command='/usr/local/airflow/spark/{{params.script_path}} /usr/local/airflow/dags/spark/ /root/',
    params={'script_path': 'stage_commodities.sh'},
    dag=dag
)

start_operator >> show_folder_contents_task >> spark_task
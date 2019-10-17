from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
#from transform.stage_commodities import spark_commodities_etl


dag = DAG(
    "test_dag",
    start_date=datetime.now()
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

start_operator
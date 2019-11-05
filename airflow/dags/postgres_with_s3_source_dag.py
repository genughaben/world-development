import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (CreateDatabaseSchema, StageToRedshiftOperator)


default_args = {
    'owner': "sparkify",
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': datetime.timedelta(minutes=5),
    'catchup_by_default': False,
    'email_on_retry': False,
    'max_active_runs': 1,
}

dag = DAG(
    "postgres_with_s3_source_dag",
    schedule_interval='@weekly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1)
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

re_create_db_schema = CreateDatabaseSchema(
    task_id="Drop_and_create_db_schema",
    redshift_conn_id="postgres",
    to_exec=True,
    dag=dag
)

commodities_staging_to_redshift = StageToRedshiftOperator(
    task_id="stage_commodities",
    redshift_conn_id="postgres",
    aws_credentials_id="aws_credentials",
    s3_source_region_name="eu-west-1",
    table="commodities_staging",
    s3_bucket="world-development",
    s3_key="input_data/test/commodity_trade_statistics_data.csv",
    dag=dag
)

start_operator >> re_create_db_schema
re_create_db_schema >> commodities_staging_to_redshift
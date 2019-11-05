import datetime
import os
import logging
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator


# todo: implement task to correct input format
# * remove rows with to little entries
# * escape quotes

def load_test_to_postgres(*args, **kwargs):
    conn = PostgresHook(postgres_conn_id='postgres', schema='dummy').get_conn()
    query = 'INSERT INTO test (value) VALUES ("hahahah");'
    cursor = conn.cursor("serverCursor")
    cursor.execute(query)
    cursor.close()
    conn.close()

def display_count(*args, **kwargs):
    conn = PostgresHook(postgres_conn_id='postgres', schema='dummy').get_conn()
    query = 'SELECT count(*) FROM commodities_staging';
    count = conn.get_first(query)[0]
    print(f"result of {query} is {count}")
    conn.close()
    return True


def inspect_folder():
    print(os.getcwd())
    print(os.listdir())
    print(os.listdir('dags/'))
    print(os.listdir('dags/data/'))
    print()

# client side
def copy_task_with_client_file():
    conn = PostgresHook(postgres_conn_id='postgres', schema='dummy').get_conn()
    table = "commodities_staging"
    # path to file on client system
    file_path = "/usr/local/airflow/dags/data/test/commodity_trade_statistics_data.csv"
    cur = conn.cursor()

    with open(file_path, 'r') as f:
        next(f)
        cur.copy_from(f, 'commodities_staging', sep=',')
        conn.commit()

    conn.close()

# server side
def copy_task_with_server_file():
    conn = PostgresHook(postgres_conn_id='postgres', schema='dummy')
    table = "commodities_staging"
    file_path = "/data/test/commodity_trade_statistics_data.csv"

    query = (
        f"COPY {table} "
        f"FROM '{file_path}' "
        f"CSV HEADER; "
    )
    logging.info(f"Executing: {query}")
    print(dir(conn))
    conn.run(query)
    conn.close()

dag = DAG(
    "postgres_with_local_data_dag",
    schedule_interval='@weekly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1)
)

ls_task = PythonOperator(
    task_id="inspect_folder",
    python_callable=inspect_folder,
    dag=dag
)

copy_csv_task = PythonOperator(
    task_id="copy_csv",
    python_callable=copy_task_with_server_file,
    dag=dag
)

count_records_task = PythonOperator(
    task_id='count_records',
    provide_context=True,
    python_callable=display_count,
    dag=dag)


start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

start_operator >> ls_task
ls_task >> copy_csv_task
copy_csv_task >> count_records_task
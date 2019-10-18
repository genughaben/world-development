import datetime
import logging
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator

#
# def load_data_to_postgres(*args, **kwargs):
#     conn = PostgresHook(postgres_conn_id='postgres', schema='dummy').get_conn()
#     query = 'INSERT INTO test (value) VALUES ("hahahah");'
#     cursor = conn.cursor("serverCursor")
#     cursor.execute(query)
#     cursor.close()
#     conn.close()


dag = DAG(
    "test_postgres_dag",
    schedule_interval='@weekly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1)
)

count_task1 = PostgresOperator(
    task_id='count_table_lines1',
    sql=
    """
        SELECT COUNT(*) FROM test;
        INSERT INTO test (value) VALUES ('test');
        SELECT COUNT(*) FROM test;
    """,
    postgres_conn_id='postgres',
    autocommit=True,
    dag=dag,
)

# etl_task = PythonOperator(
#     task_id='etl',
#     provide_context=True,
#     python_callable=load_data_to_postgres,
#     dag=dag)
#
# count_task2= PostgresOperator(
#     task_id='count_table_lines2',
#     sql=
#     """
#     SELECT COUNT(*) FROM dummy.test
#     """,
#     postgres_conn_id='postgres',
#     autocommit=True,
#     dag=dag,
# )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

start_operator >> count_task1
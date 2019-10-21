# from airflow import DAG
# from datetime import datetime, timedelta
# from airflow.contrib.operators.ssh_operator import SSHOperator
#
# default_args = {
#         'owner'                 : 'airflow',
#         'description'           : 'Use of the DockerOperator',
#         'depend_on_past'        : False,
#         'start_date'            : datetime(2018, 1, 3),
#         'email_on_failure'      : False,
#         'email_on_retry'        : False,
#         'retries'               : 1,
#         'retry_delay'           : timedelta(minutes=5)
# }
#
#
# with DAG('spark_dag', default_args=default_args, schedule_interval="5 * * * *", catchup=False) as dag:
#

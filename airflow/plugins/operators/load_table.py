from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import insert_table_queries

class LoadTableOperator(BaseOperator):

    '''LoadTableOperator

     This operator loads data into a table if its insert statment was specified in insert_table_queries.
     It can either replace the currently existing data or append it.
     '''

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 table="",
                 append_only=False,
                 *args, **kwargs):

        super(LoadTableOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.append_only = append_only

    def execute(self, context):
        postgres_hook = PostgresHook(self.postgres_conn_id)

        if self.append_only:
            self.log.info('Remove pre-existing data...')
            postgres_hook.run(f'DELETE FROM {self.table}')
        else:
            self.log.info('Pre-existing data is preseved... new data is appended only.')

        sql_query = insert_table_queries[self.table]
        self.log.info(f"Load data to table {self.table} executing {sql_query} ...")
        ret = postgres_hook.run(sql_query)

        self.log.info(f"Insert data to table {self.table} finished.")
        return ret
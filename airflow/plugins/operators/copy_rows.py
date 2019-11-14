from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import copy_rows_queries

class CopyTableRowsOperator(BaseOperator):

    '''CopyTableRowsOperator

    This operator copies entries of a table.
    Values in copy_dict of format { copy_name: existing_value_to_copy } are used.
    Every <column> of <table> with value <existing_value_to_copy> is copied to a new record where only <copy_name> is
    replaced in <column> for every entry in the dict.
    '''

    ui_color = '#ccccff'

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 table="",
                 column="",
                 copy_dict={},
                 *args, **kwargs):

        super(CopyTableRowsOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.column = column
        self.copy_dict = copy_dict

    def execute(self, context):
        postgres_hook = PostgresHook(self.postgres_conn_id)

        if not self.copy_dict:
            self.log.info('Nothing to be copied if copy_dict is empty.')
        else:
            self.log.info(f'Copying {self.table} with values "previous:new" = {self.copy_dict}')

            query_template = copy_rows_queries[f"{self.table}_{self.column}"]

            for copy_mew, existing in self.copy_dict.items():
                query = query_template % (copy_mew, existing)
                try:
                    postgres_hook.run(query)
                except:
                    print("cound not execute:")
                    print(query)
                    return False

            self.log.info(f"Updating table {self.table} finished.")
        return True
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import create_row_update_query

class UpdateTableRowsOperator(BaseOperator):

    ui_color = '#ffcccc'

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 table="",
                 column="",
                 update_dict={},
                 *args, **kwargs):

        super(UpdateTableRowsOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.column = column
        self.update_dict = update_dict

    def execute(self, context):
        postgres_hook = PostgresHook(self.postgres_conn_id)

        if not self.update_dict:
            self.log.info('Nothing to be updated if update_dict is empty.')
        else:
            self.log.info(f'Updating {self.table} with values "previous:new" = {self.update_dict}')

            for prev_label, new_label in self.update_dict.items():
                query = create_row_update_query(self.table, self.column, new_label, prev_label)
                try:
                    postgres_hook.run(query)
                except:
                    print("cound not execute:")
                    print(query)
                    return False

            self.log.info(f"Updating table {self.table} finished.")
        return True
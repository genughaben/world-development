from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import expected_table_counts

class DataQualityOperator(BaseOperator):

    '''DataQualityOperator

     This operator checks for every table whose names it gets passed as a list of strings, if its total count compares
     to a value defined in expected_table_counts found in helpers.
     '''

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 tables=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id=postgres_conn_id
        self.tables=tables

    def execute(self, context):
        self.log.info('Detect number of entries per table, optionally compare to expected numbers')

        postgres_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        for table in self.tables:

            query = f"SELECT COUNT(*) FROM {table};"
            count = postgres_hook.get_first(query)[0]
            print(f"result of {query} is {count}")

            if table in expected_table_counts.keys():
                expected_count = expected_table_counts[table]
                if count != expected_count:
                    print(f"Validation error: table {table} contains {count} records while {expected_count} where expected.")
                else:
                    print(f"Validation success: table {table} contains {count} records as expected.")
            else:
                if count > 0:
                    print(f"Validation success: table {table} contains {count} records.")
                else:
                    print(f"Validation error: table {table} contains no records while some records where expected.")

        return True
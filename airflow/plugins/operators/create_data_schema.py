from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import re_create_database_schema


class CreateDatabaseSchema(BaseOperator):

    ui_color = '#998866'

    @apply_defaults
    def __init__(self,
                 postgres_conn_id="",
                 to_exec=False,
                 *args, **kwargs):

        super(CreateDatabaseSchema, self).__init__(*args, **kwargs)
        self.postgres_conn_id=postgres_conn_id
        self.to_exec = to_exec


    def execute(self, context):
        if self.to_exec:
            self.log.info(f"Drop and recreate DB schema..")
            postgres_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
            re_create_database_schema(postgres_hook)

            self.log.info(f"Insert data finished.")
        else:
            self.log.info(f"Current schema is kept. Continue.")

        return True


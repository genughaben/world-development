from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 s3_source_region_name="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_source_region_name = s3_source_region_name
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

    def get_copy_statement(self, aws_credentials):
        copy_sql = (
                f"COPY {self.table} "
                f"FROM 's3://{self.s3_bucket}/{self.s3_key}' "
                f"WITH (FORMAT csv); "
        )
        return copy_sql

    def execute(self, context):
        awshook = AwsHook(aws_conn_id=self.aws_credentials_id)
        aws_credentials = awshook.get_credentials(self.s3_source_region_name)
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("First, delete old data before copying new data..")
        self.log.info(f"Executing: DELETE FROM {self.table};")
        redshift.run(f"DELETE FROM {self.table};")

        self.log.info('Copy data from S3 to Redshift')
        copy_stmt = self.get_copy_statement(aws_credentials)
        self.log.info(f"Executing: {copy_stmt}")
        redshift.run(copy_stmt)

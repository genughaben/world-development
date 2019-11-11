S3_PATH=$1
spark-submit \
  --master=spark://spark-master:7077 \
  --driver-class-path=/usr/local/airflow/spark/dependencies/postgresql-42.2.8.jar \
  --jars=/usr/local/airflow/spark/dependencies/postgresql-42.2.8.jar \
  --packages=org.apache.hadoop:hadoop-aws:2.7.0 \
  --executor-memory 4g \
  /usr/local/airflow/spark/scripts/load_commodities_tables.py

SCRIPT_HOME=$1
CLUSTER_HOME=$2
spark-submit \
  --master=spark://spark-master:7077 \
  --driver-class-path=/usr/local/airflow/spark/dependencies/postgresql-42.2.8.jar \
  --jars=/usr/local/airflow/spark/dependencies/postgresql-42.2.8.jar \
  --packages=org.apache.hadoop:hadoop-aws:2.7.0 \
  --executor-memory 4g \
  /usr/local/airflow/spark/scripts/stage_commodities.py

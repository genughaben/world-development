spark-submit \
  --master=spark://<INPUT_SPARK_MASTER_CONTAINER_IP>:7077 \
  --driver-class-path=spark/dependencies/postgresql-42.2.8.jar \
  --jars=spark/dependencies/postgresql-42.2.8.jar \
  --packages=org.apache.hadoop:hadoop-aws:2.7.0 \
   spark/scripts/stage_commodities.py
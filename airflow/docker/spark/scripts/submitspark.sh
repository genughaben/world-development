HOME=$1
spark-submit \
  --master=spark://172.18.0.2:7077 \
  --driver-class-path=dependencies/postgresql-42.2.8.jar \
  --jars=dependencies/postgresql-42.2.8.jar \
  --packages=org.apache.hadoop:hadoop-aws:2.7.0 \
   $HOMEscripts/stage_commodities.py

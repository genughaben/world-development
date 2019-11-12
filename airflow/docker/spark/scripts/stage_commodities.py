import os
import configparser
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s3_path", help="S3 Path to the CSV resource to read in for commodity stage.")
args = parser.parse_args()
if args.s3_path:
    s3_path = args.s3_path
else:
    s3_path = "s3a://world-development/input_data/commodity_trade_statistics_data.csv"

CONFIG_PATH=os.path.expanduser('~/config.cfg')
print(f"path: {CONFIG_PATH}")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

def create_spark_sql_context():
    '''Creates a Spark session.
    Output:
    * spark -- Spark session.
    '''

    spark_prop = config['SPARK']
    jdbc_driver_jar_path = spark_prop['jdbc_driver_jar_path']

    os.environ['PYSPARK_SUBMIT_ARGS'] = f'--jars file:///{os.path.expanduser(jdbc_driver_jar_path)} pyspark-shell'
    os.environ['SPARK_CLASSPATH'] = jdbc_driver_jar_path

    sparkSession = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .config("spark.hadoop.fs.s3a.access.key", config['AWS']['KEY']) \
        .config("spark.hadoop.fs.s3a.secret.key",  config['AWS']['SECRET']) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config('spark.network.timeout', '600s') \
        .config('spark.executor.heartbeatInterval', '60s') \
        .getOrCreate()

    sparkContext = sparkSession.sparkContext
    sqlContext = SQLContext(sparkContext)

    print(f"Spark started with config: \n {sparkContext.getConf().getAll()}\n")

    return sqlContext

def spark_commodities_etl():
    sqlContext = create_spark_sql_context()

    #commodities_data_path = "s3a://world-development/input_data/test/commodity_trade_statistics_data.csv"

    ### READ CSV to PySpark DataFrame

    schema = StructType([
        StructField("country_or_area", StringType(), False),
        StructField("year", IntegerType(), False),
        StructField("comm_code", StringType(), False),
        StructField("commodity", StringType(), False),
        StructField("flow", StringType(), False),
        StructField("trade_usd", DoubleType(), True),
        StructField("weight_kg", DoubleType(), True),
        StructField("quantity_name", StringType(), False),
        StructField("quantity", DoubleType(), True),
        StructField("category", StringType(), False)
    ])

    df = sqlContext.read.format("com.databricks.spark.csv").csv(s3_path, header=True, schema=schema)
    df.printSchema()


    ### CLEAN

    ### Detect and remove nans

    string_columns = ['country_or_area', 'year', 'comm_code', 'commodity', 'flow', 'quantity_name', 'category']
    number_columns = ['trade_usd', 'weight_kg', 'quantity']

    ### Detect and remove nans


    print("Remove records with nan in String Columns")
    col_names = df.columns
    count = df.count()

    for col_name in string_columns:
        print(f"Filter for nans in column: {col_name}")
        df = df.filter(df[col_name].isNotNull())
        old_count = count
        count = df.count()
        print(f"{old_count - count} records based on nan in {col_name} removed. New dataset has {count} records (had {old_count} records before)")


    #### Remove records with nan in Numer Columns

    print("Remove records with nan in Number Columns")
    at_least_one_factual_values = df.filter( df['trade_usd'].isNotNull() | df['weight_kg'].isNotNull() | df['quantity'].isNotNull())


    ### REMOVE DUPLICATES

    at_least_one_factual_values_no_dup = at_least_one_factual_values.dropDuplicates()

    ### WRITE DataFrame to PostgreSQL Database

    db_prop = config['POSTGRESQL']
    db_url = os.path.expanduser(db_prop['url'])
    db_properties = {
        "driver": db_prop['driver'],
        "user": db_prop['username'],
        "password": db_prop['password']
    }

    # mode: can be 'overwrite' or 'append'
    #at_least_one_factual_values.write.jdbc(url=db_url, mode='overwrite', table="commodities_staging", properties=db_properties)

    at_least_one_factual_values_no_dup.write \
        .format("jdbc") \
        .mode("overwrite") \
        .option("url", "jdbc:postgresql://db:5432/world") \
        .option("dbtable", "commodities_staging") \
        .option("user", "genughaben") \
        .option("password", "docker") \
        .save()


spark_commodities_etl()

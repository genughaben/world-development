import os
import configparser
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType


config = configparser.ConfigParser()
config.read('config.cfg')

spark_prop = config['SPARK']
jdbc_driver_jar_path = spark_prop['jdbc_driver_jar_path']

os.environ['PYSPARK_SUBMIT_ARGS'] = f'--jars file:///{jdbc_driver_jar_path} pyspark-shell'
os.environ['SPARK_CLASSPATH'] = jdbc_driver_jar_path


def create_spark_sql_context():
    '''Creates a Spark session.
    Output:
    * spark -- Spark session.
    '''
    sparkSession = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .config('spark.network.timeout', '600s') \
        .config('spark.executor.heartbeatInterval', '60s') \
        .getOrCreate()

    sparkContext = sparkSession.sparkContext
    sqlContext = SQLContext(sparkContext)

    print(f"Spark started with config: \n {sparkContext.getConf().getAll()}\n")

    return sqlContext


def log(df, tab='', msg='', verbose=True):
    ''' Prints schema and count of df as well as a optional message if verbose is True.
    Keyword arguments:
    * df            -- Spark dataframe.
    * tab           -- string: table name
    * msg           -- string: optional message
    * verbose       -- boolean
    '''

    if verbose:
        if msg != '':
            print(msg)
        df.printSchema()
        print(f'count({tab}): {df.count()}')


def process_commodities(sqlContext, db_url, db_properties, input_data, verbose=False):

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

    df = sqlContext.read.format("com.databricks.spark.csv").csv(input_data, header=True, schema=schema)
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
        print(
            f"{old_count - count} records based on nan in {col_name} removed. New dataset has {count} records (had {old_count} records before)")

    #### Remove records with nan in Numer Columns
    print("Remove records with nan in Number Columns")
    at_least_one_factual_values = df.filter(
        df['trade_usd'].isNotNull() | df['weight_kg'].isNotNull() | df['quantity'].isNotNull())
    at_least_one_factual_values

    ### WRITE DataFrame to PostgreSQL Database
    df.write.jdbc(url=db_url, mode='overwrite', table="commodities_staging", properties=db_properties)
    # mode: can be 'overwrite' or 'append'


def main():
    sqlContext = create_spark_sql_context()

    db_prop = config['POSTGRESQL']
    db_url = db_prop['url']
    db_properties = {
        "driver": db_prop['driver'],
        "user": db_prop['username'],
        "password": db_prop['password']
    }
    commodities_data = config['PATH']['COMMODITIES_DATA']

    process_commodities(sqlContext, db_url, db_properties, commodities_data)


if __name__ == "__main__":
    main()
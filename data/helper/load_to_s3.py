import boto3
import configparser
import os

config = configparser.ConfigParser()
config.read('../../config.cfg')
aws = config['AWS']

KEY = aws['KEY']
SECRET = aws['SECRET']

s3 = boto3.client(
    's3',
    region_name='eu-west-1',
    aws_access_key_id=KEY,
    aws_secret_access_key=SECRET
)

bucket = "world-development"

#s3.upload_file("data/test/commodity_trade_statistics_data.csv", bucket, f"input_data/test/commodity_trade_statistics_data.csv")
s3.upload_file("../GlobalLandTemperaturesByCountry.csv", bucket, f"input_data/GlobalLandTemperaturesByCountry.csv")
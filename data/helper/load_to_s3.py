'''
This script helps to upload data to S3

Customize variables:
* source_file_path
* target_bucket
* target_key

and make sure that your AWS credentials in config.cfg are up to date.
'''


import boto3
import configparser

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



source_file_path = "../GlobalLandTemperaturesByCountry.csv"
target_bucket = "world-development"
target_key = "input_data/GlobalLandTemperaturesByCountry.csv"

#s3.upload_file("data/test/commodity_trade_statistics_data.csv", bucket, f"input_data/test/commodity_trade_statistics_data.csv")
s3.upload_file(source_file_path, target_bucket, target_key)
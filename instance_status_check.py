import boto3
import psycopg2
import time
import random

session = boto3.session.Session()
region = session.region_name
db_instance = 'reimagine-dev-canada-instance-1'
print("AWS Region = %s" % (region))

rds_client = boto3.client('rds')
ec2_client = boto3.client('ec2')
kms_client = boto3.client('kms')


describeinstance = rds_client.describe_db_instances()
describeinstance


# check instance status
new_db_instance_status = describeinstance['DBInstances'][0]['DBInstanceStatus']

print(new_db_instance_status)
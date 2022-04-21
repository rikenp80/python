#C:\Users\rpatel3\Documents\GitHub\databases\scripts\create_ad_logins.py --username rpatel3

import sys, argparse
import boto3
import psycopg2
import json

##set connection string using AWS Secrets Manager
#client = boto3.client('secretsmanager')

#response = client.get_secret_value(SecretId='arn:aws:secretsmanager:ca-central-1:497886394954:secret:dev/reimagineUser-3uTMqm')

#secret = json.loads(response['SecretString'])
#user = secret['username']
#password = secret['password']
#host = secret['host']

##set connection string using hard coded connection string
user = 'reimagineUser'
password = ''
host = 'reimagine-prod-canada.cluster-ckrmvhnrbxg7.ca-central-1.rds.amazonaws.com'

parser=argparse.ArgumentParser()
parser.add_argument('--username')
args=parser.parse_args()
print (args)


conn = psycopg2.connect(host=host, database="postgres", user=user, password=password)
cur=conn.cursor()

sql = f'CREATE USER "{args.username}@CORP.TRUEBLUEINC.COM" WITH LOGIN;'
sql = sql + f'GRANT rds_ad TO "{args.username}@CORP.TRUEBLUEINC.COM";\n'
sql = sql + f'GRANT all_db_readonly TO "{args.username}@CORP.TRUEBLUEINC.COM";\n'
print(sql)

cur.execute(sql)

conn.commit()
cur.close()

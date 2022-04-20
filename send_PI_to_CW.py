#C:\Users\rpatel3\Documents\GitHub\databases\scripts\create_ad_logins.py --username rpatel3

import sys, argparse
import boto3
import psycopg2
import json
import time
from datetime import datetime

rds_client = boto3.client('rds')
pi_client = boto3.client('pi')
cw_client = boto3.client('cloudwatch')

query_time = (datetime.utcnow())
#query_time = '2021-08-04 17:00:00'
#query_time = datetime.strptime(query_time, '%Y-%m-%d %H:%M:%S')

current_utc_year = query_time.year
current_utc_month = query_time.month
current_utc_day = query_time.day
current_utc_hour = query_time.hour

start_time = datetime(current_utc_year, current_utc_month, current_utc_day, current_utc_hour-1, 0, 0)
end_time = datetime(current_utc_year, current_utc_month, current_utc_day, current_utc_hour, 0, 0)

print(start_time)
print(end_time)



db_instances = rds_client.describe_db_instances()
db_instances_list = (db_instances['DBInstances'])

for db_instance in db_instances_list:

    if (db_instance['PerformanceInsightsEnabled']) == True:

        DBInstanceIdentifier = (db_instance['DBInstanceIdentifier'])
        DbiResourceId = (db_instance['DbiResourceId'])
        print("Instance: %s" % (DBInstanceIdentifier))
        print("DB_ID: %s" % (DbiResourceId))


        pi_metrics = pi_client.get_resource_metrics(
            ServiceType='RDS',
            Identifier=DbiResourceId,
            MetricQueries=[
                {
                    'Metric': 'db.load.avg',
                    'GroupBy': {
                        'Group': 'db.sql',              
                    },            
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            PeriodInSeconds=60
        )

        metric_list = (pi_metrics['MetricList'])
        metric_list_count = len(metric_list)

        metric_list = (metric_list[2:metric_list_count])

        #print (metric_list)
        #print (metric_list['Key'])
        #print (metric_list['Key']['Metric'])
        #print (metric_list['Key']['Dimensions'])
        #print (metric_list['Key']['Dimensions']['db.sql.statement'])


        for metric_group in metric_list:

            #get dimension info for each metric group
            sql_statement = (metric_group['Key']['Dimensions']['db.sql.statement'])
            sql_tokenized_id = (metric_group['Key']['Dimensions']['db.sql.tokenized_id'])
            
            sql_statement = sql_statement.replace("\r","")
            sql_statement = sql_statement.replace("\n","")
            sql_statement = sql_statement.replace("\t","")
            sql_statement = sql_statement[0:256]
            print(sql_statement)
            

            #get data points for each metric group
            data_points = (metric_group['DataPoints'])
            for data_point in data_points:        

                data_point_timestamp = data_point['Timestamp']
                #send metrics to cloudwatch
                response = cw_client.put_metric_data(
                    Namespace='SQLPerformanceInsights',
                    MetricData=[
                        {
                            'MetricName': 'sql_load',
                            'Dimensions': [
                                {
                                    'Name': 'DBInstanceIdentifier',
                                    'Value': DBInstanceIdentifier
                                },                            
                                {
                                    'Name': 'sql_statement',
                                    'Value': sql_statement
                                },
                            ],
                            'Timestamp': data_point_timestamp,
                            'Value': data_point['Value']
                        },
                    ]
                )


        print("Last Metric Timestamp: %s" % (data_point_timestamp))
        print("Complete")


#python "C:\Users\rpatel3\Documents\Python\restore_aurora_db.py"
 
import boto3
import time

client = boto3.client('cloudwatch')
Namespace = 'AWS/RDS'
DBClusterIdentifier = 'reimagine-dev-canada'
SNS_ARN = 'arn:aws:sns:ca-central-1:497886394954:Database-Notifications'
alarm = client.describe_alarms(AlarmNames=['DB_Connections_Anomaly'])


AlarmName = alarm['MetricAlarms'][0]['AlarmName']
Stat = alarm['MetricAlarms'][0]['Metrics'][0]['MetricStat']['Stat']
Period = alarm['MetricAlarms'][0]['Metrics'][0]['MetricStat']['Period']
Metrics = alarm['MetricAlarms'][0]['Metrics'][0]


MetricName = alarm['MetricAlarms'][0]['Metrics'][0]['MetricStat']['Metric']['MetricName']
Dimensions = alarm['MetricAlarms'][0]['Metrics'][0]['MetricStat']['Metric']['Dimensions']

Dimensions.pop(1)
Dimensions.append({'Name': 'DBClusterIdentifier', 'Value': DBClusterIdentifier})


EvaluationPeriods = alarm['MetricAlarms'][0]['EvaluationPeriods']
DatapointsToAlarm = alarm['MetricAlarms'][0]['DatapointsToAlarm']

ComparisonOperator = alarm['MetricAlarms'][0]['ComparisonOperator']
ThresholdMetricId = alarm['MetricAlarms'][0]['ThresholdMetricId']
TreatMissingData = alarm['MetricAlarms'][0]['TreatMissingData']



alarm = repr(alarm)

file = open("alarm.txt", "w")
file.write(alarm)
file = open("alarm.txt", "r")


("AlarmName=" + AlarmName + "\n" +"AlarmActions="+SNS_ARN + "\n"+"MetricName = "+MetricName )



response = client.put_metric_alarm(
    AlarmName=AlarmName,
    ActionsEnabled=True,
    AlarmActions=SNS_ARN,
    MetricName=MetricName,
    Namespace=Namespace,
    Statistic=Stat,
    Dimensions=Dimensions,
    Period=Period,
    EvaluationPeriods=EvaluationPeriods,
    DatapointsToAlarm=DatapointsToAlarm,
    ComparisonOperator=ComparisonOperator,
    TreatMissingData=TreatMissingData,
    Metrics=Metrics,   
    ThresholdMetricId=ThresholdMetricId
)

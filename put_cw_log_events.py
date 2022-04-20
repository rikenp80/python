import time
import datetime
import boto3


client = boto3.client('logs')


LogGroup='/aws/rds/reimagine-dev-canada/queries/'
LogStream='reimagine-dev-canada-instance-1'


log_streams = client.describe_log_streams(
    logGroupName=LogGroup,
    logStreamNamePrefix=LogStream
)

uploadSequenceToken = (log_streams['logStreams'][0]['uploadSequenceToken'])


epoch_ms = int((time.time())*1000)

client.put_log_events (
    logGroupName=LogGroup,
    logStreamName=LogStream,
    logEvents=[
        {
            'timestamp': epoch_ms,
            'message': 'test5'
        },
    ],
    sequenceToken=uploadSequenceToken
)

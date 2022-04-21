#python C:\Users\rpatel3\Documents\GitHubNew\databases\scripts\delete_snapshots\delete_snapshot_by_cluster_name.py --v_db_cluster_name="from-snap-reimagine-dev-canada"

import boto3
import sys, argparse
import botocore
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

sts_client = boto3.client('sts')
rds_client = boto3.client('rds')


#output AWS account ARN and region
session = boto3.session.Session()
region = session.region_name
account_arn = sts_client.get_caller_identity()["Arn"]

print (account_arn, ("AWS Region = %s" % (region)), sep="\n", end='\n\n')



#define incoming argument
parser = argparse.ArgumentParser()

parser.add_argument('--v_db_cluster_name')

args=parser.parse_args()



#get manual snapshots for specified cluster
manual_snaps = rds_client.describe_db_cluster_snapshots(DBClusterIdentifier=args.v_db_cluster_name, SnapshotType='manual')['DBClusterSnapshots']

#output total number of snapshots
print ("snapshot count = %s" % (len(manual_snaps)), end='\n\n')


#loop through snapshots and delete
for manual_snap in manual_snaps:

    snapshot_name = manual_snap['DBClusterSnapshotIdentifier']
    snapshot_time = manual_snap['SnapshotCreateTime']

    print(snapshot_name)
    print(snapshot_time)
    
    delete_response = rds_client.delete_db_cluster_snapshot(DBClusterSnapshotIdentifier=snapshot_name)
    print (delete_response, end='\n\n')



#get manual snapshots for specified cluster again and output new count
manual_snaps = rds_client.describe_db_cluster_snapshots(DBClusterIdentifier=args.v_db_cluster_name, SnapshotType='manual')['DBClusterSnapshots']
print ("remaining snapshot count = %s" % (len(manual_snaps)))
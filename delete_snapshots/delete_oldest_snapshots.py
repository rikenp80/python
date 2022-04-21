#python C:\Users\rpatel3\Documents\GitHubNew\databases\scripts\delete_snapshots\delete_oldest_snapshots.py --v_delete_threshold=90

import boto3
import sys, argparse
from datetime import datetime, timedelta
import pandas as pd

sts_client = boto3.client('sts')
rds_client = boto3.client('rds')


#output AWS account ARN and region
session = boto3.session.Session()
region = session.region_name
account_arn = sts_client.get_caller_identity()["Arn"]

print (account_arn, ("AWS Region = %s" % (region)), sep="\n", end='\n\n')


#define incoming argument
parser = argparse.ArgumentParser()

parser.add_argument('--v_delete_threshold', type=int)

args=parser.parse_args()


#get count of RDS clusters
clusters = rds_client.describe_db_clusters()['DBClusters']
cluster_count = len(clusters)


#perform a loop for the same number of times as cluster_count value
#e.g. if there are 3 clusters, then loop 3 times to delete 3 snapshots
#this ensures that there will be enough space for new snapshots to be taken for each cluster
for x in range(cluster_count):

    #get all manual snapshots and a count of snapshots
    manual_snaps = rds_client.describe_db_cluster_snapshots(SnapshotType='manual')['DBClusterSnapshots']
    snapshot_count = len(manual_snaps)


    #check if total number of snapshots is more than specified amount. if not, exit script.
    if snapshot_count < args.v_delete_threshold:
        print ("Deleting manual snapshots is not required when there are less than 90 manual snapshots. current snapshot count = %s" % (snapshot_count), end='\n\n')
        exit()
    else:
        print ("snapshot count = %s" % (snapshot_count), end='\n\n')


    #create dataframe of snapshots
    snapshot_name_list = []
    snapshot_time_list = []
    db_cluster_list = []

    for manual_snap in manual_snaps:
        
        snapshot_name_list.append(manual_snap['DBClusterSnapshotIdentifier'])
        snapshot_time_list.append(manual_snap['SnapshotCreateTime'])
        db_cluster_list.append(manual_snap['DBClusterIdentifier'])
        
        
    snapshot_dict = {'snapshot_name': snapshot_name_list, 'snapshot_time': snapshot_time_list, 'db_cluster': db_cluster_list}
    df = pd.DataFrame(data=snapshot_dict)


    #create dataframe with count of snapshots per cluster
    df_counts = (df.groupby(['db_cluster']).size()
    .sort_values(ascending=False)
    .reset_index(name='count'))   

    print (df_counts)


    #get db_cluster with highest snapshot count
    id_cluster_snapshot_max_count = df_counts['count'].idxmax()
    max_count_cluster = df_counts.iloc[id_cluster_snapshot_max_count]['db_cluster']


    #get oldest snapshot in the cluster with the highest snapshot count
    id_earliest_snapshot = df.query('db_cluster == @max_count_cluster')['snapshot_time'].idxmin()
    snapshot_name = df.iloc[id_earliest_snapshot, 0]

    
    delete_response = rds_client.delete_db_cluster_snapshot(DBClusterSnapshotIdentifier=snapshot_name)
    print (delete_response, end='\n\n')


    #get all manual snapshots again and output new count
    manual_snaps = rds_client.describe_db_cluster_snapshots(SnapshotType='manual')['DBClusterSnapshots']
    print ("remaining snapshot count = %s" % (len(manual_snaps)))
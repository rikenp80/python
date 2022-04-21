#python "C:\Users\rpatel3\Documents\GitHubNew\databases\scripts\create_clusters\restore_aurora_db_point_in_time.py" --source_db_cluster=reimagine-dev-us-cluster --new_db_cluster=new-reimagine-dev-us-cluster

 
import boto3
import time
import datetime
import sys, argparse
from Get_DataSubnet_SecGroupID import *
from Check_Cluster_Available import *
from Create_DB_Instances import *

rds_client = boto3.client('rds')


v_Environment='Development' #set to either 'Development', 'Demo', 'Test' or 'Production'


#get 24 hours ago as the default restore point in time
yesterday_datetime = datetime.datetime.now() - datetime.timedelta(days = 1)
restore_to_time_UTC_def = yesterday_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')


#definte incoming arguments
parser=argparse.ArgumentParser()

parser.add_argument('--source_db_cluster')
parser.add_argument('--new_db_cluster')
parser.add_argument('--restore_to_time_UTC', default=restore_to_time_UTC_def)

args=parser.parse_args()


print("Restore Point In Time: %s" % (args.restore_to_time_UTC))



#get source cluster properties
source_db_cluster = rds_client.describe_db_clusters(DBClusterIdentifier=args.source_db_cluster)

#get source db instance properties
source_db_instance = rds_client.describe_db_instances(
    Filters=[
                {
                    'Name': 'db-cluster-id',
                    'Values': [args.source_db_cluster],
                },
            ]
        )


#extract source cluster and instance properties to use in creating new cluster and instance
subnet_group_name = source_db_cluster['DBClusters'][0]['DBSubnetGroup']
cluster_parameter_group = source_db_cluster['DBClusters'][0]['DBClusterParameterGroup']
db_instance_class = source_db_instance['DBInstances'][0]['DBInstanceClass']
db_engine = source_db_instance['DBInstances'][0]['Engine']



#restore DB cluster
response = rds_client.restore_db_cluster_to_point_in_time(
    DBClusterIdentifier= args.new_db_cluster,
    RestoreType='full-copy',
    SourceDBClusterIdentifier= args.source_db_cluster,
    RestoreToTime= args.restore_to_time_UTC,
    DBSubnetGroupName=subnet_group_name,
    CopyTagsToSnapshot= True,
    VpcSecurityGroupIds=Get_DataSubnet_SecurityGroupID(),
    DeletionProtection=True,
    DBClusterParameterGroupName=cluster_parameter_group,
    EnableCloudwatchLogsExports=['postgresql']
)


#keep checking until the cluster is available before moving to next step
Check_Cluster_Available(response)


#create a writer and reader instance
CreateDBInstances(args.new_db_cluster, v_Environment, subnet_group_name)

#python C:\Users\rpatel3\Documents\GitHubNew\databases\scripts\create_clusters\restore_cluster_from_snapshot.py --v_Environment=Development --v_SnapshotIdentifier="autocopy-reimagine-dev-canada-2022-02-19-06-13" --v_ParameterGroupName=reimaginedbparameters12 --v_ClusterIdentifier=test-dev1 --v_DBSubnetGroupName="rds database subnet group"

import sys, argparse
import boto3
from Get_DataSubnet_SecGroupID import *
from Check_Cluster_Available import *
from Create_DB_Instances import *


rds_client = boto3.client('rds')


#define incoming arguments
parser = argparse.ArgumentParser()

parser.add_argument('--v_Environment') #set to either 'Development', 'Demo', 'Test' or 'Production'
parser.add_argument('--v_SnapshotIdentifier')
parser.add_argument('--v_ParameterGroupName')
parser.add_argument('--v_ClusterIdentifier')
parser.add_argument('--v_DBSubnetGroupName')

args=parser.parse_args()



#restore DB cluster
new_cluster = rds_client.restore_db_cluster_from_snapshot(
    DBClusterIdentifier=args.v_ClusterIdentifier,
    SnapshotIdentifier=args.v_SnapshotIdentifier,
    Engine= 'aurora-postgresql',
    DBSubnetGroupName=args.v_DBSubnetGroupName,
    CopyTagsToSnapshot= True,
    VpcSecurityGroupIds=Get_DataSubnet_SecurityGroupID(),
    DeletionProtection=True,
    DBClusterParameterGroupName=args.v_ParameterGroupName,
    EnableCloudwatchLogsExports=['postgresql']
)



#keep checking until the cluster is available before moving to next step
Check_Cluster_Available(new_cluster)


#create a writer and reader instance
CreateDBInstances(args.v_ClusterIdentifier, args.v_Environment, args.v_DBSubnetGroupName)
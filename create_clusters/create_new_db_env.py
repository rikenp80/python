#python C:\Users\rpatel3\Documents\GitHubNew\databases\scripts\create_clusters\create_new_db_env.py --v_Environment=Development --v_EngineVersion=12.4 --v_ParameterGroupName=reimaginedbparameters12 --v_ClusterIdentifier=test-dev1 --v_MasterUserPassword=test1234* --v_DBSubnetGroupName="rds database subnet group"

import boto3
import sys, argparse
import random

from Get_DataSubnet_SecGroupID import *
from Check_Cluster_Available import *
from Get_RDS_KMS_Key import *
from Create_ReimagineClusterParamGroup import *
from Create_DB_Instances import *
from Get_DBSubnetGroupAZs import *

session = boto3.session.Session()
region = session.region_name
print ("AWS Region = %s" % (region))


rds_client = boto3.client('rds')
ec2_client = boto3.client('ec2')


#define incoming arguments
parser = argparse.ArgumentParser()

parser.add_argument('--v_Environment') #set to either 'Development', 'Demo', 'Test' or 'Production'
parser.add_argument('--v_EngineVersion')
parser.add_argument('--v_ParameterGroupName')
parser.add_argument('--v_ClusterIdentifier')
parser.add_argument('--v_MasterUserPassword')
parser.add_argument('--v_DBSubnetGroupName')

args=parser.parse_args()


v_RDSKMSKey = Get_RDS_KMS_Key()


Create_ReimagineClusterParamGroup(args.v_ParameterGroupName, args.v_Environment)


#check if DB CLuster already exists
try:
    DBCluster = rds_client.describe_db_clusters(DBClusterIdentifier=args.v_ClusterIdentifier)
    DBClusterExists = 1
    print ("DB Cluster '%s' already exists" % (args.v_ClusterIdentifier))
except:
    DBClusterExists = 0


#get 3 random AZs from region for use in creating the cluster
ThreeAZsList = random.sample(Get_DBSubnetGroupAZs(args.v_DBSubnetGroupName), 3)


#create DB Cluster
if DBClusterExists == 0:

    new_db_cluster = rds_client.create_db_cluster(
        AvailabilityZones = ThreeAZsList,
        BackupRetentionPeriod=7,
        DBClusterIdentifier = args.v_ClusterIdentifier,
        DBClusterParameterGroupName = args.v_ParameterGroupName,
        DBSubnetGroupName=args.v_DBSubnetGroupName,
        Engine='aurora-postgresql',
        VpcSecurityGroupIds=Get_DataSubnet_SecurityGroupID(),
        EngineVersion=args.v_EngineVersion,
        Port=5432,
        MasterUsername='reimagineUser',
        MasterUserPassword=args.v_MasterUserPassword,
        PreferredBackupWindow='06:00-07:00',
        PreferredMaintenanceWindow='sat:07:00-sat:11:00',
        Tags=[
                    {
                        "Key": "CostCenter",
                        "Value": "9000"
                    },
                    {
                        "Key": "Environment",
                        "Value": args.v_Environment
                    },
                    {
                        "Key": "BusinessUnit",
                        "Value": "PeopleReady"
                    }
                ],
        StorageEncrypted=True,
        EnableIAMDatabaseAuthentication=False,
        EnableCloudwatchLogsExports=['postgresql'],
        EngineMode='provisioned',
        EnableHttpEndpoint=False,
        CopyTagsToSnapshot=True,
        DeletionProtection=True,
        KmsKeyId=v_RDSKMSKey
    )


    #keep checking until the cluster is available before moving to next step
    Check_Cluster_Available(new_db_cluster)    


    #create a writer and reader instance
    CreateDBInstances(args.v_ClusterIdentifier, args.v_Environment, args.v_DBSubnetGroupName, ThreeAZsList)

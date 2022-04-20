
import boto3
import time

client = boto3.client('rds')
dbclusters = client.describe_db_clusters()

for dbcluster in dbclusters['DBClusters']:
    ClusterIdentifier=[]
    ClusterIdentifier.append(dbcluster['DBClusterIdentifier'])
    
    PreferredBackupWindow = (dbcluster['PreferredBackupWindow'])
    PreferredMaintenanceWindow = (dbcluster['PreferredMaintenanceWindow'])
    PreferredBackupWindow = (dbcluster['PreferredBackupWindow'])

    print("\nCLUSTER = %s" % (ClusterIdentifier))
    print("Backup Window = %s " % (PreferredBackupWindow))
    print("Maintenance Window = %s " % (PreferredMaintenanceWindow))   


    for db_cluster_identifier in ClusterIdentifier:

        db_instance = client.describe_db_instances( \
            Filters=[ \
                        { \
                            'Name': 'db-cluster-id', \
                            'Values': [db_cluster_identifier], \
                        }, \
                    ]
                )


        for db in db_instance['DBInstances']:
            DBInstanceIdentifier = (db['DBInstanceIdentifier'])
            PreferredMaintenanceWindow = (db['PreferredMaintenanceWindow'])
            

            print("\n\tINSTANCE = %s" % (DBInstanceIdentifier))
            print("\tMaintenance Window = %s " % (PreferredMaintenanceWindow))
    
    
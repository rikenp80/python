import boto3
import botocore
from botocore.exceptions import ClientError


session = boto3.session.Session()
region = session.region_name
print ("AWS Region = %s" % (region))


rds_client = boto3.client('rds')



auto_snaps = rds_client.describe_db_cluster_snapshots(SnapshotType='automated')['DBClusterSnapshots']

auto_snapshot_arns = []
auto_snapshot_names = []

for auto_snap in auto_snaps:

    auto_snapshot_names.append(auto_snap['DBClusterSnapshotIdentifier'])


for auto_snapshot_name in auto_snapshot_names:
    
    target_snapshot_name = auto_snapshot_name.replace('rds:', 'autocopy-') 

    print("\n=======Copying: %s" % (auto_snapshot_name))
    try:
        rds_client.copy_db_cluster_snapshot(SourceDBClusterSnapshotIdentifier=auto_snapshot_name, TargetDBClusterSnapshotIdentifier=target_snapshot_name, CopyTags=True)
    except rds_client.exceptions.DBClusterSnapshotAlreadyExistsFault as snapshotexists:
       print (snapshotexists.response['Error']['Message'])
    except botocore.exceptions.ClientError as client_error:
        print (client_error.response['Error']['Message'])
    else:
        snapshot_copied = rds_client.describe_db_cluster_snapshots(DBClusterSnapshotIdentifier=target_snapshot_name)['DBClusterSnapshots'][0]['Status']
        if snapshot_copied == 'available':
            print("Successfully copied snapshot: %s" % (auto_snapshot_name))
        else:
            print("Failed to copy snapshot: %s" % (auto_snapshot_name))
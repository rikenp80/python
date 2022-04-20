import boto3
import psycopg2

rds_client = boto3.client('rds')

rds_client.create_db_cluster_snapshot(
    DBClusterSnapshotIdentifier='reimagine-dev-us-cluster-20200824175000',
    DBClusterIdentifier='reimagine-dev-us-cluster'
    )

response = rds_client.copy_db_cluster_snapshot(
    SourceDBClusterSnapshotIdentifier='arn:aws:rds:us-west-2:497886394954:cluster-snapshot:reimagine-dev-us-cluster-20200824175000',
    TargetDBClusterSnapshotIdentifier='reimagine-dev-us-cluster-20200824175000',
    KmsKeyId='arn:aws:kms:ca-central-1:908947454082:key/0cef0d85-e768-44cb-9712-8aa1aef0215a',
    CopyTags=True,
    SourceRegion='us-west-2'
)

def Check_Instance_Available(Instance):

    import boto3
    import time
    rds_client = boto3.client('rds')

    session = boto3.session.Session()
    region = session.region_name

    db_cluster_id = 'clone-reimagine-dev-canada-instance-1-cluster'
    print ("AWS Region = %s" % (region))




    db_instance_status_available = 0
    db_instance_count = -1

    #check every 60 seconds if new instance is available
    while db_instance_status_available != db_instance_count:

        db_instance_status_available = 0

        #check instance status
        db_instances = rds_client.describe_db_instances \
                (
                Filters=[
                    {
                        'Name': 'db-cluster-id',
                        'Values': [db_cluster_id, ]
                    },
                ]
            )['DBInstances']


        db_instance_count = len(db_instances)


        for db_instance in db_instances:

            db_instance_status = db_instance['DBInstanceStatus']

            print("Instance: %s, Status = %s" % (db_instance['DBInstanceIdentifier'], db_instance_status))

            if db_instance_status == 'available':
                db_instance_status_available = db_instance_status_available + 1

        time.sleep(60)
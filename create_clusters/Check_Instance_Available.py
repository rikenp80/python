def Check_Instance_Available(db_cluster_id):

    import boto3
    import time
    rds_client = boto3.client('rds')


    #set initial variable values
    db_instance_available_count = 0
    db_instance_count = -1


    #check every 60 seconds until all instances in the cluster are "available"
    #total count of instances in the cluster must equal count of instances with available status for loop to end
    while db_instance_available_count != db_instance_count:
        
        
        #wait 1 minute before checking
        time.sleep(60)
        
        #reset value for db_instance_available_count
        db_instance_available_count = 0


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
            

        #get count of instances in the cluster
        db_instance_count = len(db_instances)

        
        #check status of each instance and output result
        for db_instance in db_instances:

            db_instance_status = db_instance['DBInstanceStatus']

            print("Instance: %s, Status = %s" % (db_instance['DBInstanceIdentifier'], db_instance_status))

            
            #if instance is "available", add 1 to the counter to get the total number of available instances
            if db_instance_status == 'available':
                db_instance_available_count = db_instance_available_count + 1
                
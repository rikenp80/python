def Create_ReimagineClusterParamGroup(ParameterGroupName, Environment):

    import boto3
    rds_client = boto3.client('rds')


        #check if Parameter Group already exists and set ParameterGroupExists value based on this
    try:
        ParameterGroup = rds_client.describe_db_cluster_parameter_groups(DBClusterParameterGroupName=ParameterGroupName)
        ParameterGroupExists = 1
        print ("Cluster Parameter Group '%s' already exists" % (ParameterGroupName))
    except:
        ParameterGroupExists = 0


    #create parameter group if it does not exist
    if ParameterGroupExists == 0:

        rds_client.create_db_cluster_parameter_group(
            DBClusterParameterGroupName=ParameterGroupName,
            DBParameterGroupFamily='aurora-postgresql12',
            Description='Default parameters with customizations needed for reimagine',
            Tags=[
                {
                    'Key': 'BusinessUnit',
                    'Value': 'PeopleReady'
                },
                {
                    'Key': 'CostCenter',
                    'Value': '9000'
                },
                {
                    'Key': 'Environment',
                    'Value': Environment
                }
            ]
        )

        #modify parameter group settings
        rds_client.modify_db_cluster_parameter_group(
            DBClusterParameterGroupName=ParameterGroupName,
            Parameters=[
                {
                    'ParameterName': 'rds.logical_replication',
                    'ParameterValue': '1',
                    'ApplyMethod': 'pending-reboot',        
                },
                {
                    'ParameterName': 'wal_sender_timeout',
                    'ParameterValue': '0',
                    'ApplyMethod': 'pending-reboot',        
                },        
            ]
        )

        print ("Cluster Parameter Group '%s' created" % (ParameterGroupName))
def CreateDBInstances(v_ClusterName, v_Environment, v_DBSubnetGroupName, AZList=[]):

    import boto3
    import random
    from Get_RDS_KMS_Key import Get_RDS_KMS_Key
    from Get_DBSubnetGroupAZs import Get_DBSubnetGroupAZs
    from Check_Instance_Available import Check_Instance_Available

    rds_client = boto3.client('rds')

    v_RDSKMSKey = Get_RDS_KMS_Key()
    v_DBSubnetGroupName='rds database subnet group'


    #if AZList already has values from input variable then get 2 random AZs for us in instance creation
    #otherwise call the Get_DBSubnetGroupAZs to get 2 random AZs from the DB Subnet Group
    if AZList:
        AZs = random.sample(AZList, 2)        
    else:
        AZs = random.sample(Get_DBSubnetGroupAZs(v_DBSubnetGroupName), 2)

    AZ1 = AZs[0]
    AZ2 = AZs[1]    
 


    rds_client.create_db_instance(
        AvailabilityZone = AZ1,
        DBInstanceIdentifier=v_ClusterName + '-instance1',
        DBClusterIdentifier=v_ClusterName,
        Engine='aurora-postgresql',
        DBSubnetGroupName=v_DBSubnetGroupName,
        DBInstanceClass='db.t3.medium',
        PreferredMaintenanceWindow='sun:07:00-sun:09:00',
        CopyTagsToSnapshot= True,
        EnablePerformanceInsights=True,
        PerformanceInsightsRetentionPeriod=7,
        PerformanceInsightsKMSKeyId=v_RDSKMSKey,    
        Tags=[
            {
                "Key": "CostCenter",
                "Value": "9000"
            },
            {
                "Key": "v_Environment",
                "Value": v_Environment
            },
            {
                "Key": "BusinessUnit",
                "Value": "PeopleReady"
            }
        ],
    )

    
    rds_client.create_db_instance(
        AvailabilityZone = AZ2,
        DBInstanceIdentifier=v_ClusterName + '-instance2',
        DBClusterIdentifier=v_ClusterName,
        Engine='aurora-postgresql',
        DBSubnetGroupName=v_DBSubnetGroupName,
        DBInstanceClass='db.t3.medium',
        PreferredMaintenanceWindow='sun:09:00-sun:11:00',
        CopyTagsToSnapshot= True,
        EnablePerformanceInsights=True,
        PerformanceInsightsRetentionPeriod=7,
        PerformanceInsightsKMSKeyId=v_RDSKMSKey,    
        Tags=[
            {
                "Key": "CostCenter",
                "Value": "9000"
            },
            {
                "Key": "v_Environment",
                "Value": v_Environment
            },
            {
                "Key": "BusinessUnit",
                "Value": "PeopleReady"
            }
        ],
    )


    #keep checking until the instances are available
    Check_Instance_Available(v_ClusterName)

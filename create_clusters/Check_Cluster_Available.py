def Check_Cluster_Available(Cluster):

    import boto3
    import time
    rds_client = boto3.client('rds')

    #get initial status of restoring cluster
    new_cluster_identifier = Cluster['DBCluster']['DBClusterIdentifier']
    new_cluster_status = Cluster['DBCluster']['Status']
    

    #check every 60 seconds if new cluster is available
    while new_cluster_status != 'available':
        #print cluster status
        print("Creating Cluster: %s, Status = %s" % (new_cluster_identifier, new_cluster_status))

        time.sleep(60)

        #check cluster status
        new_cluster_status = (rds_client.describe_db_clusters(DBClusterIdentifier=new_cluster_identifier)['DBClusters'][0]['Status'])

    #print final cluster status
    print("Creating Cluster: %s, Status = %s" % (new_cluster_identifier, new_cluster_status))    

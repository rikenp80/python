def Get_DBSubnetGroupAZs(v_DBSubnetGroupName):

    import boto3
    rds_client = boto3.client('rds')

    rds_subnet = rds_client.describe_db_subnet_groups (DBSubnetGroupName=v_DBSubnetGroupName)
    subnets = (rds_subnet['DBSubnetGroups'][0]['Subnets'])

    AZs = []
    for subnet in subnets:
        AZs.append(subnet['SubnetAvailabilityZone']['Name'])

    return AZs
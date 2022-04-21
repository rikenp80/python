def Get_AZforRegion():

    import boto3
    ec2_client = boto3.client('ec2')

    #get availability zones for current region
    AZs = ec2_client.describe_availability_zones() 
    AZs = (AZs['AvailabilityZones'][::])

    Zones = []
    for AZ in AZs:
        Zones.append(AZ['ZoneName'])

    return Zones
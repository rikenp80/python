def Get_DataSubnet_SecurityGroupID():

    import boto3
    ec2_client = boto3.client('ec2')

    v_DataSubnet_SecurityGroupID = []

    data_sg = ec2_client.describe_security_groups (Filters=[{'Name':'group-name','Values':['Data Subnet Security Group']}])
    data_sg_group = (data_sg['SecurityGroups'])

    for group in data_sg_group:
        v_DataSubnet_SecurityGroupID.append(group['GroupId'])

    return v_DataSubnet_SecurityGroupID
def Get_RDS_KMS_Key():

    import boto3
    kms_client = boto3.client('kms')

    rds_kms_listaliases = kms_client.list_aliases()

    kms_aliases = (rds_kms_listaliases['Aliases'])

    for kms_alias in kms_aliases:

        kms_alias_name = (kms_alias['AliasName'])

        #if alias name is like KMS-RDS then get the key ID and exit loop
        if 'KMS-RDS' in kms_alias_name:
            v_KmsKeyId = (kms_alias['TargetKeyId'])
            break

    return v_KmsKeyId
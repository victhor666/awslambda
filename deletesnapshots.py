import boto3


def lambda_handler(event, context):
    #todo igual menos esta linea para que filtre los de esta cuenta, si no saca los públicos que son un cerro de snapshots
    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ec2 = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2.describe_regions()['Regions']]

    for region in regions:
        print("Region:", region)
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_snapshots(OwnerIds=[account_id])
        snapshots = response["Snapshots"]

        # Se ordenan por hora de inicio
        snapshots.sort(key=lambda x: x["StartTime"])

        # Eliminamos los x últimos, en este caso, 2
        snapshots = snapshots[:-2]

        for snapshot in snapshots:
            id = snapshot['SnapshotId']
            try:
                print("Deleting snapshot:", id)
                ec2.delete_snapshot(SnapshotId=id)
            except Exception as e:
                print("Snapshot {} in use, skipping.".format(id))
                continue
                #esto se puede trabajar un poco mas para que notifique o algo si ha fallado...para la v2

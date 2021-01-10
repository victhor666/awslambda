from datetime import datetime

import boto3


def lambda_handler(event, context):

    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    #listamos las regiones donde puedan existir maquinas
    for region in regions:

        print('Instances in EC2 Region {0}:'.format(region))
        ec2 = boto3.resource('ec2', region_name=region)
        #esta es importante, esto va por tags, las máquinas que queramos salvaguardar tienen que tener este tag en true
        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:backup', 'Values': ['true']}
            ]
        )

        # ISO 8601 timestamp, i.e. 2019-01-31T14:01:58
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
        #y aqui hacemos backup de los volumenes de cada maquina 
        for i in instances.all():
            for v in i.volumes.all():

                desc = 'Backup of {0}, volume {1}, created {2}'.format(
                    i.id, v.id, timestamp)
                print(desc)

                snapshot = v.create_snapshot(Description=desc)

                print("Created snapshot:", snapshot.id)

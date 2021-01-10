#codigo para la lambda

import boto3

def handler (event,context):
    ec2_client=boto3.client('ec2')
    #esta primera parte únicamente enumera las regiones
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]
    for region in regions:
        ec2=boto3.resource('ec2',region_name=region)
        print ("Region:",region)
        #ahora lista las que estan encendidas
        instances=ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name',
                'Values':['running']}])
        #y las para. si queremos que las arranque...no hay mas que hacer uqe en lugar de stop() haga start()
        for instance in instances:
            instance.stop()
            print("Instancua parada:",instance.id)

import uuid
import googleapiclient.discovery
from google.cloud import runtimeconfig
from google.cloud import storage
from oauth2client.client import GoogleCredentials
import os
import time

def cloud_fn_stop_all_servers(event, context):
    """
    Simply stops all servers in the project. This is meant to run periodically to prevent servers from running
    constantly
    :param event: No data is passed to this function
    :param context: No data is passed to this function
    :return:
    """
    runtimeconfig_client = runtimeconfig.Client()
    myconfig = runtimeconfig_client.config('cybergym')
    project = myconfig.get_variable('project').value.decode("utf-8")
    zone = myconfig.get_variable('zone').value.decode("utf-8")

    compute = googleapiclient.discovery.build('compute', 'v1')
    result = compute.instances().list(project=project, zone=zone).execute()
    if 'items' in result:
        for vm_instance in result['items']:
            compute.instances().stop(project=project, zone=zone, instance=vm_instance["name"]).execute()


def cloud_fn_your_cloud_function(event, context):
    """
    This is your function
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    Returns:
        A success status
    """

    action = event['attributes']['action'] if 'action' in event['attributes'] else None

    if not action:
        print(f'No action provided in cloud_fn_manage_server for published message.')
        return

    if action == "build":
        """""
        runtimeconfig_client = runtimeconfig.Client()
        myconfig = runtimeconfig_client.config('cybergym')
        project = myconfig.get_variable('project').value.decode("utf-8")
        zone = myconfig.get_variable('zone').value.decode("utf-8")

        server_name = f"auto_server-{uuid.uuid4()}"
        compute = googleapiclient.discovery.build('compute', 'v1')
        image_response = compute.images().getFromFamily(project="debian-cloud", family="debian-9").execute()
        source_disk_image = image_response["selfLink"]
        config = {
            "name": server_name,
            "machineType": f"projects/{project}/zones/{zone}/machineTypes/e2-micro",
            "disks": [
                {
                    "boot": True,
                    "autoDelete": True,
                    "initializeParams": {
                        "sourceImage": source_disk_image,
                    }
                }
            ],
            "networkInterfaces": [{
                "network": "global/networks/default",
                "accessConfigs": [
                    {"type": "ONE_TO_ONE_NAT", "name": "External NAT"}
                ]
            }],
        }
        result = compute.instances().insert(project=project, zone=zone, body=config).execute()
        return result
        """
        '''''
        compute = googleapiclient.discovery.build('compute', 'v1')

        print('Creating instance.')
        project = 'cpsc5387'
        zone = 'US-CENTRAL1'
        instance_name = 'computOne'
        bucket = 'bucketComputeOne'
        operation = create_instance(compute, project, zone, instance_name, bucket)
        wait_for_operation(compute, project, zone, operation['name'])

        instances = list_instances(compute, project, zone)

        print('Instances in project %s and zone %s:' % (project, zone))
        for instance in instances:
            print(' - ' + instance['name'])
        '''
        
        compute = googleapiclient.discovery.build('compute', 'v1')
        project = 'cpsc5387'
        zone = 'us-central1-a'
        name = 'computone'
        bucket = 'function_mybucket_computone'
        image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-9').execute()
        source_disk_image = image_response['selfLink']

        # Configure the machine
        machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
        startup_script = 'https://storage.cloud.google.com/bucket_startup_script/startup-script.sh'
        image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
        image_caption = "Ready for dessert?"

        config = {
            'name': name,
            'machineType': machine_type,

            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': source_disk_image,
                    }
                }
            ],

            # Specify a network interface with NAT to access the public
            # internet.
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            # Allow the instance to access cloud storage and logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/devstorage.read_write',
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }],

            # Metadata is readable from the instance and allows you to
            # pass configuration from deployment scripts to instances.
            'metadata': {
                'items': [{
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    'key': 'startup-script',
                    'value': startup_script
                }, {
                    'key': 'url',
                    'value': image_url
                }, {
                    'key': 'text',
                    'value': image_caption
                }, {
                    'key': 'bucket',
                    'value': bucket
                }]
            }
        }

        return compute.instances().insert(
            project=project,
            zone=zone,
            body=config).execute()
        '''
        credentials = GoogleCredentials.get_application_default()

        service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

        # Project ID for this request.
        project = 'cpsc5387'  # TODO: Update placeholder value.

        # The name of the zone for this request.
        #zone = 'us-central1-a'  # TODO: Update placeholder value.
        runtimeconfig_client = runtimeconfig.Client()
        myconfig = runtimeconfig_client.config('cybergym')
        zone = myconfig.get_variable('zone').value.decode("utf-8")
        instance_body = {
            # TODO: Add desired entries to the request body.
            # not sure what to do
        }

        request = service.instances().insert(project=project, zone=zone, body=instance_body)
        response = request.execute()

        # TODO: Change code below to process the `response` dict:
        # not sure what to do
        return response
        '''
    elif action == "bucket":
        
        bucket_name = "function_mybucket"

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "COLDLINE"
        new_bucket = storage_client.create_bucket(bucket, location="us")

        print(
            "Created bucket {} in {} with storage class {}".format(
                new_bucket.name, new_bucket.location, new_bucket.storage_class
            )
        )
        return new_bucket

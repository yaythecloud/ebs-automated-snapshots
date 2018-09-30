import boto3
import datetime
from datetime import date
from datetime import time
import calendar
import json

def create_backups():
    c = boto3.client('ec2', region_name='us-east-1')
    
    print ("---Daily Backup Job Starting-"+"---Time in UTC---")
    
    # check to see if its monday and set the tag:backup value: Monthly or Daily
    today = date.today()
    if today.day == 1:
        version = "Monthly"
        print(version)
    else:
        version = "Daily"
        print(version)
    
    # retrieving instances for backup job based on tag:Environment Value: Test or Prod
    volumes = c.describe_volumes(
        Filters = [
            {
                'Name': 'tag:Environment',
                'Values': [
                    'Test',
                    'Prod'
                ]
            },
        ]
    ).get(
        'Volumes', [])
    print("---volumes available based on tag:Environment with the Values:Test and Prod---")
    print(volumes)
    print("---total number of volumes--- %s" % len(volumes))
    
    # look through volumes and print their volumeIds. If the volume has a tag of Name: Value take a snapshot and carry the version and tag_val
    for volume in volumes:
        vol_Id = volume['VolumeId']
        print("---printing the volumeId---")
        print(volume)
        for name in volume['Tags']:
            tag_key = name['Key']
            tag_val = name['Value']
            if tag_key == 'Name':
                snap = c.create_snapshot(
                    VolumeId = vol_Id,
                    Description = 'Automated Snapshot',
                    TagSpecifications=[
                        {
                            'ResourceType': 'snapshot',
                            'Tags': [
                                {
                                    'Key': 'Backup',
                                    'Value': version
                                },
                                {
                                    'Key': 'Maintenance',
                                    'Value': 'False'
                                },
                                {
                                    'Key': 'Created',
                                    'Value': "%s " % date.today()
                                },
                                {
                                    'Key': 'Retention',
                                    'Value': "Delete On"
                                },
                                {
                                    'Key': 'Name',
                                    'Value': tag_val
                                }
                            ]
                        }
                    ]
                )
    


def lambda_handler(event, context):
    
    create_backups()
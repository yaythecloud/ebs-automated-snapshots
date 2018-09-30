import boto3
import datetime
from datetime import date
from datetime import time
import json

def ebs_Snap_Handler():
    c = boto3.client('ec2', region_name='us-east-1')
    
    print("---ebs snapshots handler starting---")
    
    # create a list with daily and monthly
    versions = ["Daily", "Monthly"]
    # create delete_on variable that equals todays date in y-m-d format
    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    
    
    # get snapshots that have the tag key values
    snapshots_response = c.describe_snapshots(
        Filters=[
            {
                'Name': 'tag:Backup',
                'Values': [
                    'Monthly',
                    'Daily'
                ]
            },
            {
                'Name': 'tag:Retention',
                'Values': [
                    'Delete On'
                ]
            }
        ]
    ).get(
        'Snapshots', [])
    print("---snapshots available based on tag filter---")
    print(snapshots_response)
    print("---number of volumes with tag values---")
    print("%s " % len(snapshots_response))
    
    # look through snapshots and print the snapshotId
    for snaps in snapshots_response:
        print("---printing snapshot id---")
        snap_Id = snaps['SnapshotId']
        print(snap_Id)
        #  look through snapshot tags and if they have the value Daily and 
        #  the date the snapshot was taken was today add 30 days to the 
        #  date and add that value to the retention tag
        for t in snaps['Tags']:
            tag_key = t['Key']
            tag_val = t['Value']
            if tag_val == 'Daily' and datetime.datetime.today():
                createdDate = (snaps['StartTime']).date()
                print("---current date of snapshot creation---%s " % createdDate)
                dailyDate = (createdDate + datetime.timedelta(days=30))
                print("---date when daily snap will be deleted---%s " % dailyDate)
                tag_create = c.create_tags(
                    Resources = [
                        snaps['SnapshotId']
                    ],
                    Tags = [
                        {
                            'Key': 'Retention',
                            'Value': str(dailyDate)
                        }
                    ]
                )
            # else if the snapshot tag equals Monthly and the date the 
            # snapshot was taken was today add 365 days to the date
            # and add that value to the retention tag
            elif tag_val == 'Monthly' and datetime.datetime.today():
                createdDate = (snaps['StartTime']).date()
                print("---current date of snapshot creation---%s " % createdDate)
                monthlyDate = (createdDate + datetime.timedelta(days=365))
                print("---date when monthly snap will be deleted ---%s " % monthlyDate)
                tag_create = c.create_tags(
                    Resources = [
                        snaps['SnapshotId']
                    ],
                    Tags = [
                        {
                            'Key': 'Retention',
                            'Value': str(monthlyDate)
                        }
                    ]
                )

def lambda_handler(event, context):
    
    ebs_Snap_Handler()
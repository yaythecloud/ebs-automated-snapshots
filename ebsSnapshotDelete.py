import boto3
import datetime
from datetime import date
from datetime import time
import json

def ebs_Daily_Delete():
    c = boto3.client('ec2', region_name='us-east-1')
    
    print("---ebs daily delete function starting---")
    
    # get snapshots based on daily or monthly tag values
    get_snapshots = c.describe_snapshots(
        Filters = [
            {
                'Name': 'tag:Backup',
                'Values': [
                    'Daily',
                    'Monthly'
                ]
            }
        ]
    ).get(
        'Snapshots', [])
    print("---snapshots available based on tag filter---")
    print(get_snapshots)
    
    # look through snapshots and print snapshotId
    for snaps in get_snapshots:
        print("---printing snapshot id---")
        snap_Id = snaps['SnapshotId']
        print(snap_Id)
        # look through snapshot tags and if retention tag holds a value of today delete it
        for t in snaps['Tags']:
            tag_key = t['Key']
            tag_val = t['Value']
            if tag_key == 'Retention' and tag_val == datetime.date.today().strftime('%Y-%m-%d'):
                print(snaps)
                snap_del = c.delete_snapshot(
                        SnapshotId = snaps['SnapshotId']
                )
            # if retention key does not equal today print no snapshots to delete
            elif tag_key == 'Retention' and tag_val != datetime.date.today().strftime('%Y-%m-%d'):
                print("---no snapshots to delete---")
                
def lambda_handler(event, context):
    
    ebs_Daily_Delete()
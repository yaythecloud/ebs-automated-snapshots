import boto3
import datetime
from datetime import date
from datetime import time
import json

def ebs_Daily_Delete():
    c = boto3.client('ec2', region_name='us-east-1')
    
    print("---ebs daily delete function starting---")
    
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
    
    for snaps in get_snapshots:
        print("---printing snapshot id---")
        snap_Id = snaps['SnapshotId']
        print(snap_Id)
        for t in snaps['Tags']:
            tag_key = t['Key']
            tag_val = t['Value']
            if tag_key == 'Retention' and tag_val == datetime.date.today().strftime('%Y-%m-%d'):
                print(snaps)
                snap_del = c.delete_snapshot(
                        SnapshotId = snaps['SnapshotId']
                )
            elif tag_key == 'Retention' and tag_val != datetime.date.today().strftime('%Y-%m-%d'):
                print("---no snapshots to delete---")
                
def lambda_handler(event, context):
    
    ebs_Daily_Delete()
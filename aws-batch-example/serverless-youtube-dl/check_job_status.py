from __future__ import unicode_literals

import boto3
import json
import os
import sys
from boto3.dynamodb.conditions import Key, Attr

class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def check(job_id):

    print("job_id: " + job_id)

    dynamo_client = get_dynamo_client()
    batch_client = get_batch_client()

    res = dynamo_client.query(
        TableName=os.environ[dynamo_table],
        ProjectionExpression='batch_job_id, video_id',
        KeyConditionExpression='job_id = :job_id',
        FilterExpression='NOT (#BSTS IN (:succeeded, :failed))',
        ExpressionAttributeValues={
            ':job_id': {'S': job_id},
            ':succeeded': {'S': 'SUCCEEDED'},
            ':failed': {'S': 'FAILED'}
        },
        ExpressionAttributeNames={
            '#BSTS': 'batch_job_status'
        },
    )

    incomplete_jobs = 0

    for i in res[u'Items']:
        print("Received Items: " + json.dumps(i, indent=2))

        batch_job_id = i['batch_job_id']['S']
        video_id = i['video_id']['S']

        response = batch_client.describe_jobs(jobs=[batch_job_id])

        batch_job_status = response['jobs'][0]['status']

        if batch_job_status != "SUCCEEDED" or batch_job_status != "FAILED":
            print("batch_job_status: " + batch_job_status)
            incomplete_jobs += 1

        dynamo_client.update_item(
            TableName=os.environ[dynamo_table],
            Key={
                'job_id': {
                    'S': job_id
                },
                'video_id': {
                    'S': video_id
                }
            },
            UpdateExpression='SET #BSTS = :bsts',
            ExpressionAttributeNames={
                '#BSTS': 'batch_job_status'
            },
            ExpressionAttributeValues={
                ':bsts': {
                    'S': batch_job_status
                }
            }
        )

    return incomplete_jobs

def get_dynamo_client():
    try:
        session = boto3.Session()
        
        if session.get_credentials() is None:
            session = boto3.Session(aws_access_key_id=os.environ[aws_access_key_id],
                                    aws_secret_access_key=os.environ[aws_secret_access_key])
            
        return session.client('dynamodb')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def get_batch_client():
    try:
        session = boto3.Session()
        
        if session.get_credentials() is None:
            session = boto3.Session(aws_access_key_id=os.environ[aws_access_key_id],
                                    aws_secret_access_key=os.environ[aws_secret_access_key])
            
        return session.client('batch')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

aws_access_key_id = 'AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'AWS_SECRET_ACCESS_KEY'
dynamo_table = 'DYNAMODB_TABLE'
job_definition = 'JOB_DEFINITION'
job_queue = 'JOB_QUEUE'

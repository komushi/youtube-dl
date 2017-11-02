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

def submit(job_id):

    print("job_id: " + job_id)

    dynamo_client = get_dynamo_client()
    batch_client = get_batch_client()

    res = dynamo_client.query(
        TableName=os.environ[dynamo_table],
        ProjectionExpression='video_id, video_url, video_title',
        KeyConditionExpression='job_id = :job_id',
        ExpressionAttributeValues={
            ':job_id': {'S': job_id}
        },
    )

    for i in res[u'Items']:
        print("Received Items: " + json.dumps(i, indent=2))

        video_title = i['video_title']['S']
        video_url = i['video_url']['S']
        video_id = i['video_id']['S']
        job_name = "{0}-{1}".format(video_id, job_id)

        print("jobName: " + job_name)
        print("video_url: " + video_url)
        print("video_title: " + video_title)

        response = batch_client.submit_job(
            jobName=job_name,
            jobQueue=os.environ[job_queue],
            jobDefinition=os.environ[job_definition],
            parameters={
                'url': video_url
            }
        )

        print("batch job id: " + json.dumps(response, indent=2))

        dynamo_client.update_item(
            TableName='youtube_jobs',
            Key={
                'job_id': {
                    'S': job_id
                },
                'video_id': {
                    'S': video_id
                }
            },
            UpdateExpression='SET #BAT = :bat, #STS = :sts',
            ExpressionAttributeNames={
                '#BAT': 'batch_job_id',
                '#STS': 'job_status'
            },
            ExpressionAttributeValues={
                ':bat': {
                    'S': response['jobId']
                },
                ':sts': {
                    'S': 'SUBMITTED'
                }
            }
        )



def get_dynamo_client():
    try:
        session = boto3.Session()
        
        if session.get_credentials() is None:
            session = boto3.Session(aws_access_key_id=os.environ[aws_access_key],
                                    aws_secret_access_key=os.environ[aws_secret_key])
            
        return session.client('dynamodb')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def get_batch_client():
    try:
        session = boto3.Session()
        
        if session.get_credentials() is None:
            session = boto3.Session(aws_access_key_id=os.environ[aws_access_key],
                                    aws_secret_access_key=os.environ[aws_secret_key])
            
        return session.client('batch')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

aws_access_key = 'AWS_ACCESS_KEY_ID'
aws_secret_key = 'AWS_SECRET_ACCESS_KEY'
dynamo_table = 'DYNAMODB_TABLE'
job_definition = 'JOB_DEFINITION'
job_queue = 'JOB_QUEUE'
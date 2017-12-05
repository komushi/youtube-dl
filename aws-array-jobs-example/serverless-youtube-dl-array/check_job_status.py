from __future__ import unicode_literals

import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(here, './vendored'))
import boto3
from boto3.dynamodb.conditions import Key, Attr


def check(job_id):

    print("job_id: " + job_id)

    dynamo_client = get_dynamo_client()
    batch_client = get_batch_client()

    res = dynamo_client.query(
        TableName=os.environ[dynamo_table],
        ProjectionExpression='batch_job_id, video_index',
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

    active_job_list = list(map(lambda x: x['batch_job_id']['S'] + ':' + str(x['video_index']['N']), res[u'Items']))

    incomplete_jobs = len(active_job_list)

    if incomplete_jobs == 0:
        print("incomplete_jobs: " + str(incomplete_jobs))
        return incomplete_jobs
    else:
        response = batch_client.describe_jobs(jobs=active_job_list)
        # print("Received Dynamo Item: " + json.dumps(response, indent=2))

        for i in response[u'jobs']:
            print("Received Job: " + json.dumps(i, indent=2))

            batch_job_status = i['status']
            video_index = i['jobId'].split(':')[1]

            if batch_job_status == 'SUCCEEDED' or batch_job_status == 'FAILED':
                print("batch_job_status: " + batch_job_status)
                incomplete_jobs -= 1

            dynamo_client.update_item(
                TableName=os.environ[dynamo_table],
                Key={
                    'job_id': {
                        'S': job_id
                    },
                    'video_index': {
                        'N': video_index
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

    print("incomplete_jobs: " + str(incomplete_jobs))
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

# os.environ[job_queue] = 'job-que-youtube-dl'
# os.environ[job_definition] = 'job-def-youtube-dl'

# check('68362bab-deb7-4458-8649-c52686439de8')



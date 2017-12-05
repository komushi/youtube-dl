from __future__ import unicode_literals

import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(here, "./vendored"))
import boto3
from boto3.dynamodb.conditions import Key, Attr

class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def submit(args):


    print("my11 boto3.__version__", boto3.__version__)

    print("args: " + json.dumps(args, indent=2))    
    
    job_id = args['job_id']
    size = args['size']

    dynamo_client = get_dynamo_client()
    batch_client = get_batch_client()

    response = batch_client.submit_job(
        jobName=job_id,
        jobQueue=os.environ[job_queue],
        jobDefinition=os.environ[job_definition],
        parameters={
            'job_id': job_id
            # 'url': 'https://www.youtube.com/watch?v=obVmsE6Qgvs'
        },
        arrayProperties={
            'size': size
        }
    )

    # print("response", json.dumps(response, indent=2))
    batch_job_id = response['jobId']
    batch_job_status = 'SUBMITTED'

    for video_index in range(size):

        dynamo_client.update_item(
            TableName=os.environ[dynamo_table],
            Key={
                'job_id': {
                    'S': job_id
                },
                 'video_index': {
                    'N': str(video_index)
                }
            },
            UpdateExpression='SET #BAT = :bat, #BSTS = :bsts',
            ExpressionAttributeNames={
                '#BAT': 'batch_job_id',
                '#BSTS': 'batch_job_status'
            },
            ExpressionAttributeValues={
                ':bat': {
                    'S': batch_job_id
                },
                ':bsts': {
                    'S': batch_job_status
                }
            }
        )


    return job_id

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

# submit({'job_id': 'asd', 'size': 2})



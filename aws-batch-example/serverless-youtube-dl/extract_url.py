from __future__ import unicode_literals

import boto3
import os
import sys
import uuid

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vendored'))

from youtube_dl import YoutubeDL

class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def processing_hook(d):
    print(d)
    if d['status'] == 'finished':
        print(d)
        print('Done downloading, now converting & uploading ...')
        # print(upload(d))
        
def extract(url):

    ydl_opts = {
        'logger': Logger(),
        'progress_hooks': [processing_hook],
    }


    ydl = YoutubeDL(ydl_opts)
    info = ydl.extract_info(url, download=False)

    client = get_dynamo_client()
    job_id = str(uuid.uuid4())


    playlist_id = info['id']
    playlist_title = info['title']


    for entry in info['entries']:
        video_title = entry['title']
        video_id = entry['id']
        video_url = entry['webpage_url']
        client.put_item(
            TableName='youtube_jobs',
            Item={
                'job_id': {'S': job_id},
                'video_id': {'S': video_id},
                'video_title': {'S': video_title},
                'video_url': {'S': video_url},
                'playlist_id': {'S': playlist_id},
                'playlist_title': {'S': playlist_title},
                'job_status': {'S': 'NEW'}
            }
        )

    return job_id



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

aws_access_key = 'AWS_ACCESS_KEY_ID'
aws_secret_key = 'AWS_SECRET_ACCESS_KEY'

# print(sys.argv)
# run(sys.argv[1])
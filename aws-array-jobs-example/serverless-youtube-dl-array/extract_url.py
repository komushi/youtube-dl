from __future__ import unicode_literals


import os
import sys
import uuid

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(here, "./vendored"))
import boto3
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

    print("my11 boto3.__version__", boto3.__version__)

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

    print('job_id:', job_id)
    # print('info:', info)
    print('playlist count:', len(info['entries']))

    for entry in info['entries']:
        video_title = entry['title']
        video_id = entry['id']
        video_url = entry['webpage_url']
        video_index = int(entry['playlist_index']) - 1
        print('video_title:', video_title)
        print('video_id:', video_id)
        print('video_index:', video_index)
        
        client.put_item(
            TableName='youtube_array_jobs',
            Item={
                'job_id': {'S': job_id},
                'video_index': {'N': str(video_index)},
                'video_id': {'S': video_id},
                'video_title': {'S': video_title},
                'video_url': {'S': video_url},
                'playlist_id': {'S': playlist_id},
                'playlist_title': {'S': playlist_title}
            }
        )

    return {'job_id': job_id, 'size': len(info['entries'])}

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

aws_access_key_id = 'AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'AWS_SECRET_ACCESS_KEY'


# extract(sys.argv[1])
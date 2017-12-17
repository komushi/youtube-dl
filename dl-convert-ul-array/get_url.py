from __future__ import unicode_literals
import boto3
import json
import os
import sys
import youtube_dl_array

def get_url(job_id):

	video_index = os.environ[aws_batch_job_array_index]

	dynamo_client = get_dynamo_client()
		
	res = dynamo_client.query(
		TableName=os.environ[dynamo_table],
		ProjectionExpression='video_id, video_url, video_title',
		KeyConditionExpression='job_id = :job_id and video_index = :video_index',
		ExpressionAttributeValues={
			':job_id': {'S': job_id},
			':video_index': {'N': str(video_index)}
		}
	)

	for i in res[u'Items']:
		print("Received Items: " + json.dumps(i, indent=2))

		video_url = i['video_url']['S']
		print("video_url: " + video_url)
		youtube_dl_array.run(video_url, job_id)


def get_dynamo_client():
	try:

		session = boto3.Session(region_name=os.environ[region_name])
		
		if session.get_credentials() is None:
			session = boto3.Session(aws_access_key_id=os.environ[aws_access_key_id],
															aws_secret_access_key=os.environ[aws_secret_access_key],
															region_name=os.environ[region_name])
				
		return session.client('dynamodb', region_name=os.environ[region_name])
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise

aws_batch_job_array_index = 'AWS_BATCH_JOB_ARRAY_INDEX'
dynamo_table = 'DYNAMODB_TABLE'
region_name = 'REGION_NAME'
aws_access_key_id = 'AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'AWS_SECRET_ACCESS_KEY'


print(sys.argv)
get_url(sys.argv[1])
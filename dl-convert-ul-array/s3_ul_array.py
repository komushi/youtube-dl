from __future__ import unicode_literals
import boto3
import os
import sys

def upload(filename, job_id):

	client = get_s3_client()
	filepath = "./{0}".format(filename)
	
	if bucket_key in os.environ:
		bucket = os.environ[bucket_key]
	else:
		bucket = client.list_buckets()['Buckets'][0]['Name']

	client.upload_file(filepath, bucket, filename)
	client.put_object_acl(ACL='public-read', Bucket=bucket, Key=filename)

	region = client.get_bucket_location(Bucket=bucket)['LocationConstraint']

	url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(region, bucket, filename)
	print(url)

	return url

def get_s3_client():
	try:
		session = boto3.Session()
		
		if session.get_credentials() is None:
			session = boto3.Session(aws_access_key_id=os.environ[aws_access_key_id],
                  					aws_secret_access_key=os.environ[aws_secret_access_key])
			
		return session.client('s3')
	except:
	    print("Unexpected error:", sys.exc_info()[0])
	    raise

print(os.environ)
bucket_key = 'YOUTUBE_DESTINATION_BUCKET'
aws_access_key_id = 'AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'AWS_SECRET_ACCESS_KEY'

print(sys.argv)
upload(sys.argv[1], sys.argv[2])

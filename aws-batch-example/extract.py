from __future__ import unicode_literals
from youtube_dl import YoutubeDL
import boto3
import os
import sys

class Logger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		print(msg)

	def error(self, msg):
		print(msg)


# def upload(d):

# 	client = get_s3_client()
# 	filename = d['filename']
# 	filepath = "./{0}".format(filename)

# 	if bucket_key in os.environ:
# 		bucket = os.environ[bucket_key]
# 	else:
# 		bucket = client.list_buckets()['Buckets'][0]['Name']

# 	print(bucket)

# 	client.upload_file(filepath, bucket, filename)
# 	client.put_object_acl(ACL='public-read', Bucket=bucket, Key=filename)

# 	region = client.get_bucket_location(Bucket=bucket)['LocationConstraint']

# 	return "https://s3-{0}.amazonaws.com/{1}/{2}".format(region, bucket, filename)

def processing_hook(d):
	print(d)
	if d['status'] == 'finished':
		print(d)
		print('Done downloading, now converting & uploading ...')
		# print(upload(d))
		
def run(url):

	ydl_opts = {
		'logger': Logger(),
		'progress_hooks': [processing_hook],
	}


	ydl = YoutubeDL(ydl_opts)
	info = ydl.extract_info(url, download=False)

	print(info)


	for entry in info['entries']:
		print (entry['playlist_title'])
		print (entry['title'])
		print (entry['webpage_url'])
		# dynamodb.put_item(TableName='youtube-dl-jobs', Item={'fruitName':{'S':'Banana'},'key2':{'N':'value2'})

	# print(info['entries'][0]['title'])
	# print(info['entries'][0]['webpage_url'])
	# print(info['entries'][1]['title'])
	# print(info['entries'][1]['webpage_url'])



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

print(sys.argv)
run(sys.argv[1])
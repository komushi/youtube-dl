from __future__ import unicode_literals
from youtube_dl import YoutubeDL
from botocore.exceptions import ProfileNotFound
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


def upload(d):

	# session = boto3.Session(profile_name='default')	
	# client = boto3.client('s3')
	# bucket = 'your-bucket-name'


	filename = d['filename']
	filepath = "./{0}".format(filename)
	# print(filepath)

	client.upload_file(filepath, bucket, filename)
	client.put_object_acl(ACL='public-read', Bucket=bucket, Key=filename)
	region = "ap-northeast-1"
	return "https://s3-{0}.amazonaws.com/{1}/{2}".format(region, bucket, filename)

def processing_hook(d):
	if d['status'] == 'finished':
		print(d)
		print('Done downloading, now converting & uploading ...')
		print(upload(d))
		

# def run(url, key, secret):
def run(url):
	ydl_opts = {
		'outtmpl': '%(title)s-%(id)s.%(ext)s',
		'format': 'best[height=360]',
		'postprocessors': [{
			'key': 'FFmpegVideoConvertor',
			'preferedformat': 'mp4',
		}],
		'logger': Logger(),
		'progress_hooks': [processing_hook],
		# 'ffmpeg_location': 'ffmpeg/',
	}

	# ydl_opts2 = {
	# 	'logger': Logger(),
	# 	'progress_hooks': [processing_hook],
	# }


	# ydl = YoutubeDL(ydl_opts2)
	# info = ydl.extract_info(url, download=False)
	# print(info['entries'][0]['title'])
	# print(info['entries'][1]['title'])

	ydl = YoutubeDL(ydl_opts)
	info = ydl.extract_info(url, True)




def get_s3_client(sysArgv):
	try:
		session = boto3.Session()
		if session.get_credentials() is not None:
			client = session.client('s3')
		elif (len(sysArgv) == 4 and sysArgv[2] is not None and sysArgv[3] is not None):
			session = boto3.Session(aws_access_key_id=sysArgv[2],
                  					aws_secret_access_key=sysArgv[3])
			client = session.client('s3')

		return session.client('s3')
		# session = boto3.Session(profile_name='default')	
	# except ProfileNotFound as e:
	# 	session = Session(aws_access_key_id=sysArgv[2],
	# 	                  aws_secret_access_key=sysArgv[3])
	except:
	    print("Unexpected error:", sys.exc_info()[0])
	    raise

    


# client = boto3.client('s3')
# bucket = 's3exp'
# run(sys.argv[1], sys.argv[2], sys.argv[3])

print(sys.argv)
client = get_s3_client(sys.argv)
bucket = 's3exp'
run(sys.argv[1])

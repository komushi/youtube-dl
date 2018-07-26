from __future__ import unicode_literals
from youtube_dl import YoutubeDL
import os
import sys

class Logger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		print(msg)

	def error(self, msg):
		print(msg)


def run(url, job_id):
	
	if height_key in os.environ:
		exec_cmd = 'mv {} tmp_mp4; ffmpeg -f mp4 -i tmp_mp4 -vf scale=800:' + os.environ[height_key] + ' {}; rm tmp_mp4; python s3_ul_array.py {} ' + job_id
	else:
		exec_cmd = 'python s3_ul_array.py {} ' + job_id

	ydl_opts = {
		'outtmpl': '%(title)s-%(id)s.%(ext)s',
		'format': 'best',
		'postprocessors': [{
			'key': 'ExecAfterDownload',
			'exec_cmd': exec_cmd,
		}],
		'logger': Logger(),
	}

	ydl = YoutubeDL(ydl_opts)
	info = ydl.extract_info(url, True)

height_key = 'YOUTUBE_MAX_HEIGHT'


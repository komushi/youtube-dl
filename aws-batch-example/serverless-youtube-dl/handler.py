from __future__ import print_function

import sys
import json
import os
import extract_url
import submit_batch_jobs
import check_job_status

def extract(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    url = event['url']
    try:
        return {'job_id': extract_url.extract(url)}
    except Exception as e:
        print(e)
        raise e

def submit(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    job_id = event['job_id']
    try:
        return {'job_id': submit_batch_jobs.submit(job_id)}
    except Exception as e:
        print(e)
        raise e

def check(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    job_id = event['job_id']
    try:
        return {
            'incomplete_jobs': check_job_status.check(job_id),
            'job_id': job_id
            }
    except Exception as e:
        print(e)
        raise e


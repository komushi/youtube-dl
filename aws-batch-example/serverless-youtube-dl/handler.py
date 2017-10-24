from __future__ import print_function

import sys
import json
import os
import extract_url

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    url = event['url']
    try:
        
        # return os.system("python extract_url.py {0}".format(url))

        return extract_url.extract(url)
    except Exception as e:
        print(e)
        raise e



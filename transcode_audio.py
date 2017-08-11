import json
import logging
import boto3

logger = logging.getLogger('boto3')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3_event = parse_event(event)
    logger.info(json.dumps(s3_event))

    # ffmpeg copy audio only: ffmpeg -i input.mp4 -c:v copy -c:a libfdk_aac -vbr 3 output.mp4
    # see: https://trac.ffmpeg.org/wiki/Encode/AAC

    return 'done'

def parse_event(event):
    record = event['Records'][0]
    if 'EventSource' in record and record['EventSource'] == 'aws:sns':
        return json.loads(record['Sns']['Message'])

    return event

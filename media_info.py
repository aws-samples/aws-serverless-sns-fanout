import json
import logging
import boto3

logger = logging.getLogger('boto3')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3_event = parse_event(event)
    logger.info(json.dumps(s3_event))

    # MediaInfo Processing
    # see: https://aws.amazon.com/blogs/compute/extracting-video-metadata-using-lambda-and-mediainfo/

    return 'done'

def parse_event(event):
    record = event['Records'][0]
    if 'EventSource' in record and record['EventSource'] == 'aws:sns':
        return json.loads(record['Sns']['Message'])

    return event

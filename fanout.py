import json
import logging
import boto3

logger = logging.getLogger('boto3')
logger.setLevel(logging.INFO)

client = boto3.client('lambda')
fanout_functions = ['media_info', 'transcode_audio']

def lambda_handler(event, context):
    logger.info(json.dumps(event))
    logger.info('fanout_functions: %s', fanout_functions)

    for fanout_function in fanout_functions:
        logger.info('invoke: %s', fanout_function)
        response = client.invoke(
            FunctionName=fanout_function,
            InvocationType='Event',
            Payload=json.dumps(event)
        )
        logger.info('response: %s', response)

    return 'done'

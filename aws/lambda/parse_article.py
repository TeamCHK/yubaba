import boto3
import json
import logging
import os
from newspaper import Article

logging.root.setLevel(logging.DEBUG)

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    logging.info("Received event: " + json.dumps(event, indent=2))
    data = json.loads(json.dumps(event))
    url = data["url"]
    
    logging.info(f"Downloading article from: {url}")
    article = Article(url)
    article.download()
    
    logging.info(f"Parsing article from: {url}")
    article.parse()
    logging.debug("Article title: ", article.title)
    logging.debug("Article date: ", article.publish_date)
    logging.debug("Article authors: ", article.authors)
    
    inference_payload = {
        "inputs": [article.text]
    }
    
    if not article.is_valid_body:
        return {
            "statusCode": 400,
            "body": [{
                "url": url
            }]
        }
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/json',
                                       Body=json.dumps(inference_payload))
    result = json.loads(response['Body'].read().decode())
    logging.debug(result)
    
    return {
        'statusCode': 200,
        'body': result
    }

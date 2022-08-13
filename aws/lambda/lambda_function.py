import boto3
import json
import logging
import os
from newspaper import Article

logging.root.setLevel(logging.DEBUG)

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')

def handler(event, context):
    # Extract URL from the request
    logging.info("Received event: " + json.dumps(event, indent=2))
    data = json.loads(json.dumps(event))
    url = data["url"]
    
    # Download article from the given URL
    logging.info(f"Downloading article from: {url}")
    article = Article(url)
    article.download()
    
    # Parse the article
    logging.info(f"Parsing article from: {url}")
    article.parse()
    logging.debug(f"Article title: {article.title}")
    logging.debug(f"Article date: {article.publish_date}")
    logging.debug(f"Article authors: {article.authors}")
    
    # Set up inference payload that contains article body
    inference_payload = {
        "inputs": [article.text]
    }
    
    # Send error response if the given URL does not contain a valid article
    if not article.is_valid_body():
        return {
            "statusCode": 400,
            "body": [{
                "url": url
            }]
        }
    
    # Invoke an inference endpoint
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/json',
                                       Body=json.dumps(inference_payload))
    result = json.loads(response['Body'].read().decode())
    logging.debug(result)
    
    return {
        'statusCode': 200,
        'body': result
    }

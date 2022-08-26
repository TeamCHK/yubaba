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
    # Request example: {"headers": {}, "httpMethod": "POST", "body": "{\"url\":\"https://example.com\"}"}
    logging.info("Received event: " + json.dumps(event, indent=2))
    data = json.loads(json.dumps(event))
    url = json.loads(data["body"])["url"]
    
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
    # https://github.com/codelucas/newspaper/blob/master/newspaper/article.py#L322
    if not article.is_valid_body():
        return {
            "statusCode": 202,
            'headers': {'Content-Type': 'application/json'},
            "body": json.dumps([{
                "url": url
            }])
        }
    
    # Invoke an inference endpoint
    # Response example: [{'summary_text': 'This is an example of article summary.'}]
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/json',
                                       Body=json.dumps(inference_payload))
    result = json.loads(response['Body'].read().decode())[0]
    logging.debug(f"Response dict: {result}")

    endpoint_response = {
        'articleSummary': result['summary_text'],
        'articleTitle': article.title,
        'articleAuthors': article.authors,
        'publishDate': article.publish_date.isoformat(),
    }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(endpoint_response),
    }

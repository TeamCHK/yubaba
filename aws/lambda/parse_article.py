import json
import os
import boto3
from newspaper import Article
import logging

logging.root.setLevel(logging.DEBUG)

ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    logging.INFO("Received event: " + json.dumps(event, indent=2))
    data = json.loads(json.dumps(event))
    url = data["url"]

    logging.INFO(f"Downloading article from: {url}")
    article = Article(url)
    article.download()

    logging.INFO(f"Parsing article from: {url}")
    article.parse()
    print(article.title)
    logging.DEBUG("Article title: ", article.title)
    logging.DEBUG("Article date: ", article.publish_date)
    logging.DEBUG("Article authors: ", article.authors)

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
    print(result)

    return {
        'statusCode': 200,
        'body': result
    }

# AWS Lambda

## Updating the Lambda Function
1. Configure AWS SSO
```
$ aws configure sso
SSO start URL [None]: https://d-9067b50b9c.awsapps.com/start
SSO Region [None]: us-east-1
The only AWS account available to you is: 279578104300
Using the account ID 279578104300
The only role available to you is: AdministratorAccess
Using the role name "AdministratorAccess"
CLI default client Region [None]: [Press Enter]
CLI default output format [None]: [Press Enter]
CLI profile name [AdministratorAccess-279578104300]: [Press Enter]
```

2. Authenticate the Docker CLI to the Amazon ECR registry
```
aws ecr get-login-password --region us-east-1 --profile AdministratorAccess-279578104300 | docker login --username AWS --password-stdin 279578104300.dkr.ecr.us-east-1.amazonaws.com/lambda_function
```

3. Build a docker image that contains the lambda handler along with dependencies
```
docker build -t yubaba/lambda_function .
```

3. Tag the image to match the repository name, and deploy the image to Amazon ECR using the docker push command
```
docker tag yubaba/lambda_function:latest 279578104300.dkr.ecr.us-east-1.amazonaws.com/lambda_function:latest
docker push 279578104300.dkr.ecr.us-east-1.amazonaws.com/lambda_function:latest
```

4. Update the lambda function with the newly uploaded image
```
aws lambda update-function-code --region us-east-1 --function-name summarize --image-uri 279578104300.dkr.ecr.us-east-1.amazonaws.com/lambda_function:latest --profile AdministratorAccess-279578104300
```

5. Start the notebook instance on [SageMaker notebook page](https://us-east-1.console.aws.amazon.com/sagemaker/home?region=us-east-1#/notebook-instances)

6. Make sure the new lambda function's test passes by running tests on [AWS Lambda web page](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/pass-article-to-summarization-model?tab=testing)

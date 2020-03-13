# Github Commit Tweeter
A small Python project that uses AWS API Gateway and AWS Lambda to tweet new Github commits.

To use this project, you will the following items -
- AWS Lambda Function
- An API Gateway that accepts `POST` requests at a `/github` resource endpoint & has an **Integration Type** as Lambda Function (provide the ARN to your Lambda).
- A [Twitter Application](https://developer.twitter.com/en/apps) with the proper keys & tokens.
- Environment variables defined in your AWS Lambda Function with (at least) the following values -
  - TWTR_CONSUMER_KEY
  - TWTR_CONSUMER_SECRET
  - TWTR_ACCESS_TOKEN
  - TWTR_ACCESS_SECRET


In the API Gateway, you'll need the following configuration in **Integration Request** > **Mapping Templates** > **Request Body Passthrough** for the `application/json` Content-Type.
```
{
    "method": "$context.httpMethod",
    "body" : $input.json('$'),
    "headers": {
        #foreach($param in $input.params().header.keySet())
        "$param": "$util.escapeJavaScript($input.params().header.get($param))"
        #if($foreach.hasNext),#end
        #end
    }
}
```

To deploy this project, run the following commands (if using a virtualenv). This is [fully documented](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) within the AWS documentation as well.
```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
(venv)$ deactivate
$ cd venv/lib/python3.6/site-packages
$ zip -r9 ${OLDPWD}/function.zip .
$ cd $OLDPWD
$ zip -g function.zip lambda_function.py
$ aws lambda update-function-code --function-name github-commit-twitter --zip-file fileb://function.zip

# Sample Output For the AWS Lambda Function (Some Info Redacted)
{
    "FunctionName": "github-commit-twitter",
    "FunctionArn": "arn:aws:lambda:us-east-1:024303108096:function:github-commit-twitter",
    "Runtime": "python3.7",
    "Role": "",
    "Handler": "lambda_function.lambda_handler",
    "CodeSize": 5537590,
    "Description": "",
    "Timeout": 3,
    "MemorySize": 128,
    "LastModified": "2020-03-13T03:14:05.258+0000",
    "CodeSha256": "",
    "Version": "$LATEST",
    "Environment": {
        "Variables": {
            "DEBUG_TWTR_ACCESS_SECRET": "",
            "DEBUG_TWTR_ACCESS_TOKEN": "",
            "TWTR_CONSUMER_SECRET": "",
            "TWTR_ACCESS_SECRET": "",
            "DEBUG_TWTR_CONSUMER_KEY": "",
            "DEBUG_TWTR_CONSUMER_SECRET": "",
            "TWTR_ACCESS_TOKEN": "",
            "TWTR_CONSUMER_KEY": ""
        }
    },
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "f55a1648-7f42-40f1-9b84-3676d6ee375e",
    "State": "Active",
    "LastUpdateStatus": "Successful"
}
```


## TODO
- Convert this deployment into AWS SAM so anyone can use this to tweet their commits.

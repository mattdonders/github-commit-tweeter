# Github Commit Tweeter
A small Python project that uses AWS API Gateway and AWS Lambda to tweet new Github commits.

To use this project, you will the following items - 
1. AWS Lambda Function
2. An API Gateway that accepts `POST` requests at a `/github` resource endpoint & has an **Integration Type** as Lambda Function (provide the ARN to your Lambda).
3. A [Twitter Application](https://developer.twitter.com/en/apps) with the proper keys & tokens.

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

## TODO
- Convert this deployment into AWS SAM so anyone can use this to tweet their commits.

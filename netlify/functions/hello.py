# netlify/functions/hello.py

def handler(event, context):
    print("Function triggered")  # This will appear in the logs
    return {
        "statusCode": 200,
        "body": "Hello from Netlify Serverless Function!"
    }

import os
import urllib.parse
import boto3

s3 = boto3.client("s3")
sns = boto3.client("sns")


def lambda_handler(event, context):
    # The S3 event tells us which bucket and file triggered the function.
    record = event["Records"][0]["s3"]
    bucket = record["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["object"]["key"])

    # Read the text file and count the words.
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8")
    word_count = len(body.split())

    # Email the result through the SNS topic.
    message = f"The word count in the {key} file is {word_count}."
    sns.publish(
        TopicArn=os.environ["TOPIC_ARN"],
        Subject="Word Count Result",
        Message=message,
    )
    return {"statusCode": 200, "body": message}

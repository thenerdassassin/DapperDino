import boto3

def readFileFromS3(bucket, filename):
    s3 = boto3.client('s3')
    key = filename
    return s3.get_object(Bucket=bucket, Key=key).get('Body')

def readStringFromS3(bucket, filename):
    return readFileFromS3(bucket, filename).read().decode('utf-8')
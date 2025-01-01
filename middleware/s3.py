import boto3
from settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_REGION_NAME

def get_s3_client():
    s3_client = boto3.client(
        's3',
        region_name=S3_REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    return s3_client

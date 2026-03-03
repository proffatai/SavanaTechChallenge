import boto3
import os

def upload_report_to_s3(filename: str):
    s3_endpoint = os.environ.get("S3_ENDPOINT", "http://localhost:4566")
    
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        endpoint_url=s3_endpoint
    )

    # Ensure bucket exists
    bucket_name = "analyzer-reports"
    if bucket_name not in [b['Name'] for b in s3.list_buckets()['Buckets']]:
        s3.create_bucket(Bucket=bucket_name)

    with open(filename, "rb") as file:
        s3.upload_fileobj(file, bucket_name, filename)

    print(f"Uploaded {filename} to S3 bucket {bucket_name}")
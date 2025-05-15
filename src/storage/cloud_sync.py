import boto3, os
from loguru import logger
def upload(local_path:str):
    bucket = os.getenv("S3_BUCKET")
    if not bucket:
        return
    s3 = boto3.client("s3")
    key = os.path.basename(local_path)
    s3.upload_file(local_path, bucket, key)
    logger.info(f"Uploaded {local_path} to s3://{bucket}/{key}")

"""Lectura de un objeto S3 privado; sin escrituras desde el panel."""
import os
import boto3
from botocore.config import Config


def read_s3_orders() -> bytes:
    bucket = os.environ.get("CLOUDTRACK_S3_BUCKET", "")
    key = os.environ.get("CLOUDTRACK_S3_KEY", "raw/orders.csv")
    if not bucket:
        raise ValueError("Configure CLOUDTRACK_S3_BUCKET para leer desde S3.")
    client = boto3.client("s3", config=Config(
        connect_timeout=5, read_timeout=15, retries={"max_attempts": 2}
    ))
    response = client.get_object(Bucket=bucket, Key=key)
    body = response["Body"]
    try:
        if response.get("ContentLength", 0) > 10 * 1024 * 1024:
            raise ValueError("El objeto S3 supera el límite de 10 MB.")
        content = body.read(10 * 1024 * 1024 + 1)
        if len(content) > 10 * 1024 * 1024:
            raise ValueError("El objeto S3 supera el límite de 10 MB.")
        return content
    finally:
        body.close()

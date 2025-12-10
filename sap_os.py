import os
import boto3
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()


def get_credentials(mode: str):
    """
    mode = "read" or "write"
    Loads credentials from .env only.
    """

    if mode not in ("read", "write"):
        raise ValueError("Mode must be 'read' or 'write'.")

    access_key = os.getenv(f"{mode.upper()}_ACCESS_KEY_ID")
    secret_key = os.getenv(f"{mode.upper()}_SECRET_ACCESS_KEY")

    if not access_key or not secret_key:
        raise Exception(f"Missing {mode} credentials in .env")

    creds = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
        "region_name": os.getenv("REGION", "us-east-1"),
        "bucket": os.getenv("BUCKET_NAME"),
        "endpoint_url": f"https://{os.getenv('HOST', 's3.amazonaws.com')}"
    }

    if not creds["bucket"]:
        raise Exception("BUCKET_NAME missing in .env")

    return creds


def create_client(creds: dict):
    """Create S3 client using .env credentials."""
    return boto3.client(
        "s3",
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        region_name=creds["region_name"],
        endpoint_url=creds["endpoint_url"],
    )


def upload(local_file, object_key):
    creds = get_credentials("write")
    s3 = create_client(creds)
    bucket = creds["bucket"]

    s3.upload_file(local_file, bucket, object_key)
    print(f"Uploaded {local_file} → s3://{bucket}/{object_key}")


def download(object_key, local_file):
    creds = get_credentials("read")
    s3 = create_client(creds)
    bucket = creds["bucket"]

    s3.download_file(bucket, object_key, local_file)
    print(f"Downloaded s3://{bucket}/{object_key} → {local_file}")


def list_objects(prefix=None):
    creds = get_credentials("read")
    s3 = create_client(creds)
    bucket = creds["bucket"]

    params = {"Bucket": bucket}
    if prefix:
        params["Prefix"] = prefix

    response = s3.list_objects_v2(**params)

    files = []
    for item in response.get("Contents", []):
        files.append({
            "key": item["Key"],
            "size": item["Size"]
        })

    return files  

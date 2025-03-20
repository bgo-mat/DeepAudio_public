# utils/s3_utils.py

import boto3
from botocore.client import Config
from django.conf import settings
import uuid


class S3Uploader:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name=settings.AWS_S3_REGION_NAME,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_content, file_name, content_type):
        # Générer une clé S3 unique
        s3_key = f"{uuid.uuid4()}_{file_name}"

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type,
        )

        return s3_key

    def get_file_url(self, s3_key, expiration=3600):
        # Générer une URL pré-signée valide pendant 'expiration' secondes
        url = self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": s3_key},
            ExpiresIn=expiration,
        )
        return url

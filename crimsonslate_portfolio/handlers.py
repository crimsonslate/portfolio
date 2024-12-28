from datetime import datetime, timedelta
from uuid import uuid4

from boto3.session import Session
from django.conf import settings
from django.core.files.storage.base import File
from django.core.files.storage.memory import ContentFile
from django.core.files.uploadhandler import TemporaryFileUploadHandler


class MediaUploadHandler(TemporaryFileUploadHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.boto3_session = Session().client("s3")
        self.bucket_name = settings.PORTFOLIO_BUCKET_NAME
        self.object_key = str(uuid4())
        self.upload_expiry = datetime.today() + timedelta(days=7)
        self.upload_parts = []

    def new_file(self, *args, **kwargs) -> None:
        super().new_file(*args, **kwargs)
        self.upload_start = datetime.today()
        response = self.boto3_session.create_multipart_upload(
            **{
                "Bucket": self.bucket_name,
                "Key": self.object_key,
                "Expires": self.upload_expiry,
                "ContentEncoding": "gzip",
                "ContentLanguage": "en-US",
                "ContentType": "multipart/form-data",
            }
        )
        self.upload_id = response.get("UploadId")

    def file_complete(self, file_size: int | None = None) -> File:
        file = self.boto3_session.get_object(
            **{
                "Bucket": self.bucket_name,
                "Key": self.object_key,
            }
        )
        return ContentFile(file, self.file_name)

    def receive_chunk_data(self, raw_data: str | bytes, start: int) -> None:
        part_number: int = start + 1  # AWS parts start index at 1
        response = self.boto3_session.upload_part(
            **{
                "Body": raw_data,
                "Bucket": self.bucket_name,
                "ContentEncoding": "gzip",
                "ContentLanguage": "en-US",
                "ContentType": "multipart/form-data",
                "Key": self.object_key,
                "PartNumber": part_number,
                "UploadId": self.upload_id,
            }
        )
        self.upload_parts.append(
            {
                "ETag": response.get("ETag"),
                "PartNumber": part_number,
            }
        )

    def upload_complete(self) -> None:
        self.boto3_session.complete_multipart_upload(
            **{
                "Bucket": self.bucket_name,
                "Key": self.object_key,
                "UploadId": self.upload_id,
                "MultipartUpload": {
                    "Parts": self.upload_parts,
                },
            }
        )

    def upload_interrupted(self) -> None:
        assert self.upload_id  # Can't abort if upload never started
        self.boto3_session.abort_multipart_upload(
            **{
                "Bucket": self.bucket_name,
                "Key": self.object_key,
                "UploadId": self.upload_id,
            }
        )
        super().upload_interrupted()

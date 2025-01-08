from boto3.session import Session
from django.conf import ImproperlyConfigured, settings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.uploadhandler import FileUploadHandler


class S3BucketUploadHandler(FileUploadHandler):
    chunk_size = 5 * 2**20  # 5MiB, minimum allowed

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not hasattr(settings, "S3_UPLOAD_BUCKET_NAME"):
            raise ImproperlyConfigured("S3_UPLOAD_BUCKET_NAME setting is required.")
        if hasattr(settings, "S3_UPLOAD_CHUNK_SIZE"):
            self.validate_chunk_size(settings.S3_UPLOAD_CHUNK_SIZE)
            self.chunk_size = settings.S3_UPLOAD_CHUNK_SIZE

        self.bucket_name = settings.S3_UPLOAD_BUCKET_NAME
        self.boto3_client = kwargs.get("s3_client") or Session().client("s3")
        self.object_key: str | None = None
        self.upload_id: str | None = None
        self.parts: list = []

    def upload_complete(self) -> None:
        self._s3_complete_multipart_upload(self.parts)

    def upload_interrupted(self) -> None:
        self._s3_abort_multipart_upload()

    def new_file(self, *args, **kwargs) -> None:
        super().new_file(*args, **kwargs)
        assert self.file_name, "File name was not set."
        self._s3_start_multipart_upload(self.file_name)

    def file_complete(self, file_size: int) -> UploadedFile | None:
        self.upload_complete()
        assert self.object_key, "Object key was not set."
        self.file = self._s3_get_file()
        return self.file

    def receive_data_chunk(self, raw_data: bytes, start: int) -> None:
        data_chunk: bytes = raw_data[start:]
        part_number: int = 1 if start == 1 else len(self.parts) + 1
        if data_chunk:
            self._s3_continue_multipart_upload(data_chunk, part_number)

    def validate_chunk_size(self, chunk_size: int) -> None:
        """Raises ImproperlyConfigured if the chunk size is invalid."""
        max_chunk_size: int = 5 * 2**40  # 5TiB
        min_chunk_size: int = 5 * 2**20  # 5MiB
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ImproperlyConfigured(
                "S3_UPLOAD_CHUNK_SIZE must be a positive integer."
            )
        if chunk_size > max_chunk_size:
            raise ImproperlyConfigured(
                "S3_UPLOAD_CHUNK_SIZE cannot be greater than 5TiB."
            )
        if chunk_size < min_chunk_size:
            raise ImproperlyConfigured("S3_UPLOAD_CHUNK_SIZE cannot be less than 5MiB.")

    def _s3_get_file(self) -> UploadedFile:
        """
        Uploads a part of data to the multipart upload.

        :raises ClientError: If the object wasn't retrieved.
        :raises AssertionError: If :py:attr:`object_key` wasn't set.
        :return: The uploaded file.
        :rtype: :py:obj:`~django.core.files.uploadedfiles.UploadedFile`

        """

        assert self.object_key, "Object key was not set."
        response = self.boto3_client.get_object(
            **{
                "Bucket": self.bucket_name,
                "Key": self.object_key,
            }
        )
        return UploadedFile(
            file=response.get("Body"),
            name=self.file_name,
            content_type=self.content_type,
            charset=self.charset,
            content_type_extra=self.content_type_extra,
        )

    def _s3_start_multipart_upload(self, object_key: str) -> None:
        """
        Starts a multipart upload in :py:attr:`bucket_name`.

        Sets :py:attr:`upload_id` and :py:attr:`object_key`.

        :param object_key: An S3 object key.
        :type data: :py:obj:`str`
        :raises ClientError: If the upload wasn't started.
        :return: Nothing.
        :rtype: :py:obj:`None`

        """
        response = self.boto3_client.create_multipart_upload(
            **{
                "Bucket": self.bucket_name,
                "Key": object_key,
            }
        )

        self.upload_id = response.get("UploadId")
        self.object_key = object_key

    def _s3_continue_multipart_upload(self, data: bytes, part: int) -> None:
        """
        Uploads a part of data to the multipart upload.

        :param data: The raw chunk of data to upload.
        :type data: :py:obj:`bytes`
        :param part: The part number, 1-based.
        :type part: :py:obj:`int`
        :raises ClientError: If the upload fails.
        :raises AssertionError: If :py:attr:`upload_id` or :py:attr:`object_key` wasn't set.
        :return: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.object_key, "Object key was not set"
        assert self.upload_id, "Upload id was not set"
        response = self.boto3_client.upload_part(
            **{
                "Body": data,
                "Bucket": self.bucket_name,
                "Key": self.object_key,
                "UploadId": self.upload_id,
                "PartNumber": part,
            }
        )
        self.parts.append({"ETag": response.get("ETag"), "PartNumber": part})

    def _s3_complete_multipart_upload(self, parts: list) -> None:
        """
        Completes the S3 multipart upload.

        :param parts: A list of S3 multipart upload parts.
        :type data: :py:obj:`list`
        :raises ClientError: If the upload wasn't completed.
        :raises AssertionError: If :py:attr:`upload_id` or :py:attr:`object_key` wasn't set.
        :return: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.object_key, "Object key was not set"
        assert self.upload_id, "Upload id was not set"
        self.boto3_client.complete_multipart_upload(
            **{
                "Bucket": self.bucket_name,
                "Key": self.object_key,
                "MultipartUpload": {
                    "Parts": parts,
                },
                "UploadId": self.upload_id,
            }
        )

    def _s3_abort_multipart_upload(self) -> None:
        """
        Aborts the S3 multipart upload in progress.

        :raises AssertionError: If :py:attr`upload_id` or :py:attr:`object_key` wasn't set.
        :return: Nothing.
        :rtype: :py:obj:`None`

        """

        assert self.object_key, "Object key was not set"
        assert self.upload_id, "Upload id was not set"
        self.boto3_client.abort_multipart_upload(
            **{
                "Bucket": self.bucket_name,
                "Key": self.object_key,
                "UploadId": self.upload_id,
            }
        )

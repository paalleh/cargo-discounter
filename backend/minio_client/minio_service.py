from minio import Minio

from fastapi import UploadFile

from backend.settings.minio_settings import MINIOSettings


class MINIOService:
    def __init__(self):
        self.client = Minio(
            endpoint=MINIOSettings.MINIO_URL,
            access_key=MINIOSettings.ACCESS_KEY,
            secret_key=MINIOSettings.SECRET_KEY,
            secure=False
            )

    async def add_file(self, bucket_name: str, file: UploadFile, file_name: str = None):
        found = self.client.bucket_exists(bucket_name)

        if not found:
            self.client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")

        if file_name is None:
            file_name = file.filename

        self.client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=file.file,
            length=file.size,
            content_type=file.content_type
        )

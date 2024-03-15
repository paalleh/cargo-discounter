import os


class MINIOSettings:
    ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    MINIO_URL = os.getenv("MINIO_URL")

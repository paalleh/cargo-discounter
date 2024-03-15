from fastapi import APIRouter, UploadFile
from fastapi.exceptions import HTTPException
from backend.services.driver_service import DriverService
from backend.schemas.driver import SchemaDriver
from backend.minio_client.minio_service import MINIOService
test_router = APIRouter(prefix='/test')

test_router.tags = ["test"]

minio_service = MINIOService()


@test_router.post("test")
async def test(file: UploadFile):
    print(file)
    print(file.filename)
    print(file.content_type)
    await minio_service.add_file(bucket_name="test", file=file)

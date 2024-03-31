from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from backend.services.driver_service import DriverService
from backend.schemas.driver import SchemaDriver

driver_router = APIRouter(prefix='/driver')

driver_router.tags = ["Driver"]

driver_service = DriverService()


@driver_router.post("/", response_model=SchemaDriver)
async def add_driver(new_driver: SchemaDriver):
    exception = await driver_service.add_driver(new_driver=new_driver)
    if exception is not None:
        raise HTTPException(status_code=400, detail=str(exception))

    return new_driver


@driver_router.patch("/", response_model=SchemaDriver)
async def change_driver(update_driver: SchemaDriver):
    driver = await driver_service.update_driver(driver=update_driver)

    if type(driver) is Exception:
        raise HTTPException(status_code=400, detail=str(driver))

    return driver


@driver_router.get("/{driver_id}", response_model=SchemaDriver)
async def get_driver(driver_id: int):
    driver = await driver_service.get_driver(driver_id=driver_id)

    if type(driver) is Exception:
        raise HTTPException(status_code=400, detail=str(driver))

    return driver


@driver_router.delete("/", response_model=int)
async def delete_driver(driver_id: int):
    deleted_driver_id = await driver_service.delete_driver(driver_id=driver_id)

    if type(deleted_driver_id) is Exception:
        raise HTTPException(status_code=400, detail=str(deleted_driver_id))

    return deleted_driver_id

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from backend.services.driver_service import DriverService
from backend.schemas.driver import NewDriver, UpdateDriver

driver_router = APIRouter(prefix='/driver')

driver_router.tags = ["Driver"]

driver_service = DriverService()


@driver_router.post("/", response_model=NewDriver)
async def add_driver(new_driver: NewDriver):
    exception = await driver_service.add_driver(new_driver=new_driver)
    if exception is not None:
        raise HTTPException(status_code=400, detail=str(exception))

    return new_driver


@driver_router.patch("/", response_model=NewDriver)
async def change_driver(update_driver: UpdateDriver):
    driver = await driver_service.update_driver(driver=update_driver)

    if type(driver) is Exception:
        raise HTTPException(status_code=400, detail=str(driver))

    return driver

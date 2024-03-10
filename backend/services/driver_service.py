from backend.crud.driver_crud import DriverCRUD
from backend.schemas.driver import NewDriver, UpdateDriver


class DriverService:
    def __init__(self):
        self.driver_crud = DriverCRUD()

    async def add_driver(self, new_driver: NewDriver) -> Exception | None:
        exception = await self.driver_crud.add_driver(new_driver=new_driver)
        return exception

    async def update_driver(self, driver: UpdateDriver) -> Exception | UpdateDriver:
        updated_driver = await self.driver_crud.update_driver(driver)

        if type(updated_driver) is Exception:
            return updated_driver

        phone = ""
        location = ""
        driver_license = b''

        if updated_driver.phone is not None:
            phone = updated_driver.phone
        if updated_driver.location is not None:
            phone = updated_driver.location
        if updated_driver.driver_license is not None:
            phone = updated_driver.driver_license

        driver = UpdateDriver(
            id=updated_driver.id,
            first_name=updated_driver.first_name,
            last_name=updated_driver.last_name,
            phone=phone,
            location=location,
            driver_license=driver_license,
            is_blocked=updated_driver.is_blocked
        )

        return driver

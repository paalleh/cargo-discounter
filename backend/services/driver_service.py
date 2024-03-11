from typing import Type

from backend.crud.driver_crud import DriverCRUD
from backend.schemas.driver import SchemaDriver
from backend.models.models import Driver


class DriverService:
    def __init__(self):
        self.driver_crud = DriverCRUD()

    async def _driver_db_model_to_schema_model(self, driver: Type[Driver]):
        current_driver = SchemaDriver(
            id=driver.id,
            first_name=driver.first_name,
            last_name=driver.last_name,
            phone=driver.phone,
            location=driver.location,
            driver_license=driver.driver_license,
            is_blocked=driver.is_blocked
        )

        return current_driver

    async def add_driver(self, new_driver: SchemaDriver) -> Exception | None:
        exception = await self.driver_crud.add_driver(new_driver=new_driver)
        return exception

    async def update_driver(self, driver: SchemaDriver) -> Exception | SchemaDriver:
        updated_driver = await self.driver_crud.update_driver(driver)

        if type(updated_driver) is Exception:
            return updated_driver

        driver = await self._driver_db_model_to_schema_model(driver=updated_driver)

        return driver

    async def get_driver(self, driver_id: int) -> Exception | SchemaDriver:
        driver = await self.driver_crud.get_driver(driver_id=driver_id)

        if driver is None:
            return Exception("Driver is not exists")

        current_driver = await self._driver_db_model_to_schema_model(driver=driver)

        return current_driver

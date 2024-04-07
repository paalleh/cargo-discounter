from typing import Type

from fastapi_sqlalchemy import db

from backend.crud.db_operations import DBOperations
from backend.models.models import Driver
from backend.schemas.driver import SchemaDriver


class DriverCRUD(DBOperations):
    async def get_driver(self, driver_id: int) -> Type[Driver] | None:
        driver = db.session.query(Driver).filter(Driver.id == driver_id).first()
        return driver

    async def add_driver(self, new_driver: SchemaDriver) -> Exception:
        driver_exist = await self.get_driver(driver_id=new_driver.id)

        if driver_exist is not None:
            return Exception("Driver already exist")

        driver = Driver(
            id=new_driver.id,
            first_name=new_driver.first_name,
            last_name=new_driver.last_name,
            phone=new_driver.phone,
            location=new_driver.location,
            driver_license=new_driver.driver_license,
            is_blocked=new_driver.is_blocked
            if new_driver.is_blocked is not None else False
        )
        await self.db_write(driver)

    async def update_driver(self, driver: SchemaDriver) -> Exception | Type[Driver]:
        driver_exist = await self.get_driver(driver_id=driver.id)

        if driver_exist is None:
            return Exception("Driver is not exists")

        for key, value in driver.dict().items():
            if value is not None:
                setattr(driver_exist, key, value)

        await self.db_update()

        return driver_exist

    async def delete_driver(self, driver_id: int) -> Exception | int:
        driver = await self.get_driver(driver_id=driver_id)

        if driver is None:
            return Exception("Driver is not exists")

        await self.db_delete(driver)

        return driver_id

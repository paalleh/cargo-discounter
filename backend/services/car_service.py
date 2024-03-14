from typing import Type

from backend.crud.car_crud import CarCRUD
from backend.models.models import Car
from backend.schemas.car import SchemaCar


class CarService:
    def __init__(self):
        self.car_crud = CarCRUD()

    async def _car_db_model_to_schema_model(self, car: Type[Car]):
        current_driver = SchemaCar(
            driver_id=car.driver_id,
            car_id=car.id,
            car_number=car.car_number,
            vendor=car.vendor,
            model=car.model,
            load_capacity=car.load_capacity,
            volume=car.volume
        )

        return current_driver

    async def add_car(self, new_car: SchemaCar) -> Exception | SchemaCar:
        car = await self.car_crud.add_car(new_car=new_car)

        if type(car) is Exception:
            return car

        new_car.car_id = car.id
        return new_car

    async def get_car_list(self, driver_id: int) -> list[SchemaCar]:
        car_list = await self.car_crud.get_car_list(driver_id=driver_id)

        schema_car_list = []

        for car in car_list:
            schema_car_list.append(await self._car_db_model_to_schema_model(car))

        return schema_car_list

    async def update_car(self, car: SchemaCar) -> Exception | SchemaCar:
        updated_car = await self.car_crud.update_car(car=car)

        if type(updated_car) is Exception:
            return updated_car

        schema_updated_car = await self._car_db_model_to_schema_model(car=updated_car)

        return schema_updated_car

    async def delete_car(self, car_id: int):
        return await self.car_crud.delete_car(car_id=car_id)

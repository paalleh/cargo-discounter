from typing import Type

from fastapi_sqlalchemy import db

from backend.crud.db_operations import DBOperations
from backend.models.models import Car
from backend.schemas.car import SchemaCar


class CarCRUD(DBOperations):
    async def get_car_by_id(self, car_id: int) -> Type[Car] | None:
        car = db.session.query(Car).filter(Car.id == car_id).first()

        return car

    async def get_car_by_car_number(self, car_number: str) -> Type[Car] | None:
        car = db.session.query(Car).filter(Car.car_number == car_number).first()

        return car

    async def add_car(self, new_car: SchemaCar) -> Type[Car] | Exception:
        car = await self.get_car_by_car_number(car_number=new_car.car_number)

        if car is not None:
            return Exception("Car with this number exists")

        car = Car(
            car_number=new_car.car_number,
            vendor=new_car.vendor,
            model=new_car.model,
            load_capacity=new_car.load_capacity,
            volume=new_car.volume,
            driver_id=new_car.driver_id
        )

        await self.db_write(car)

        return car

    async def get_car_list(self, driver_id: int) -> list[Type[Car]]:
        car_list = db.session.query(Car).filter(Car.driver_id == driver_id).all()

        return car_list

    async def update_car(self, car: SchemaCar) -> Exception | Type[Car]:
        car_for_updating = await self.get_car_by_id(car_id=car.car_id)

        if car_for_updating is None:
            return Exception("Car doesn't exists")

        for key, value in car.dict().items():
            if value is not None:
                setattr(car_for_updating, key, value)

        await self.db_update()

        return car_for_updating

    async def delete_car(self, car_id: int):
        car = await self.get_car_by_id(car_id=car_id)

        if car is None:
            return Exception("Car doesn't exists")

        await self.db_delete(car)

        return car_id

from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from backend.services.car_service import CarService
from backend.schemas.car import SchemaCar

car_router = APIRouter(prefix='/car')

car_router.tags = ["Car"]

car_service = CarService()


@car_router.post("/", response_model=SchemaCar)
async def add_car(new_car: SchemaCar):
    car = await car_service.add_car(new_car=new_car)
    if type(car) is Exception:
        raise HTTPException(status_code=400, detail=str(car))

    return new_car


@car_router.get("/{driver_id}", response_model=List[SchemaCar])
async def get_driver_car(driver_id: int):
    cars = await car_service.get_car_list(driver_id=driver_id)

    return cars


@car_router.patch("/", response_model=SchemaCar)
async def update_car(car: SchemaCar):
    updated_car = await car_service.update_car(car=car)

    if type(updated_car) is Exception:
        raise HTTPException(status_code=400, detail=str(updated_car))

    return updated_car


@car_router.delete("/", response_model=int)
async def delete_car(car_id: int):
    deleted_car_id = await car_service.delete_car(car_id=car_id)

    if type(deleted_car_id) is Exception:
        raise HTTPException(status_code=400, detail=str(deleted_car_id))
    
    return deleted_car_id

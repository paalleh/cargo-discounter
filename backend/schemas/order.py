from pydantic import BaseModel
from datetime import date


class SchemaOrder(BaseModel):
    id: int | None = None
    price: float | None = None
    date_creation: date | None = None
    date_ending: date | None = None
    start_location: str | None = None
    finish_location: str | None = None
    driver_id: int | None = None
    customer_id: int | None = None
    car_id: int | None = None
    volume: float | None = None
    weight: float | None = None
    status: int | None = None
    customer_estimation_id: int | None = None
    driver_estimation_id: int | None = None

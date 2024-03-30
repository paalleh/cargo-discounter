from pydantic import BaseModel
from datetime import date


class SchemaOrder(BaseModel):
    id: int | None = None
    price: float | None = None
    date_creation: date | None = None
    date_ending: date | None = None
    start_location: str
    finish_location: str
    driver_id: int | None = None
    customer_id: int
    car_id: int | None = None
    volume: float
    weight: float
    status: int | None = None
    customer_estimation_id: int | None = None
    driver_estimation_id: int | None = None

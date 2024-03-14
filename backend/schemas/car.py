from pydantic import BaseModel


class SchemaCar(BaseModel):
    driver_id: int | None = None
    car_id: int | None = None
    car_number: str | None = None
    vendor: str | None = None
    model: str | None = None
    load_capacity: float | None = None
    volume: float | None = None

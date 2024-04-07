from pydantic import BaseModel


class SchemaOffer(BaseModel):
    id: int | None = None
    order_id: int | None = None
    driver_id: int | None = None
    price: float | None = None

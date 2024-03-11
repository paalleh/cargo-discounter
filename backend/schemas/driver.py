from pydantic import BaseModel


class SchemaDriver(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    location: str | None = None
    driver_license: bytes | None = None
    is_blocked: bool = None

from pydantic import BaseModel


class SchemaBaseDriver(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    location: str | None = None
    is_blocked: bool = None


class SchemaDriver(SchemaBaseDriver):
    driver_license: str | None = None


async def schemaBaseDriver_to_SchemaDriver(driver: SchemaBaseDriver) -> SchemaDriver:
    return SchemaDriver(**vars(driver))

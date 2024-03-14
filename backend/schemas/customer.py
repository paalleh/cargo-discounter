from pydantic import BaseModel


class SchemaCustomer(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    is_blocked: bool | None = None

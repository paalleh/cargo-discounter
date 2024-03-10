from pydantic import BaseModel


class NewDriver(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str = None
    location: str = None
    driver_license: bytes = None
    is_blocked: bool = False


class UpdateDriver(BaseModel):
    id: int
    first_name: str = None
    last_name: str = None
    phone: str = None
    location: str = None
    driver_license: bytes = None
    is_blocked: bool = None

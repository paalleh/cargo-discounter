from sqlalchemy import Column, String, Integer, Boolean
from backend.models.base import Base


class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    driver_license = Column(String, nullable=True)
    is_blocked = Column(Boolean, default=False)

from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    driver_license = Column(String, nullable=True)
    is_blocked = Column(Boolean, default=False)


class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True)
    car_number = Column(String, nullable=True)
    vendor = Column(String, nullable=True)
    model = Column(String, nullable=True)
    load_capacity = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    driver_id = Column(Integer, ForeignKey('driver.id', ondelete='CASCADE'), nullable=False)

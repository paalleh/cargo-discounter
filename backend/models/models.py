from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from backend.models.order_status import OrderStatus

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


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_blocked = Column(Boolean, default=False)


class DriverEstimation(Base):
    __tablename__ = "driver_estimation"

    id = Column(Integer, primary_key=True)
    estimation = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)


class CustomerEstimation(Base):
    __tablename__ = "customer_estimation"

    id = Column(Integer, primary_key=True)
    estimation = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=True)
    date_creation = Column(Date, default=datetime.now().date())
    date_ending = Column(Date, nullable=True)
    start_location = Column(String, nullable=True)
    finish_location = Column(String, nullable=True)
    driver_id = Column(Integer, ForeignKey('driver.id', ondelete='CASCADE'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), nullable=True)
    car_id = Column(Integer, ForeignKey('car.id', ondelete='CASCADE'), nullable=True)
    volume = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    status = Column(Enum(OrderStatus))
    customer_estimation_id = Column(Integer, ForeignKey('customer_estimation.id', ondelete='CASCADE'), nullable=True)
    driver_estimation_id = Column(Integer, ForeignKey('driver_estimation.id', ondelete='CASCADE'), nullable=True)


class Offers(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id', ondelete='CASCADE'))
    driver_id = Column(Integer, ForeignKey('driver.id', ondelete='CASCADE'))
    price = Column(Integer, nullable=True)

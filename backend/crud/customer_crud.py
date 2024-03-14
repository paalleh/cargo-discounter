from typing import Type

from fastapi_sqlalchemy import db

from backend.crud.db_operations import DBOperations
from backend.models.models import Customer
from backend.schemas.customer import SchemaCustomer


class CustomerCRUD(DBOperations):
    async def get_customer(self, customer_id: int) -> Type[Customer] | None:
        customer = db.session.query(Customer).filter(Customer.id == customer_id).first()
        return customer

    async def add_customer(self, new_customer: SchemaCustomer) -> Exception | None:
        customer = await self.get_customer(customer_id=new_customer.id)

        if customer is not None:
            return Exception("Customer already exist")

        customer = Customer(
            id=new_customer.id,
            first_name=new_customer.first_name,
            last_name=new_customer.last_name,
            phone=new_customer.phone,
            is_blocked=new_customer.is_blocked
            if new_customer.is_blocked is not None else False
        )
        await self.db_write(customer)

    async def update_customer(self, customer: SchemaCustomer) -> Exception | Type[Customer]:
        customer_for_updating = await self.get_customer(customer_id=customer.id)

        if customer is None:
            return Exception("Customer does not exist")

        for key, value in customer.dict().items():
            if value is not None:
                setattr(customer_for_updating, key, value)

        await self.db_update()

        return customer_for_updating

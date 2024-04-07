from typing import Type

from backend.crud.customer_crud import CustomerCRUD
from backend.schemas.customer import SchemaCustomer
from backend.models.models import Customer


class CustomerService:
    def __init__(self):
        self.customer_crud = CustomerCRUD()

    async def _customer_db_model_to_schema_model(self, customer: Type[Customer]):
        current_customer = SchemaCustomer(
            id=customer.id,
            first_name=customer.first_name,
            last_name=customer.last_name,
            phone=customer.phone,
            is_blocked=customer.is_blocked
        )

        return current_customer

    async def add_customer(self, new_customer: SchemaCustomer) -> Exception | None:
        customer = await self.customer_crud.add_customer(new_customer=new_customer)

        return customer

    async def get_customer(self, customer_id: int) -> SchemaCustomer | Exception:
        customer = await self.customer_crud.get_customer(customer_id=customer_id)

        if customer is None:
            return Exception("Customer doesn't exists")

        customer_schema = await self._customer_db_model_to_schema_model(customer)

        return customer_schema

    async def update_customer(self, customer: SchemaCustomer) -> SchemaCustomer | Exception:
        updated_customer = await self.customer_crud.update_customer(customer=customer)

        if type(updated_customer) is Exception:
            return updated_customer

        updated_customer = await self._customer_db_model_to_schema_model(customer=updated_customer)
        return updated_customer

    async def delete_customer(self, customer_id: int) -> Exception | int:
        return await self.customer_crud.delete_customer(customer_id)

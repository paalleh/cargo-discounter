from typing import Type

from fastapi_sqlalchemy import db

from backend.crud.db_operations import DBOperations
from backend.models.order_status import OrderStatus
from backend.schemas.order import SchemaOrder
from backend.models.models import Order


class OrderCRUD(DBOperations):
    async def create_order(self, new_order: SchemaOrder) -> Order:

        order = Order(
            price=new_order.price,
            start_location=new_order.start_location,
            finish_location=new_order.finish_location,
            customer_id=new_order.customer_id,
            volume=new_order.volume,
            weight=new_order.weight,
            status=OrderStatus.new
        )

        await self.db_write(order)

        return order

    async def get_order_by_id(self, order_id: int) -> Type[Order] | None:
        order = db.session.query(Order).filter(Order.id == order_id).first()
        return order

    async def update_order(self, patch_data: SchemaOrder) -> Type[Order] | None:
        order = await self.get_order_by_id(order_id=patch_data.id)

        if order is None:
            return order

        for key, value in patch_data.dict().items():
            if value is not None:
                setattr(order, key, value)

        await self.db_update()

        return order

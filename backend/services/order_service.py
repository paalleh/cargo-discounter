from typing import Type

from backend.crud.order_crud import OrderCRUD
from backend.schemas.order import SchemaOrder
from backend.models.models import Order


class OrderService:
    def __init__(self):
        self.order_crud = OrderCRUD()

    async def _order_model_to_order_schema(self, order: Type[Order]) -> SchemaOrder:
        order_schema = SchemaOrder(
            id=order.id,
            price=order.price,
            date_creation=order.date_creation,
            date_ending=order.date_ending,
            start_location=order.start_location,
            finish_location=order.finish_location,
            driver_id=order.driver_id,
            customer_id=order.customer_id,
            car_id=order.car_id,
            volume=order.volume,
            weight=order.weight,
            status=order.status,
            customer_estimation_id=order.customer_estimation_id,
            driver_estimation_id=order.driver_estimation_id
        )

        return order_schema

    async def create_order(self, new_order: SchemaOrder) -> SchemaOrder:
        order = await self.order_crud.create_order(new_order=new_order)

        new_order.id = order.id
        new_order.status = order.status.name
        return new_order

    async def get_order_by_id(self, order_id: int) -> SchemaOrder | Exception:
        order = await self.order_crud.get_order_by_id(order_id=order_id)

        if order is None:
            return Exception('Order is not exists')

        order_schema = await self._order_model_to_order_schema(order=order)
        return order_schema

    async def update_order(self, patch_data: SchemaOrder) -> SchemaOrder | Exception:
        order = await self.order_crud.update_order(patch_data=patch_data)

        if order is None:
            return Exception('Order is not exists')

        updated_order = await self._order_model_to_order_schema(order=order)
        return updated_order

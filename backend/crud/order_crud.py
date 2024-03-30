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

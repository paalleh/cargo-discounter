from backend.crud.order_crud import OrderCRUD
from backend.schemas.order import SchemaOrder


class OrderService:
    def __init__(self):
        self.order_crud = OrderCRUD()

    async def create_order(self, new_order: SchemaOrder) -> SchemaOrder:
        order = await self.order_crud.create_order(new_order=new_order)

        new_order.id = order.id
        new_order.status = order.status.name
        return new_order

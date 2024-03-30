from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from backend.services.order_service import OrderService
from backend.schemas.order import SchemaOrder

order_router = APIRouter(prefix='/order')

order_router.tags = ["Order"]

order_service = OrderService()


@order_router.post("/", response_model=SchemaOrder)
async def add_order(new_order: SchemaOrder):
    order = await order_service.create_order(new_order=new_order)

    return order


@order_router.get("/")
async def get_order_by_id():
    pass


@order_router.patch("/")
async def update_order():
    pass

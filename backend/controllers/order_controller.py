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


@order_router.get("/{order_id}", response_model=SchemaOrder)
async def get_order_by_id(order_id: int):
    order = await order_service.get_order_by_id(order_id=order_id)

    if type(order) is Exception:
        raise HTTPException(status_code=400, detail=str(order))

    return order


@order_router.patch("/", response_model=SchemaOrder)
async def update_order(patch_data: SchemaOrder):
    if patch_data.id is None:
        raise HTTPException(status_code=400, detail="Data should contain order_id")

    updated_order = await order_service.update_order(patch_data=patch_data)

    if type(updated_order) is Exception:
        raise HTTPException(status_code=400, detail=str(updated_order))

    return updated_order

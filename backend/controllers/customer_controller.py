from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from backend.services.customer_service import CustomerService
from backend.schemas.customer import SchemaCustomer

customer_router = APIRouter(prefix='/customer')

customer_router.tags = ["Customer"]

customer_service = CustomerService()


@customer_router.post("/", response_model=SchemaCustomer)
async def add_customer(new_customer: SchemaCustomer):
    customer = await customer_service.add_customer(new_customer=new_customer)
    if type(customer) is Exception:
        raise HTTPException(status_code=400, detail=str(customer))

    return new_customer


@customer_router.get("/", response_model=SchemaCustomer)
async def get_customer(customer_id: int):
    customer = await customer_service.get_customer(customer_id=customer_id)
    if type(customer) is Exception:
        raise HTTPException(status_code=400, detail=str(customer))

    return customer


@customer_router.patch("/", response_model=SchemaCustomer)
async def update_customer(customer: SchemaCustomer):
    customer = await customer_service.update_customer(customer=customer)
    if type(customer) is Exception:
        raise HTTPException(status_code=400, detail=str(customer))

    return customer


@customer_router.delete("/", response_model=int)
async def delete_customer(customer_id: int):
    deleted_customer_id = await customer_service.delete_customer(customer_id=customer_id)

    if type(deleted_customer_id) is Exception:
        raise HTTPException(status_code=400, detail=str(deleted_customer_id))

    return deleted_customer_id

from fastapi import APIRouter
from fastapi.exceptions import HTTPException


driver_router = APIRouter(prefix='/driver')

driver_router.tags = ["Driver"]


@driver_router.post("/test", response_model=str)
async def test(test_text: str):

    return test_text

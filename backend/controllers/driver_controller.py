from fastapi import APIRouter
from fastapi.exceptions import HTTPException


driver_router = APIRouter(prefix='/driver')

driver_router.tags = ["Driver"]

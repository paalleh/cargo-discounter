import os
from dotenv import load_dotenv


if os.path.exists('../.env'):
    load_dotenv('../.env')


import uvicorn
from fastapi import FastAPI
from backend.controllers.driver_controller import driver_router
from backend.controllers.car_controller import car_router
from backend.controllers.customer_controller import customer_router
from fastapi_sqlalchemy import DBSessionMiddleware
from backend.settings.db_settings import DBSettings


app = FastAPI(openapi_prefix="/api/v1")
app.add_middleware(
    DBSessionMiddleware,
    db_url=f'postgresql+psycopg2://{DBSettings.CONNECTION_DATA}'
)

app.include_router(driver_router)
app.include_router(car_router)
app.include_router(customer_router)


if __name__ == "__main__":
    uvicorn.run(app, port=9000)

import os
from dotenv import load_dotenv


if os.path.exists('../.env'):
    load_dotenv('../.env')


import uvicorn
from fastapi import FastAPI
from backend.controllers.driver_controller import driver_router
from backend.models.base import Base
from fastapi_sqlalchemy import DBSessionMiddleware
from backend.settings.db_settings import DBSettings


app = FastAPI(openapi_prefix="/api/v1")
app.add_middleware(
    DBSessionMiddleware,
    db_url=f'postgresql+psycopg2://{DBSettings.CONNECTION_DATA}'
)

app.include_router(driver_router)


if __name__ == "__main__":
    Base.metadata.create_all(bind=DBSettings.engine)
    uvicorn.run(app, port=9000)

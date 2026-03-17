from fastapi import FastAPI
import logging

from .core.logging_config import set_logger
from .db.database import engine, SessionLocal, Base
from .models.product import Product
from .routers import products



set_logger()
logger = logging.getLogger(__name__)

logger.info("starting the app")
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health-check")
async def check_health():

    return "Welcome"


app.include_router(products.router)

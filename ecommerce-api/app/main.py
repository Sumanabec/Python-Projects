from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager


from .core.logging_config import set_logger
from .db.database import engine, AsyncSessionLocal, Base
from .db.init_db import init_db
from .models.product import Product
from .routers import products, load_products



set_logger()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.exception(f"Startup failed : {e}")

    yield


app = FastAPI(lifespan=lifespan)

#Base.metadata.create_all(bind=engine)

@app.get("/health-check")
async def check_health():
    return "Welcome"


app.include_router(products.router)
app.include_router(load_products.router)

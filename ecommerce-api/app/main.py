from fastapi import FastAPI

from .db.database import engine, SessionLocal, Base
from .models.product import Product
from .routers import products



app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health-check")
async def check_health():
    return "Welcome"


app.include_router(products.router)

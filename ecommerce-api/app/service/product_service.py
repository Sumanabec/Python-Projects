from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

from app.repositories import product_repository 
from app.db.database import get_db
from ..models.product import Product
from ..schemas.product import ProductUpdate


def list_all_products(db: Session):
    return product_repository.get_all_products(db)


def create_product(db: Session, product):
    product_model = Product(**product.model_dump())
    #print(product.model_dump())
    if not product_model:
        return None
    return product_repository.create_product(db, product_model)


def update_product(db:Session, product_id: int, data: ProductUpdate):
    db_product = product_repository.get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    return product_repository.update_product(db, db_product, update_data)
    

from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
import logging

from app.repositories import product_repository 
from app.db.database import get_db
from ..models.product import Product
from ..schemas.product import ProductUpdate, ProductCreate


logger = logging.getLogger(__name__)

def list_all_products(db: Session):
    return product_repository.get_all_products(db)



def get_product(db: Session, product_id: int):
    return product_repository.get_product(db, product_id)



def create_product(db: Session, product_data:ProductCreate):
    existing_product = product_repository.get_product(db, product_data.id)
    if existing_product:
        return None
    
    product = Product(**product_data.model_dump())
    return product_repository.create_product(db, product)



def update_product(db:Session, product_id: int, data: ProductUpdate):
    db_product = product_repository.get_product(db, product_id)
    
    if not db_product:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    return product_repository.update_product(db, db_product, update_data)



def delete_product(db:Session, product_id:int):
    db_product = product_repository.get_product(db, product_id)
    if not db_product:
        logger.info(f"product does not exist: {product_id}")
        return None
    
    deleted_product_id = product_repository.delete_product(db, db_product)
    logger.info(f"deleted product id: {deleted_product_id}")
    return deleted_product_id

    
    

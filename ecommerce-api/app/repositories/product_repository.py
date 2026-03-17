from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends
import logging

from ..db.database import get_db
from ..models.product import Product


logger = logging.getLogger(__name__)


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product(db:Session, product_id:int):
    return db.query(Product).filter(Product.id == product_id).first()



def create_product(db: Session, product: Product):
    try:
        db.add(product)
        db.commit() 
        db.refresh(product)
        logger.info(f"Created product: {product.id}")
        return product.id
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating product : {e}")
        return None



def update_product(db: Session, db_product: Product, data: dict):
    try:
        for field, value in data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error in updating product: {db_product.id}")
        return None



def delete_product(db: Session, db_product: Product):
    product_id = db_product.id
    try:
        db.delete(db_product)
        db.commit()
        return product_id
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error in deleting the product")
        return None

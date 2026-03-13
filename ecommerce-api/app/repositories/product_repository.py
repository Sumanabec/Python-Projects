from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from ..db.database import get_db
from ..models.product import Product



def get_all_products(db: Session):
    return db.query(Product).all()


def get_product(db:Session, product_id:int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product_model):
    db.add(product_model)
    db.commit() 
    db.refresh(product_model)
    return product_model.id


def update_product(db: Session, db_product, data):
    for field, value in data.items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    
    return db_product

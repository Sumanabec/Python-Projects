from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends
import logging

from ..db.database import get_db
from ..models.product import Product


logger = logging.getLogger(__name__)


async def get_all_products(db: AsyncSession):
    try:
        result = await db.execute(select(Product))
        return result.scalars().all()
    except SQLAlchemyError as err:
        logger.error(err)
        return None
    


async def get_product(db:AsyncSession, product_id:int):
    try:
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()
    except SQLAlchemyError as err:
        logger.error(err)
        return None



async def create_product(db: AsyncSession, product: Product):
    try:
        db.add(product)
        await db.commit() 
        await db.refresh(product)
        logger.info(f"Created product: {product.id}")
        return product
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error creating product : {e}")
        return None



async def update_product(db: AsyncSession, db_product: Product, data: dict):
    try:
        for field, value in data.items():
            setattr(db_product, field, value)
        await db.commit()
        await db.refresh(db_product)
        return db_product
    except SQLAlchemyError as sql_err:
        await db.rollback()
        logger.error(f"Error in updating product: {db_product.id}, {sql_err}")
        return None
    except Exception as e:
        logger.error(e)



async def delete_product(db: AsyncSession, db_product: Product):
    product_id = db_product.id
    try:
        db.delete(db_product)
        await db.commit()
        return product_id
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error in deleting the product")
        return None

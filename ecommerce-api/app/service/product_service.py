from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import logging

from app.repositories import product_repository 
from app.db.database import get_db
from ..models.product import Product
from ..schemas.product import ProductUpdate, ProductCreate


logger = logging.getLogger(__name__)


async def list_all_products(db: AsyncSession):
    return await product_repository.get_all_products(db)



async def get_product(db: AsyncSession, product_id: int):
    product = await product_repository.get_product(db, product_id)
    return product



async def create_product(db: AsyncSession, product_data:ProductCreate):
    existing_product = await product_repository.get_product(db, product_data.id)
    if existing_product:
        return None
    
    product = Product(**product_data.model_dump())
    return await product_repository.create_product(db, product)



async def update_product(db: AsyncSession, product_id: int, data: ProductUpdate):
    
    db_product = await product_repository.get_product(db, product_id)
    if not db_product:
        return None
    logger.info(f"got the product {db_product}")

    update_data = data.model_dump(exclude_unset=True)
    result = await product_repository.update_product(db, db_product, update_data)
    logger.info(f"after update : {result}")
    return result



async def delete_product(db: AsyncSession, product_id:int):
    db_product = await product_repository.get_product(db, product_id)
    if not db_product:
        logger.info(f"product does not exist: {product_id}")
        return None
    
    deleted_product_id = await product_repository.delete_product(db, db_product)
    logger.info(f"deleted product id: {deleted_product_id}")
    return deleted_product_id

    
    

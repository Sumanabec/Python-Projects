from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from pydantic import Field
import logging


from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate
from ..models.product import Product
from ..db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.service import product_service


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/product",
    tags=["Products"]
)


db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.get("/all-products", response_model=list[ProductResponse])
async def get_products(db: Session = Depends(get_db)):

    products = await product_service.list_all_products(db)
    logger.info(f"Fetching all {len(products)} products from database")
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, 
            detail="There is no product to list"
            )

    return products



@router.get("/get-product", response_model=ProductResponse)
async def get_product(db: db_dependency, product_id: int):
    product = await product_service.get_product(db, product_id)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item Not Found"
            )
    return product



@router.post("/create-product", response_model=ProductResponse, summary="Create a new product")
async def create_product(
                db: db_dependency, 
                product_data: ProductCreate
            ):
    logger.info(f"Creating a new product")
    product = await product_service.create_product(db, product_data)
    
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="product already exist or could not be created"
            )
    return product



@router.patch("/update-product/{id}", summary="Update existing product")
async def update_product(db:db_dependency, id:int,  data:ProductUpdate):
    updated_product = await product_service.update_product(db, id, data)
    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product Not Found"
            )
    
    return {
            "message": "Successfully updated", 
            "Product ID": id
            }


@router.delete("/delete-product/{id}", summary="Delete product")
def delete_product(db:db_dependency, id: int):
    response = product_service.delete_product(db, id)
    
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item Not Found or could not be deleted"
            )
    
    return {
        "message": "Successfully deleted",
        "Product ID": response
        } 
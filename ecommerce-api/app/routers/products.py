from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from pydantic import Field

from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate
from ..models.product import Product
from ..db.database import get_db
from sqlalchemy.orm import Session
from app.service import product_service


router = APIRouter()


db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = product_service.list_all_products(db)
    return products



@router.post("/create-product")
async def create_product(db: db_dependency, product: ProductCreate):
    
    # product_model = Product(**product.model_dump())
    # db.add(product_model)
    # db.commit()
    product_id = product_service.create_product(db, product)
    if product_id is None:
        return {"message": "Not created"}
    return {"message": "Product created successfully", "Product ID": product_id}



@router.get("/get-product/", response_model=ProductResponse)
async def get_product(db: db_dependency, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")
    return product



@router.patch("/update-product/{id}")
async def update_product(db:db_dependency, id:int,  data:ProductUpdate):
    # db_product = db.query(Product).filter(Product.id == id).first()
    # if db_product is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")
    
    # update_data = product.model_dump(exclude_unset=True)
    
    # for field, value in update_data.items():
    #     setattr(db_product, field, value)
    # db.commit()
    updated_product = product_service.update_product(db, id, data)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")
    return {
            "message": "Successfully updated", 
            "Product ID": id
            }


@router.delete("/delete-product/{id}")
async def delete_product(id: int, db:db_dependency):
    db_product = db.get(Product, id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Item Not Found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Successfully deleted", "Product ID": db_product.id} 
from fastapi import APIRouter, Depends, HTTPException
import requests
from requests.exceptions import HTTPError
import logging
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.product_scraper import scrape_products
from ..service.product_service import create_product
from ..db.database import get_db
from ..schemas.product import ProductCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Admin"]
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]

# http://books.toscrape.com/


@router.get("/load-products")
async def load_products(url: str, db: db_dependency):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_error:
        logger.error(http_error)
        raise HTTPException(status_code=400, detail="Failed to fetch url")
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=500, detail="Unexpected error occured")
    
    logger.info("Successfully loaded the url")
    if not response:
        logger.error("Empty or Invalid response received")
        raise HTTPException(status_code=400, detail="Empty or Invalid response received")
    
    try:
        product_list = scrape_products(response)
    except Exception as e:
        logger.exception("Scraping failed {e}")
        raise HTTPException(status_code=500, detail="Scraping failed")

    if not product_list:
        return {"message": "No Product Found"}
    
    product_created_count = 0
    for product in product_list:
        try:
            product_obj = ProductCreate(**product)
            await create_product(db, product_obj)
            product_created_count+=1
        except Exception as e:
            logger.error(f"Error while creating product in database: {e}")
            continue
    
    return {
        "message": "Products created successfully",
        "total_scraped": len(product_list),
        "total_created": product_created_count
    }

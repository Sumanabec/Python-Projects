from bs4 import BeautifulSoup
from requests import Response
import logging
import re
import csv


logger = logging.getLogger(__name__)


def load_products_in_csv(filepath, product_data: list[dict], header):
    fieldnames = list(header)
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(product_data)



def scrape_products(response: Response):
    products = []
    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_blocks = soup.find_all("li", class_ = "col-xs-6 col-sm-4 col-md-3 col-lg-3")
        if not product_blocks:
            logger.warning("No product blocks found on the page")
            return []

        id = 100
        for product in product_blocks:
            try:
                product_name = product.find("a").find("img")["alt"]
                product_description = product_name
                product_price = product.find("p", class_="price_color").text

                pattern = r"\d+\.\d+"
                match = re.search(pattern, product_price)
                product_price = float(match.group(0))
                
                products.append({
                    "id": id,
                    "name": product_name,
                    "description": product_description,
                    "price": product_price,
                    "stock": 1000
                })
                id+=1
            except Exception as e:
                logger.error(f"Error parsing the product block: {e}")
                logger.error(f"product: {product}")
                load_products_in_csv("data/error.csv", product, [])
                continue

        if not products:
            logger.warning("No product to load")
            return []
        try:
            load_products_in_csv("data/products.csv", products, products[0].keys())
        except Exception as e:
            logger.exception(e)
            
        return products
    except Exception as e:
        logger.error(f"Critical error : {e}")
        return []




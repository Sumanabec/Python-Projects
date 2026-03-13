from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime



class ProductBase(BaseModel):
    id: int =Field(gt=0)
    name: str = Field(max_length=100)
    description: str = Field(default=None, max_length=500)
    price: float =Field(gt=0)
    stock: int = Field(default=0)
    date_created: datetime | None = Field(default_factory=datetime.now)
    date_modified: datetime | None = Field(default_factory=datetime.now)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int | None = None
    name: str | None = None
    price: float | None = None
    #date_modified: datetime = Field(default_factory=datetime.now())


class ProductResponse(ProductBase):
    id: int
    name: str
    description: str
    
    
    


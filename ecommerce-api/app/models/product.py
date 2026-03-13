from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..db.database import Base, engine


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    date_created = Column(DateTime, default=datetime.now())
    date_modified = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

Base.metadata.create_all(bind=engine)

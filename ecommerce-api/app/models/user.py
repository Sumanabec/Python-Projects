from sqlalchemy import Column, Integer, Float, String, DateTime
from ..db.database import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer)
    
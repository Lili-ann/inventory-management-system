from sqlalchemy import Column, String, Integer
from database import Base
import uuid

class Item(Base):
    __tablename__ = "items" # tablename

    # Defining the columns for items table 
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)   
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
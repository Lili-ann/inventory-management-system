from pydantic import BaseModel

# Base properties for an Item
class ItemBase(BaseModel):
    name: str
    description: str
    price: int
    stock: int

# Schema for creating an item (user doesn't send the ID, we generate it)
class ItemCreate(ItemBase):
    pass

# Schema for what the API returns back to the user (includes the ID)
class ItemResponse(ItemBase):
    id: str

    class Config:
        from_attributes = True # This tells Pydantic to cleanly read your SQLAlchemy database model
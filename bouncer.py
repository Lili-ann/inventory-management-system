from pydantic import BaseModel

# Base properties for an Item
class ItemBase(BaseModel):
    name: str
    description: str
    price: int
    stock: int

# Schema for creating an item 
class ItemCreate(ItemBase):
    pass

# Schema for what the API returns back to the user (includes the ID)
class ItemResponse(ItemBase):
    id: str

    class Config:
        from_attributes = True 
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    stock: int
    date: datetime
    owner_id: str

    model_config = {"from_attributes": True}
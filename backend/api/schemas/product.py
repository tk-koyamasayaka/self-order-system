from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# 商品スキーマ
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    image: Optional[str] = None
    is_available: bool = True
    order: int = 0
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image: Optional[str] = None
    is_available: Optional[bool] = None
    order: Optional[int] = None
    category_id: Optional[int] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
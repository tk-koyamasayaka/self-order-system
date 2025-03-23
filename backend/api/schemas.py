from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# カテゴリスキーマ
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    order: int = 0
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


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


# 注文明細スキーマ
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int
    price: int
    created_at: datetime
    product: ProductOut

    class Config:
        orm_mode = True


# 注文スキーマ
class OrderBase(BaseModel):
    table_number: int
    status: str = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None


class OrderOut(OrderBase):
    id: int
    total_price: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        orm_mode = True


# エラーレスポンススキーマ
class ErrorResponse(BaseModel):
    detail: str
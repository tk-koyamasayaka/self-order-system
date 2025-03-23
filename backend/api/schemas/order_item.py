from pydantic import BaseModel
from datetime import datetime
from .product import ProductOut


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
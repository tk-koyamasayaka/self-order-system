from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .order_item import OrderItemCreate, OrderItemOut


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
        
    @classmethod
    def from_orm(cls, obj):
        # 明示的にitemsリレーションを処理
        if hasattr(obj, 'items'):
            # 新しいオブジェクトを作成して返す
            return cls(
                id=obj.id,
                table_number=obj.table_number,
                status=obj.status,
                total_price=obj.total_price,
                created_at=obj.created_at,
                updated_at=obj.updated_at,
                # 明示的にリストに変換
                items=[OrderItemOut.from_orm(item) for item in obj.items.all()]
            )
        return super().from_orm(obj)
from typing import List
from ninja import Router

from api.schemas.order import OrderOut, OrderCreate, OrderUpdate
from api.services.order_service import OrderService

# 注文ルーター
order_router = Router(tags=["注文"])

@order_router.get("", response=List[OrderOut])
def list_orders(request, table_number: int = None):
    """注文一覧を取得"""
    if table_number:
        return OrderService().get_orders_by_table(table_number)
    return OrderService().get_all_orders()

@order_router.get("/{order_id}", response=OrderOut)
def get_order(request, order_id: int):
    """注文詳細を取得"""
    return OrderService().get_order_by_id(order_id)

@order_router.post("", response={201: OrderOut})
def create_order(request, payload: OrderCreate):
    """注文を作成"""
    # OrderCreateスキーマをディクショナリに変換
    order_data = {
        'table_number': payload.table_number,
        'status': payload.status,
        'items': [item.dict() for item in payload.items]
    }
    
    order = OrderService().create_order(order_data)
    return 201, order

@order_router.put("/{order_id}", response=OrderOut)
def update_order(request, order_id: int, payload: OrderUpdate):
    """注文を更新"""
    # 更新するフィールドを抽出
    update_data = payload.dict(exclude_unset=True)
    return OrderService().update_order(order_id, update_data)

@order_router.delete("/{order_id}", response={204: None})
def delete_order(request, order_id: int):
    """注文を削除"""
    OrderService().delete_order(order_id)
    return 204, None
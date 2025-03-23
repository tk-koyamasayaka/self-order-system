from typing import List, Optional
from django.db.models import QuerySet

from core.models import OrderItem, Order, Product
from api.dao.base_dao import BaseDAO


class OrderItemDAO(BaseDAO[OrderItem]):
    """
    注文明細モデルのデータアクセスオブジェクト
    """
    
    model_class = OrderItem
    
    def get_items_by_order(self, order_id: int) -> QuerySet[OrderItem]:
        """
        注文IDによる注文明細の取得
        
        Args:
            order_id: 注文ID
            
        Returns:
            指定された注文の注文明細QuerySet
        """
        return OrderItem.objects.filter(order_id=order_id)
    
    def create_order_item(self, order: Order, product: Product, quantity: int, price: int) -> OrderItem:
        """
        注文明細の作成
        
        Args:
            order: 注文オブジェクト
            product: 商品オブジェクト
            quantity: 数量
            price: 価格
            
        Returns:
            作成された注文明細
        """
        return OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price
        )
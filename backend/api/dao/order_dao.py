from typing import List, Optional
from django.db.models import QuerySet, Prefetch

from core.models import Order, OrderItem
from api.dao.base_dao import BaseDAO


class OrderDAO(BaseDAO[Order]):
    """
    注文モデルのデータアクセスオブジェクト
    """
    
    model_class = Order
    
    def get_orders_with_items(self) -> QuerySet[Order]:
        """
        注文明細を含む注文一覧を取得
        
        Returns:
            注文明細を含む注文QuerySet
        """
        return Order.objects.prefetch_related(
            'items__product'
        )
    
    def get_orders_by_table(self, table_number: int) -> QuerySet[Order]:
        """
        テーブル番号による注文の取得
        
        Args:
            table_number: テーブル番号
            
        Returns:
            指定されたテーブルの注文QuerySet
        """
        return Order.objects.filter(table_number=table_number)
    
    def get_order_with_items(self, order_id: int) -> Order:
        """
        注文明細を含む注文詳細を取得
        
        Args:
            order_id: 注文ID
            
        Returns:
            注文明細を含む注文オブジェクト
        """
        return self.get_by_id(order_id)
    
    def create_order(self, table_number: int, status: str = 'pending', total_price: int = 0) -> Order:
        """
        注文の作成
        
        Args:
            table_number: テーブル番号
            status: 注文ステータス
            total_price: 合計金額
            
        Returns:
            作成された注文
        """
        return Order.objects.create(
            table_number=table_number,
            status=status,
            total_price=total_price
        )
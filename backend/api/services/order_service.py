from typing import List, Optional, Dict, Any
from django.db.models import QuerySet
from django.db import transaction

from core.models import Order, OrderItem, Product
from api.dao.order_dao import OrderDAO
from api.dao.order_item_dao import OrderItemDAO
from api.dao.product_dao import ProductDAO


class OrderService:
    """
    注文に関するビジネスロジックを提供するサービスクラス
    """
    
    def __init__(self):
        """コンストラクタ"""
        self.order_dao = OrderDAO()
        self.order_item_dao = OrderItemDAO()
        self.product_dao = ProductDAO()
    
    def get_all_orders(self) -> QuerySet[Order]:
        """
        すべての注文を取得
        
        Returns:
            すべての注文のQuerySet
        """
        return self.order_dao.get_orders_with_items()
    
    def get_orders_by_table(self, table_number: int) -> QuerySet[Order]:
        """
        テーブル番号による注文の取得
        
        Args:
            table_number: テーブル番号
            
        Returns:
            指定されたテーブルの注文QuerySet
        """
        return self.order_dao.get_orders_by_table(table_number)
    
    def get_order_by_id(self, order_id: int) -> Order:
        """
        IDによる注文取得
        
        Args:
            order_id: 注文ID
            
        Returns:
            指定されたIDの注文
        """
        return self.order_dao.get_order_with_items(order_id)
    
    @transaction.atomic
    def create_order(self, data: Dict[str, Any]) -> Order:
        """
        注文の作成
        
        Args:
            data: 注文データ
            {
                'table_number': int,
                'status': str,
                'items': [
                    {
                        'product_id': int,
                        'quantity': int
                    },
                    ...
                ]
            }
            
        Returns:
            作成された注文
        """
        # 注文の作成
        order = self.order_dao.create_order(
            table_number=data['table_number'],
            status=data['status'],
            total_price=0  # 初期値
        )
        
        # 注文明細の作成と合計金額の計算
        total_price = 0
        for item_data in data['items']:
            product = self.product_dao.get_by_id(item_data['product_id'])
            
            # 注文明細の作成
            self.order_item_dao.create_order_item(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
            
            # 合計金額の計算
            total_price += product.price * item_data['quantity']
        
        # 合計金額の更新
        self.order_dao.update(order, total_price=total_price)
        
        # 最新の注文データを取得して返す
        return self.order_dao.get_order_with_items(order.id)
    
    def update_order(self, order_id: int, data: Dict[str, Any]) -> Order:
        """
        注文の更新
        
        Args:
            order_id: 注文ID
            data: 更新データ
            
        Returns:
            更新された注文
        """
        order = self.order_dao.get_by_id(order_id)
        return self.order_dao.update(order, **data)
    
    def delete_order(self, order_id: int) -> None:
        """
        注文の削除
        
        Args:
            order_id: 注文ID
        """
        order = self.order_dao.get_by_id(order_id)
        self.order_dao.delete(order)
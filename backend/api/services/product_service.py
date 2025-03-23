from typing import List, Optional, Dict, Any
from django.db.models import QuerySet

from core.models import Product
from api.dao.product_dao import ProductDAO
from api.dao.category_dao import CategoryDAO


class ProductService:
    """
    商品に関するビジネスロジックを提供するサービスクラス
    """
    
    def __init__(self):
        """コンストラクタ"""
        self.product_dao = ProductDAO()
        self.category_dao = CategoryDAO()
    
    def get_all_products(self, available_only: bool = True) -> QuerySet[Product]:
        """
        すべての商品を取得
        
        Args:
            available_only: 販売可能な商品のみを取得するかどうか
            
        Returns:
            商品のQuerySet
        """
        if available_only:
            return self.product_dao.get_available_products()
        return self.product_dao.get_all()
    
    def get_products_by_category(self, category_id: int, available_only: bool = True) -> QuerySet[Product]:
        """
        カテゴリIDによる商品の取得
        
        Args:
            category_id: カテゴリID
            available_only: 販売可能な商品のみを取得するかどうか
            
        Returns:
            指定されたカテゴリの商品QuerySet
        """
        # カテゴリの存在確認
        self.category_dao.get_by_id(category_id)
        return self.product_dao.get_products_by_category(category_id, available_only)
    
    def get_product_by_id(self, product_id: int) -> Product:
        """
        IDによる商品取得
        
        Args:
            product_id: 商品ID
            
        Returns:
            指定されたIDの商品
        """
        return self.product_dao.get_by_id(product_id)
    
    def create_product(self, data: Dict[str, Any]) -> Product:
        """
        商品の作成
        
        Args:
            data: 商品データ
            
        Returns:
            作成された商品
        """
        # カテゴリの存在確認
        self.category_dao.get_by_id(data['category_id'])
        return self.product_dao.create(**data)
    
    def update_product(self, product_id: int, data: Dict[str, Any]) -> Product:
        """
        商品の更新
        
        Args:
            product_id: 商品ID
            data: 更新データ
            
        Returns:
            更新された商品
        """
        product = self.product_dao.get_by_id(product_id)
        
        # カテゴリIDが含まれている場合、存在確認
        if 'category_id' in data:
            self.category_dao.get_by_id(data['category_id'])
            
        return self.product_dao.update(product, **data)
    
    def delete_product(self, product_id: int) -> None:
        """
        商品の削除
        
        Args:
            product_id: 商品ID
        """
        product = self.product_dao.get_by_id(product_id)
        self.product_dao.delete(product)
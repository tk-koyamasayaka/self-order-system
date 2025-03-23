from typing import List, Optional
from django.db.models import QuerySet

from core.models import Product
from api.dao.base_dao import BaseDAO


class ProductDAO(BaseDAO[Product]):
    """
    商品モデルのデータアクセスオブジェクト
    """
    
    model_class = Product
    
    def get_available_products(self) -> QuerySet[Product]:
        """
        販売可能な商品のみを取得
        
        Returns:
            販売可能な商品のQuerySet
        """
        return Product.objects.filter(is_available=True)
    
    def get_products_by_category(self, category_id: int, available_only: bool = True) -> QuerySet[Product]:
        """
        カテゴリIDによる商品の取得
        
        Args:
            category_id: カテゴリID
            available_only: 販売可能な商品のみを取得するかどうか
            
        Returns:
            指定されたカテゴリの商品QuerySet
        """
        query = Product.objects.filter(category_id=category_id)
        if available_only:
            query = query.filter(is_available=True)
        return query
from typing import List, Optional
from django.db.models import QuerySet

from core.models import Category
from api.dao.base_dao import BaseDAO


class CategoryDAO(BaseDAO[Category]):
    """
    カテゴリモデルのデータアクセスオブジェクト
    """
    
    model_class = Category
    
    def get_active_categories(self) -> QuerySet[Category]:
        """
        有効なカテゴリのみを取得
        
        Returns:
            有効なカテゴリのQuerySet
        """
        return Category.objects.filter(is_active=True)
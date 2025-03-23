from typing import List, Optional, Dict, Any
from django.db.models import QuerySet

from core.models import Category
from api.dao.category_dao import CategoryDAO


class CategoryService:
    """
    カテゴリに関するビジネスロジックを提供するサービスクラス
    """
    
    def __init__(self):
        """コンストラクタ"""
        self.category_dao = CategoryDAO()
    
    def get_all_categories(self) -> QuerySet[Category]:
        """
        すべてのカテゴリを取得
        
        Returns:
            すべてのカテゴリのQuerySet
        """
        return self.category_dao.get_all()
    
    def get_active_categories(self) -> QuerySet[Category]:
        """
        有効なカテゴリのみを取得
        
        Returns:
            有効なカテゴリのQuerySet
        """
        return self.category_dao.get_active_categories()
    
    def get_category_by_id(self, category_id: int) -> Category:
        """
        IDによるカテゴリ取得
        
        Args:
            category_id: カテゴリID
            
        Returns:
            指定されたIDのカテゴリ
        """
        return self.category_dao.get_by_id(category_id)
    
    def create_category(self, data: Dict[str, Any]) -> Category:
        """
        カテゴリの作成
        
        Args:
            data: カテゴリデータ
            
        Returns:
            作成されたカテゴリ
        """
        return self.category_dao.create(**data)
    
    def update_category(self, category_id: int, data: Dict[str, Any]) -> Category:
        """
        カテゴリの更新
        
        Args:
            category_id: カテゴリID
            data: 更新データ
            
        Returns:
            更新されたカテゴリ
        """
        category = self.category_dao.get_by_id(category_id)
        return self.category_dao.update(category, **data)
    
    def delete_category(self, category_id: int) -> None:
        """
        カテゴリの削除
        
        Args:
            category_id: カテゴリID
        """
        category = self.category_dao.get_by_id(category_id)
        self.category_dao.delete(category)
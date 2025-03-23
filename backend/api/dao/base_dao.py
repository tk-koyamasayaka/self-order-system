from typing import List, Optional, TypeVar, Generic, Type
from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404

# ジェネリック型の定義
T = TypeVar('T', bound=Model)

class BaseDAO(Generic[T]):
    """
    データアクセスオブジェクトの基底クラス
    基本的なCRUD操作を提供する
    
    このクラスは抽象クラスとして使用され、具体的なDAOクラスで
    モデルクラスを直接指定することを想定しています。
    """
    
    model_class = None
    
    def get_all(self) -> QuerySet[T]:
        """
        すべてのオブジェクトを取得
        
        Returns:
            すべてのオブジェクトのQuerySet
        """
        return self.model_class.objects.all()
    
    def get_by_id(self, id: int) -> T:
        """
        IDによるオブジェクト取得
        
        Args:
            id: オブジェクトのID
            
        Returns:
            指定されたIDのオブジェクト
            
        Raises:
            Http404: オブジェクトが存在しない場合
        """
        return get_object_or_404(self.model_class, id=id)
    
    def create(self, **kwargs) -> T:
        """
        オブジェクトの作成
        
        Args:
            **kwargs: オブジェクトの属性
            
        Returns:
            作成されたオブジェクト
        """
        return self.model_class.objects.create(**kwargs)
    
    def update(self, instance: T, **kwargs) -> T:
        """
        オブジェクトの更新
        
        Args:
            instance: 更新するオブジェクト
            **kwargs: 更新する属性
            
        Returns:
            更新されたオブジェクト
        """
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def delete(self, instance: T) -> None:
        """
        オブジェクトの削除
        
        Args:
            instance: 削除するオブジェクト
        """
        instance.delete()
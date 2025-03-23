from typing import List
from ninja import Router

from api.schemas.category import CategoryOut, CategoryCreate, CategoryUpdate
from api.services.category_service import CategoryService

# カテゴリルーター
category_router = Router(tags=["カテゴリ"])

@category_router.get("", response=List[CategoryOut])
def list_categories(request):
    """カテゴリ一覧を取得"""
    return CategoryService().get_active_categories()

@category_router.get("/{category_id}", response=CategoryOut)
def get_category(request, category_id: int):
    """カテゴリ詳細を取得"""
    return CategoryService().get_category_by_id(category_id)

@category_router.post("", response={201: CategoryOut})
def create_category(request, payload: CategoryCreate):
    """カテゴリを作成"""
    category = CategoryService().create_category(payload.dict())
    return 201, category

@category_router.put("/{category_id}", response=CategoryOut)
def update_category(request, category_id: int, payload: CategoryUpdate):
    """カテゴリを更新"""
    # 更新するフィールドを抽出
    update_data = payload.dict(exclude_unset=True)
    return CategoryService().update_category(category_id, update_data)

@category_router.delete("/{category_id}", response={204: None})
def delete_category(request, category_id: int):
    """カテゴリを削除"""
    CategoryService().delete_category(category_id)
    return 204, None
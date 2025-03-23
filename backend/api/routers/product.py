from typing import List
from ninja import Router

from api.schemas.product import ProductOut, ProductCreate, ProductUpdate
from api.services.product_service import ProductService

# 商品ルーター
product_router = Router(tags=["商品"])

@product_router.get("", response=List[ProductOut])
def list_products(request, category_id: int = None):
    """商品一覧を取得"""
    if category_id:
        return ProductService().get_products_by_category(category_id)
    return ProductService().get_all_products()

@product_router.get("/{product_id}", response=ProductOut)
def get_product(request, product_id: int):
    """商品詳細を取得"""
    return ProductService().get_product_by_id(product_id)

@product_router.post("", response={201: ProductOut})
def create_product(request, payload: ProductCreate):
    """商品を作成"""
    product = ProductService().create_product(payload.dict())
    return 201, product

@product_router.put("/{product_id}", response=ProductOut)
def update_product(request, product_id: int, payload: ProductUpdate):
    """商品を更新"""
    # 更新するフィールドを抽出
    update_data = payload.dict(exclude_unset=True)
    return ProductService().update_product(product_id, update_data)

@product_router.delete("/{product_id}", response={204: None})
def delete_product(request, product_id: int):
    """商品を削除"""
    ProductService().delete_product(product_id)
    return 204, None
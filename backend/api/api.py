from typing import List
from ninja import NinjaAPI, Router
from ninja.errors import ValidationError
from django.http import Http404

from api.schemas import (
    CategoryOut, CategoryCreate, CategoryUpdate,
    ProductOut, ProductCreate, ProductUpdate,
    OrderOut, OrderCreate, OrderUpdate,
    ErrorResponse
)
from api.services.category_service import CategoryService
from api.services.product_service import ProductService
from api.services.order_service import OrderService

# NinjaAPIインスタンスの作成
api = NinjaAPI(
    title="セルフオーダーシステムAPI",
    description="飲食店向けセルフオーダーシステムのAPI",
    version="1.0.0",
    docs_url="/docs",
)

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

# 注文ルーター
order_router = Router(tags=["注文"])

@order_router.get("", response=List[OrderOut])
def list_orders(request, table_number: int = None):
    """注文一覧を取得"""
    if table_number:
        return OrderService().get_orders_by_table(table_number)
    return OrderService().get_all_orders()

@order_router.get("/{order_id}", response=OrderOut)
def get_order(request, order_id: int):
    """注文詳細を取得"""
    return OrderService().get_order_by_id(order_id)

@order_router.post("", response={201: OrderOut})
def create_order(request, payload: OrderCreate):
    """注文を作成"""
    # OrderCreateスキーマをディクショナリに変換
    order_data = {
        'table_number': payload.table_number,
        'status': payload.status,
        'items': [item.dict() for item in payload.items]
    }
    
    order = OrderService().create_order(order_data)
    return 201, order

@order_router.put("/{order_id}", response=OrderOut)
def update_order(request, order_id: int, payload: OrderUpdate):
    """注文を更新"""
    # 更新するフィールドを抽出
    update_data = payload.dict(exclude_unset=True)
    return OrderService().update_order(order_id, update_data)

@order_router.delete("/{order_id}", response={204: None})
def delete_order(request, order_id: int):
    """注文を削除"""
    OrderService().delete_order(order_id)
    return 204, None

# ルーターの登録
api.add_router("/categories/", category_router)
api.add_router("/products/", product_router)
api.add_router("/orders/", order_router)

# エラーハンドラー
@api.exception_handler(Http404)
def handle_not_found(request, exc):
    return api.create_response(request, {"detail": "リソースが見つかりません"}, status=404)

@api.exception_handler(ValidationError)
def handle_validation_error(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=422)
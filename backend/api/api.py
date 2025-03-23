from typing import List
from ninja import NinjaAPI, Router
from ninja.errors import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import Http404

from core.models import Category, Product, Order, OrderItem
from api.schemas import (
    CategoryOut, CategoryCreate, CategoryUpdate,
    ProductOut, ProductCreate, ProductUpdate,
    OrderOut, OrderCreate, OrderUpdate,
    ErrorResponse
)

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
    return Category.objects.filter(is_active=True)

@category_router.get("/{category_id}", response=CategoryOut)
def get_category(request, category_id: int):
    """カテゴリ詳細を取得"""
    return get_object_or_404(Category, id=category_id)

@category_router.post("", response={201: CategoryOut})
def create_category(request, payload: CategoryCreate):
    """カテゴリを作成"""
    category = Category.objects.create(**payload.dict())
    return 201, category

@category_router.put("/{category_id}", response=CategoryOut)
def update_category(request, category_id: int, payload: CategoryUpdate):
    """カテゴリを更新"""
    category = get_object_or_404(Category, id=category_id)
    
    # 更新するフィールドを抽出
    update_data = payload.dict(exclude_unset=True)
    
    # 各フィールドを更新
    for key, value in update_data.items():
        setattr(category, key, value)
    
    category.save()
    return category

@category_router.delete("/{category_id}", response={204: None})
def delete_category(request, category_id: int):
    """カテゴリを削除"""
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return 204, None

# 商品ルーター
product_router = Router(tags=["商品"])

@product_router.get("", response=List[ProductOut])
def list_products(request, category_id: int = None):
    """商品一覧を取得"""
    if category_id:
        return Product.objects.filter(category_id=category_id, is_available=True)
    return Product.objects.filter(is_available=True)

@product_router.get("/{product_id}", response=ProductOut)
def get_product(request, product_id: int):
    """商品詳細を取得"""
    return get_object_or_404(Product, id=product_id)

@product_router.post("", response={201: ProductOut})
def create_product(request, payload: ProductCreate):
    """商品を作成"""
    product = Product.objects.create(**payload.dict())
    return 201, product

@product_router.put("/{product_id}", response=ProductOut)
def update_product(request, product_id: int, payload: ProductUpdate):
    """商品を更新"""
    product = get_object_or_404(Product, id=product_id)
    
    # 更新するフィールドを抽出
    update_data = payload.dict(exclude_unset=True)
    
    # 各フィールドを更新
    for key, value in update_data.items():
        setattr(product, key, value)
    
    product.save()
    return product

@product_router.delete("/{product_id}", response={204: None})
def delete_product(request, product_id: int):
    """商品を削除"""
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return 204, None

# 注文ルーター
order_router = Router(tags=["注文"])

@order_router.get("", response=List[OrderOut])
def list_orders(request, table_number: int = None):
    """注文一覧を取得"""
    if table_number:
        return Order.objects.filter(table_number=table_number)
    return Order.objects.all()

@order_router.get("/{order_id}", response=OrderOut)
def get_order(request, order_id: int):
    """注文詳細を取得"""
    return get_object_or_404(Order, id=order_id)

@order_router.post("", response={201: OrderOut})
def create_order(request, payload: OrderCreate):
    """注文を作成"""
    with transaction.atomic():
        # 注文の作成
        order = Order.objects.create(
            table_number=payload.table_number,
            status=payload.status,
            total_price=0  # 初期値
        )
        
        # 注文明細の作成と合計金額の計算
        total_price = 0
        for item in payload.items:
            product = get_object_or_404(Product, id=item.product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )
            total_price += product.price * item.quantity
        
        # 合計金額の更新
        order.total_price = total_price
        order.save()
        
        return 201, order

@order_router.put("/{order_id}", response=OrderOut)
def update_order(request, order_id: int, payload: OrderUpdate):
    """注文を更新"""
    order = get_object_or_404(Order, id=order_id)
    
    # 更新するフィールドを抽出
    update_data = payload.dict(exclude_unset=True)
    
    # 各フィールドを更新
    for key, value in update_data.items():
        setattr(order, key, value)
    
    order.save()
    return order

@order_router.delete("/{order_id}", response={204: None})
def delete_order(request, order_id: int):
    """注文を削除"""
    order = get_object_or_404(Order, id=order_id)
    order.delete()
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
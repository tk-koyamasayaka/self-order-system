# api/register_routers.py
from api.api_config import api
from api.routers import category_router, product_router, order_router

def register_routers():
    api.add_router("/categories/", category_router)
    api.add_router("/products/", product_router)
    api.add_router("/orders/", order_router)

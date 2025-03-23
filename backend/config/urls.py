from django.contrib import admin
from django.urls import path
from api.api_config import api

from api.register_routers import register_routers

# Django 初期化後にルーターを登録
register_routers()

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
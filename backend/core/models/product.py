from django.db import models
from .category import Category


class Product(models.Model):
    """商品モデル"""
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='カテゴリ'
    )
    name = models.CharField('商品名', max_length=100)
    description = models.TextField('説明', blank=True)
    price = models.DecimalField('価格', max_digits=10, decimal_places=0)
    image = models.CharField('画像URL', max_length=255, blank=True)
    is_available = models.BooleanField('販売可能', default=True)
    order = models.IntegerField('表示順', default=0)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['category__order', 'order', 'id']

    def __str__(self):
        return self.name
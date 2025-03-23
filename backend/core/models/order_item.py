from django.db import models
from .order import Order
from .product import Product


class OrderItem(models.Model):
    """注文明細モデル"""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='注文'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='order_items',
        verbose_name='商品'
    )
    quantity = models.IntegerField('数量', default=1)
    price = models.DecimalField('価格', max_digits=10, decimal_places=0)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    class Meta:
        verbose_name = '注文明細'
        verbose_name_plural = '注文明細'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
from django.db import models


class Category(models.Model):
    """商品カテゴリモデル"""
    name = models.CharField('カテゴリ名', max_length=100)
    description = models.TextField('説明', blank=True)
    image = models.CharField('画像URL', max_length=255, blank=True)
    order = models.IntegerField('表示順', default=0)
    is_active = models.BooleanField('有効', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


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


class Order(models.Model):
    """注文モデル"""
    STATUS_CHOICES = (
        ('pending', '保留中'),
        ('processing', '処理中'),
        ('completed', '完了'),
        ('cancelled', 'キャンセル'),
    )
    
    table_number = models.IntegerField('テーブル番号')
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField('合計金額', max_digits=10, decimal_places=0)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '注文'
        verbose_name_plural = '注文'
        ordering = ['-created_at']

    def __str__(self):
        return f'注文 #{self.id} (テーブル {self.table_number})'


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
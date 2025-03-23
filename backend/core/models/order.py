from django.db import models


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
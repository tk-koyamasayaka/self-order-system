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
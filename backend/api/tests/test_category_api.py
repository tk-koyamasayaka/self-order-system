from django.test import TestCase, Client
from django.urls import reverse
from core.models import Category
import json
from datetime import datetime


class CategoryAPITest(TestCase):
    """カテゴリAPIのテストクラス"""

    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        # テスト用のカテゴリを作成
        self.category1 = Category.objects.create(
            name="テストカテゴリ1",
            description="テスト説明1",
            order=1,
            is_active=True
        )
        self.category2 = Category.objects.create(
            name="テストカテゴリ2",
            description="テスト説明2",
            order=2,
            is_active=False
        )

    def test_list_categories(self):
        """カテゴリ一覧取得APIのテスト"""
        # APIリクエスト
        response = self.client.get('/api/categories/')
        
        # レスポンスの検証
        self.assertEqual(response.status_code, 200)
        
        # JSONレスポンスをパース
        data = response.json()
        
        # アクティブなカテゴリのみが返されることを確認
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "テストカテゴリ1")
        self.assertEqual(data[0]['description'], "テスト説明1")
        self.assertEqual(data[0]['order'], 1)
        self.assertEqual(data[0]['is_active'], True)

    def test_get_category(self):
        """カテゴリ詳細取得APIのテスト"""
        # APIリクエスト
        response = self.client.get(f'/api/categories/{self.category1.id}')
        
        # レスポンスの検証
        self.assertEqual(response.status_code, 200)
        
        # JSONレスポンスをパース
        data = response.json()
        
        # 正しいカテゴリデータが返されることを確認
        self.assertEqual(data['id'], self.category1.id)
        self.assertEqual(data['name'], "テストカテゴリ1")
        self.assertEqual(data['description'], "テスト説明1")
        self.assertEqual(data['order'], 1)
        self.assertEqual(data['is_active'], True)

    def test_get_category_not_found(self):
        """存在しないカテゴリの詳細取得APIのテスト"""
        # 存在しないIDでAPIリクエスト
        response = self.client.get('/api/categories/999')
        
        # 404エラーが返されることを確認
        self.assertEqual(response.status_code, 404)

    def test_create_category(self):
        """カテゴリ作成APIのテスト"""
        # 作成前のカテゴリ数を取得
        category_count = Category.objects.count()
        
        # 作成するカテゴリデータ
        category_data = {
            "name": "新しいカテゴリ",
            "description": "新しい説明",
            "image": "",  # 空の文字列を指定
            "order": 3,
            "is_active": True
        }
        
        # APIリクエスト
        response = self.client.post(
            '/api/categories/',
            data=json.dumps(category_data),
            content_type='application/json'
        )
        
        # レスポンスの検証
        self.assertEqual(response.status_code, 201)
        
        # JSONレスポンスをパース
        data = response.json()
        
        # 正しいカテゴリデータが返されることを確認
        self.assertEqual(data['name'], "新しいカテゴリ")
        self.assertEqual(data['description'], "新しい説明")
        self.assertEqual(data['order'], 3)
        self.assertEqual(data['is_active'], True)
        
        # カテゴリが1つ増えていることを確認
        self.assertEqual(Category.objects.count(), category_count + 1)

    def test_create_category_invalid_data(self):
        """不正なデータでカテゴリ作成APIのテスト"""
        # 必須フィールドが欠けているデータ
        category_data = {
            "description": "新しい説明",
            "order": 3,
            "is_active": True
        }
        
        # APIリクエスト
        response = self.client.post(
            '/api/categories/',
            data=json.dumps(category_data),
            content_type='application/json'
        )
        
        # バリデーションエラーが返されることを確認
        self.assertEqual(response.status_code, 422)

    def test_update_category(self):
        """カテゴリ更新APIのテスト"""
        # 更新するカテゴリデータ
        category_data = {
            "name": "更新カテゴリ",
            "description": "更新説明",
            "order": 10,
            "is_active": False
        }
        
        # APIリクエスト
        response = self.client.put(
            f'/api/categories/{self.category1.id}',
            data=json.dumps(category_data),
            content_type='application/json'
        )
        
        # レスポンスの検証
        self.assertEqual(response.status_code, 200)
        
        # JSONレスポンスをパース
        data = response.json()
        
        # 正しく更新されたデータが返されることを確認
        self.assertEqual(data['name'], "更新カテゴリ")
        self.assertEqual(data['description'], "更新説明")
        self.assertEqual(data['order'], 10)
        self.assertEqual(data['is_active'], False)
        
        # データベースのカテゴリも更新されていることを確認
        updated_category = Category.objects.get(id=self.category1.id)
        self.assertEqual(updated_category.name, "更新カテゴリ")
        self.assertEqual(updated_category.description, "更新説明")
        self.assertEqual(updated_category.order, 10)
        self.assertEqual(updated_category.is_active, False)

    def test_update_category_partial(self):
        """カテゴリ部分更新APIのテスト"""
        # 一部のフィールドのみ更新
        category_data = {
            "name": "部分更新カテゴリ"
        }
        
        # APIリクエスト
        response = self.client.put(
            f'/api/categories/{self.category1.id}',
            data=json.dumps(category_data),
            content_type='application/json'
        )
        
        # レスポンスの検証
        self.assertEqual(response.status_code, 200)
        
        # JSONレスポンスをパース
        data = response.json()
        
        # 更新したフィールドのみが変更され、他のフィールドは元の値のままであることを確認
        self.assertEqual(data['name'], "部分更新カテゴリ")
        self.assertEqual(data['description'], "テスト説明1")
        self.assertEqual(data['order'], 1)
        self.assertEqual(data['is_active'], True)

    def test_update_category_not_found(self):
        """存在しないカテゴリの更新APIのテスト"""
        # 更新するカテゴリデータ
        category_data = {
            "name": "更新カテゴリ"
        }
        
        # 存在しないIDでAPIリクエスト
        response = self.client.put(
            '/api/categories/999',
            data=json.dumps(category_data),
            content_type='application/json'
        )
        
        # 404エラーが返されることを確認
        self.assertEqual(response.status_code, 404)

    def test_delete_category(self):
        """カテゴリ削除APIのテスト"""
        # 削除前のカテゴリ数を取得
        category_count = Category.objects.count()
        
        # APIリクエスト
        response = self.client.delete(f'/api/categories/{self.category1.id}')
        
        # レスポンスの検証
        self.assertEqual(response.status_code, 204)
        
        # カテゴリが1つ減っていることを確認
        self.assertEqual(Category.objects.count(), category_count - 1)
        
        # 削除したカテゴリが存在しないことを確認
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=self.category1.id)

    def test_delete_category_not_found(self):
        """存在しないカテゴリの削除APIのテスト"""
        # 存在しないIDでAPIリクエスト
        response = self.client.delete('/api/categories/999')
        
        # 404エラーが返されることを確認
        self.assertEqual(response.status_code, 404)
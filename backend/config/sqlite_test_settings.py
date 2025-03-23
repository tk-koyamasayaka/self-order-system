"""
一時的なSQLiteを使用したテスト用のDjango設定
"""

import os
from .settings import *

# SQLiteデータベースを使用
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

# テスト高速化のための設定
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# テスト時にはデバッグを無効化
DEBUG = False
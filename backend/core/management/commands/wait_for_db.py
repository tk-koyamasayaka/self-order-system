import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """データベースが利用可能になるまで待機するコマンド"""

    help = 'データベースが利用可能になるまで待機します'

    def handle(self, *args, **options):
        self.stdout.write('データベース接続を待機中...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                self.stdout.write(self.style.SUCCESS('データベース接続が確立されました！'))
            except OperationalError:
                self.stdout.write('データベースが利用できません。5秒後に再試行します...')
                time.sleep(5)
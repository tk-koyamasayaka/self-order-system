from ninja import NinjaAPI
from ninja.errors import ValidationError
from django.http import Http404

from api.schemas.common import ErrorResponse

# NinjaAPIインスタンスの作成
api = NinjaAPI(
    title="セルフオーダーシステムAPI",
    description="飲食店向けセルフオーダーシステムのAPI",
    version="1.0.0",
    docs_url="/docs",
)

# エラーハンドラー
@api.exception_handler(Http404)
def handle_not_found(request, exc):
    return api.create_response(request, {"detail": "リソースが見つかりません"}, status=404)

@api.exception_handler(ValidationError)
def handle_validation_error(request, exc):
    return api.create_response(request, {"detail": str(exc)}, status=422)
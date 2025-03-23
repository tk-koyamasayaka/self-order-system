from pydantic import BaseModel


# エラーレスポンススキーマ
class ErrorResponse(BaseModel):
    detail: str
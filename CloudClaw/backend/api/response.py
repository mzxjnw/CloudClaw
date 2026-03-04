from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 200  # 200=成功，非0=失败
    msg: str = "success"  # 中文提示信息
    data: Optional[T] = None  # 返回数据
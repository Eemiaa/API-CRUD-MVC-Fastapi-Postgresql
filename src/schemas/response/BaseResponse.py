from typing import Optional
from pydantic import BaseModel

class BaseResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[str] = None
    datas: Optional[dict] = None

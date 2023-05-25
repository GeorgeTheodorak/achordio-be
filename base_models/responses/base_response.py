from typing import Any, Union, List, Dict
from pydantic import BaseModel, EmailStr
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


class BaseResponse(BaseModel):
    data: Union[List[Dict[str, Any]], Dict[str, Any]]

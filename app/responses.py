"""Success response envelope."""
from typing import Any, Optional

from fastapi.responses import JSONResponse


def success_response(data: Any, message: str, status_code: int = 200,
                     meta: Optional[dict] = None):
    body = {"success": True, "message": message, "data": data}
    if meta is not None:
        body["meta"] = meta
    return JSONResponse(status_code=status_code, content=body)

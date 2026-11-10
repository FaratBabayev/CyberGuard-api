"""Structured error responses. Never expose stack traces or internals."""
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiError(Exception):
    def __init__(self, status_code: int, code: str, message: str,
                 details: Optional[list] = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


def error_response(status_code: int, code: str, message: str,
                   details: Optional[list] = None, headers: Optional[dict] = None):
    error = {"code": code, "message": message}
    if details:  # details only appear for validation errors
        error["details"] = details
    return JSONResponse(status_code=status_code,
                        content={"success": False, "error": error},
                        headers=headers)


async def api_error_handler(request: Request, exc: ApiError):
    return error_response(exc.status_code, exc.code, exc.message, exc.details)


async def request_validation_handler(request: Request, exc: RequestValidationError):
    """Handles invalid query/path parameters."""
    details = []
    for err in exc.errors():
        field = ".".join(str(p) for p in err["loc"] if p not in ("query", "path", "body"))
        details.append({"field": field or "request", "message": err["msg"]})
    return error_response(400, "VALIDATION_ERROR",
                          "The request contains invalid or missing fields.", details)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handles unknown URLs (404) and unsupported methods (405)."""
    if exc.status_code == 404:
        return error_response(404, "NOT_FOUND", "The requested endpoint does not exist.")
    if exc.status_code == 405:
        return error_response(405, "METHOD_NOT_ALLOWED",
                              "This HTTP method is not supported for this endpoint.",
                              headers=exc.headers)
    return error_response(exc.status_code, "ERROR", "The request could not be processed.")


async def unexpected_error_handler(request: Request, exc: Exception):
    return error_response(500, "INTERNAL_ERROR", "An unexpected error occurred.")


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApiError, api_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)

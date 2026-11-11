"""Validation for incident request bodies."""
import ipaddress
from typing import Any

from fastapi import Request

from app.errors import ApiError

SEVERITIES = ("Low", "Medium", "High", "Critical")
STATUSES = ("Open", "Investigating", "Resolved")
ALLOWED_FIELDS = {"title", "description", "severity", "status", "sourceIp"}


def _validation_error(details: list) -> ApiError:
    return ApiError(400, "VALIDATION_ERROR",
                    "The request contains invalid or missing fields.", details)


async def read_json_body(request: Request) -> Any:
    try:
        return await request.json()
    except Exception:
        raise _validation_error(
            [{"field": "body", "message": "Request body must be valid JSON."}])


def validate_incident(body: Any, required: set) -> dict:
    """Checks the body and returns a cleaned dict, or raises a 400 error."""
    if not isinstance(body, dict):
        raise _validation_error(
            [{"field": "body", "message": "Request body must be a JSON object."}])

    errors = []

    for field in body:
        if field not in ALLOWED_FIELDS:
            errors.append({"field": field, "message": "Unknown field."})

    for field in sorted(required):
        if body.get(field) is None:
            errors.append({"field": field, "message": f"{field} is required."})

    title = body.get("title")
    if title is not None and (not isinstance(title, str) or not 3 <= len(title.strip()) <= 100):
        errors.append({"field": "title",
                       "message": "Title must be a string of 3 to 100 characters."})

    description = body.get("description")
    if description is not None and (not isinstance(description, str) or len(description) > 500):
        errors.append({"field": "description",
                       "message": "Description must be a string of at most 500 characters."})

    severity = body.get("severity")
    if severity is not None and severity not in SEVERITIES:
        errors.append({"field": "severity",
                       "message": f"Severity must be one of: {', '.join(SEVERITIES)}."})

    status = body.get("status")
    if status is not None and status not in STATUSES:
        errors.append({"field": "status",
                       "message": f"Status must be one of: {', '.join(STATUSES)}."})

    source_ip = body.get("sourceIp")
    if source_ip is not None:
        try:
            if not isinstance(source_ip, str):
                raise ValueError
            ipaddress.ip_address(source_ip.strip())
        except ValueError:
            errors.append({"field": "sourceIp",
                           "message": "sourceIp must be a valid IPv4 or IPv6 address."})

    if errors:
        raise _validation_error(errors)

    cleaned = {}
    for key, value in body.items():
        if isinstance(value, str) and key in ("title", "description", "sourceIp"):
            value = value.strip()
        cleaned[key] = value
    return cleaned

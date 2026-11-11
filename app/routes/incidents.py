"""CRUD endpoints for the main resource: incidents."""
from datetime import datetime, timezone
from typing import Any, Literal, Optional
from fastapi import APIRouter, Body, Depends, Query
from app.validation import validate_incident
from app.auth import get_current_user
from app.errors import ApiError
from app.mock_data import INCIDENTS, next_id
from app.responses import success_response

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

# Design choice: when a regular user touches another user's incident we return
# 403 Forbidden (clear authorization failure). Set to True to return
# 404 Not Found instead, which hides that the incident exists.
HIDE_FOREIGN_INCIDENTS = False


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def get_allowed_incident(incident_id: str, user: dict) -> dict:
    """Returns the incident or raises 404 (missing) / 403 (not yours)."""
    incident = INCIDENTS.get(incident_id)
    if incident is None:
        raise ApiError(404, "NOT_FOUND", f"Incident '{incident_id}' was not found.")
    if user["role"] != "admin" and incident["ownerId"] != user["id"]:
        if HIDE_FOREIGN_INCIDENTS:
            raise ApiError(404, "NOT_FOUND", f"Incident '{incident_id}' was not found.")
        raise ApiError(403, "FORBIDDEN", "You are not allowed to access this incident.")
    return incident


def check_duplicate(owner_id: str, title: str, source_ip: Optional[str],
                    ignore_id: Optional[str] = None) -> None:
    """409 if the owner already has an unresolved incident with same title and IP."""
    for inc in INCIDENTS.values():
        if (inc["id"] != ignore_id and inc["ownerId"] == owner_id
                and inc["status"] != "Resolved"
                and inc["title"].lower() == title.lower()
                and inc["sourceIp"] == source_ip):
            raise ApiError(409, "CONFLICT",
                           "An unresolved incident with the same title and source IP already exists.")


@router.get("")
async def list_incidents(
    user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1),
    perPage: int = Query(10, ge=1, le=100),
    status: Optional[Literal["Open", "Investigating", "Resolved"]] = None,
    severity: Optional[Literal["Low", "Medium", "High", "Critical"]] = None,
):
    items = [i for i in INCIDENTS.values()
             if user["role"] == "admin" or i["ownerId"] == user["id"]]
    if status:
        items = [i for i in items if i["status"] == status]
    if severity:
        items = [i for i in items if i["severity"] == severity]
    items.sort(key=lambda i: i["id"])

    total = len(items)
    start = (page - 1) * perPage
    return success_response(items[start:start + perPage], "Incidents retrieved successfully.",
                            meta={"total": total, "page": page, "perPage": perPage})


@router.get("/{incident_id}")
async def get_incident(incident_id: str, user: dict = Depends(get_current_user)):
    incident = get_allowed_incident(incident_id, user)
    return success_response(incident, "Incident retrieved successfully.")


@router.post("", status_code=201)
async def create_incident(
    body: Any = Body(...),
    user: dict = Depends(get_current_user)
):
    data = validate_incident(body, required={"title", "severity"})
    status = data.get("status", "Open")
    source_ip = data.get("sourceIp")

    if status != "Resolved":
        check_duplicate(user["id"], data["title"], source_ip)

    incident = {
        "id": next_id(),
        "title": data["title"],
        "description": data.get("description"),
        "severity": data["severity"],
        "status": status,
        "sourceIp": source_ip,
        "ownerId": user["id"],
        "createdAt": now(),
        "updatedAt": now(),
    }

    INCIDENTS[incident["id"]] = incident
    return success_response(
        incident, "Incident created successfully.", status_code=201
    )

@router.put("/{incident_id}")
async def update_incident(
    incident_id: str,
    body: Any = Body(...),
    user: dict = Depends(get_current_user)
):
    incident = get_allowed_incident(incident_id, user)
    data = validate_incident(body, required={"title", "severity", "status"})

    if data["status"] != "Resolved":
        check_duplicate(
            incident["ownerId"],
            data["title"],
            data.get("sourceIp"),
            ignore_id=incident_id
        )

    incident.update({
        "title": data["title"],
        "description": data.get("description"),
        "severity": data["severity"],
        "status": data["status"],
        "sourceIp": data.get("sourceIp"),
        "updatedAt": now(),
    })

    return success_response(incident, "Incident updated successfully.")

@router.delete("/{incident_id}")
async def delete_incident(incident_id: str, user: dict = Depends(get_current_user)):
    get_allowed_incident(incident_id, user)
    del INCIDENTS[incident_id]
    return success_response(None, "Incident deleted successfully.")

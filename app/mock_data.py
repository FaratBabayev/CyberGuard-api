"""In-memory mock data. It resets every time the server restarts."""
from copy import deepcopy

SEED = {
    "inc_101": {
        "id": "inc_101",
        "title": "Brute force attempt on SSH",
        "description": "6 failed logins from one IP within 2 minutes.",
        "severity": "High",
        "status": "Open",
        "sourceIp": "203.0.113.10",
        "ownerId": "user-a",
        "createdAt": "2026-11-01T09:15:00Z",
        "updatedAt": "2026-11-01T09:15:00Z",
    },
    "inc_102": {
        "id": "inc_102",
        "title": "Invalid user probing",
        "description": "Many attempts with usernames that do not exist.",
        "severity": "Medium",
        "status": "Resolved",
        "sourceIp": "198.51.100.23",
        "ownerId": "user-a",
        "createdAt": "2026-11-02T14:40:00Z",
        "updatedAt": "2026-11-03T08:00:00Z",
    },
    "inc_103": {
        "id": "inc_103",
        "title": "Root login attempts",
        "description": "Repeated attempts to log in as root.",
        "severity": "Critical",
        "status": "Investigating",
        "sourceIp": "192.0.2.44",
        "ownerId": "user-b",
        "createdAt": "2026-11-03T22:05:00Z",
        "updatedAt": "2026-11-04T07:30:00Z",
    },
    "inc_104": {
        "id": "inc_104",
        "title": "Password spraying across accounts",
        "description": "One IP tried the same password on many accounts.",
        "severity": "High",
        "status": "Open",
        "sourceIp": "203.0.113.77",
        "ownerId": "user-b",
        "createdAt": "2026-11-05T11:20:00Z",
        "updatedAt": "2026-11-05T11:20:00Z",
    },
    "inc_105": {
        "id": "inc_105",
        "title": "Unusual login time for admin account",
        "description": None,
        "severity": "Low",
        "status": "Open",
        "sourceIp": None,
        "ownerId": "admin",
        "createdAt": "2026-11-06T03:10:00Z",
        "updatedAt": "2026-11-06T03:10:00Z",
    },
}

INCIDENTS: dict = {}
_counter = {"next": 106}


def reset_data() -> None:
    """Restore the initial mock data (used at startup and in tests)."""
    INCIDENTS.clear()
    INCIDENTS.update(deepcopy(SEED))
    _counter["next"] = 106


def next_id() -> str:
    new_id = f"inc_{_counter['next']}"
    _counter["next"] += 1
    return new_id


reset_data()

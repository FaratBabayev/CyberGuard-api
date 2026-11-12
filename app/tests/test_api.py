import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.mock_data import reset_data

client = TestClient(app)


def auth(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def fresh_data():
    reset_data()


def test_greeting_is_html():
    r = client.get("/api/v1/greeting")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "CyberGuard" in r.text


def test_missing_token_returns_401():
    r = client.get("/api/v1/incidents")
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "UNAUTHORIZED"


def test_invalid_token_returns_401():
    r = client.get("/api/v1/incidents", headers=auth("wrong-token"))
    assert r.status_code == 401


def test_user_sees_only_own_incidents():
    r = client.get("/api/v1/incidents", headers=auth("user-a-token"))
    body = r.json()
    assert r.status_code == 200
    assert body["meta"]["total"] == 2
    assert all(i["ownerId"] == "user-a" for i in body["data"])


def test_admin_sees_all_incidents():
    r = client.get("/api/v1/incidents", headers=auth("admin-token"))
    assert r.json()["meta"]["total"] == 5


def test_user_cannot_read_other_users_incident():
    r = client.get("/api/v1/incidents/inc_103", headers=auth("user-a-token"))
    assert r.status_code == 403


def test_admin_can_read_any_incident():
    r = client.get("/api/v1/incidents/inc_103", headers=auth("admin-token"))
    assert r.status_code == 200


def test_nonexistent_incident_returns_404():
    r = client.get("/api/v1/incidents/inc_999", headers=auth("user-a-token"))
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "NOT_FOUND"


def test_create_incident():
    payload = {"title": "Suspicious sudo usage", "severity": "Medium",
               "sourceIp": "10.0.0.5"}
    r = client.post("/api/v1/incidents", json=payload, headers=auth("user-a-token"))
    assert r.status_code == 201
    data = r.json()["data"]
    assert data["ownerId"] == "user-a" and data["status"] == "Open"


def test_create_validation_errors():
    r = client.post("/api/v1/incidents",
                    json={"title": "ab", "severity": "Huge", "color": "red"},
                    headers=auth("user-a-token"))
    assert r.status_code == 400
    fields = {d["field"] for d in r.json()["error"]["details"]}
    assert {"title", "severity", "color"} <= fields


def test_create_invalid_json_returns_400():
    r = client.post("/api/v1/incidents", content="not json",
                    headers={**auth("user-a-token"), "Content-Type": "application/json"})
    assert r.status_code == 400


def test_duplicate_incident_returns_409():
    payload = {"title": "Brute force attempt on SSH", "severity": "High",
               "sourceIp": "203.0.113.10"}
    r = client.post("/api/v1/incidents", json=payload, headers=auth("user-a-token"))
    assert r.status_code == 409


def test_update_own_incident():
    payload = {"title": "Brute force attempt on SSH", "severity": "Critical",
               "status": "Investigating", "sourceIp": "203.0.113.10"}
    r = client.put("/api/v1/incidents/inc_101", json=payload, headers=auth("user-a-token"))
    assert r.status_code == 200
    assert r.json()["data"]["severity"] == "Critical"


def test_user_cannot_update_other_users_incident():
    payload = {"title": "Hacked title", "severity": "Low", "status": "Open"}
    r = client.put("/api/v1/incidents/inc_103", json=payload, headers=auth("user-a-token"))
    assert r.status_code == 403


def test_update_requires_all_main_fields():
    r = client.put("/api/v1/incidents/inc_101", json={"title": "Only title"},
                   headers=auth("user-a-token"))
    assert r.status_code == 400


def test_user_cannot_delete_other_users_incident():
    r = client.delete("/api/v1/incidents/inc_101", headers=auth("user-b-token"))
    assert r.status_code == 403


def test_delete_own_then_404():
    r = client.delete("/api/v1/incidents/inc_101", headers=auth("user-a-token"))
    assert r.status_code == 200 and r.json()["data"] is None
    r = client.get("/api/v1/incidents/inc_101", headers=auth("user-a-token"))
    assert r.status_code == 404


def test_admin_can_delete_any_incident():
    r = client.delete("/api/v1/incidents/inc_104", headers=auth("admin-token"))
    assert r.status_code == 200


def test_unsupported_method_returns_405():
    r = client.patch("/api/v1/incidents/inc_101", json={}, headers=auth("user-a-token"))
    assert r.status_code == 405
    assert r.json()["error"]["code"] == "METHOD_NOT_ALLOWED"


def test_invalid_query_parameter_returns_400():
    r = client.get("/api/v1/incidents?perPage=0", headers=auth("user-a-token"))
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "VALIDATION_ERROR"

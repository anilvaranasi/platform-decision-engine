import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_list_platforms_endpoint():
    res = client.get("/platforms")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 4

def test_decide_endpoint():
    payload = {
        "initiative_name": "API Onboarding Test",
        "domain": "HR",
        "capability": "hr.onboarding",
        "intent": "optimize_existing"
    }
    res = client.post("/decide", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["decision_type"] == "rule_matched"
    assert len(data["stages"]) == 3
    assert data["stages"][0]["platform_id"] == "green_platform"
    assert data["stages"][1]["platform_id"] == "purple_platform"

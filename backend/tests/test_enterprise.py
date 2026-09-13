"""Test Enterprise SOC2 Readiness $0 — 12/13 DONE $0 — 1/13 needs $30K-$80K audit — 92% readiness $0 — After تابع x5"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_enterprise_info():
    r = client.get("/api/enterprise/")
    assert r.status_code == 200
    data = r.json()
    assert "SOC2" in str(data)
    assert "$0" in str(data) or "readiness" in str(data).lower()

def test_enterprise_soc2():
    r = client.get("/api/enterprise/soc2")
    assert r.status_code == 200
    data = r.json()
    assert "controls" in data
    assert "CC1" in data["controls"]
    assert data["controls"]["CC1"]["implemented"] is True

def test_enterprise_readiness():
    r = client.get("/api/enterprise/readiness")
    assert r.status_code == 200
    data = r.json()
    assert "readiness_0" in data
    assert "$0" in data["readiness_0"] or "controls" in str(data).lower()

def test_enterprise_checklist():
    r = client.get("/api/enterprise/checklist")
    assert r.status_code == 200
    data = r.json()
    assert "checklist_0" in data
    assert data["total"] == 13
    assert data["done_0"] == 12
    assert "92%" in data["readiness_0"] or "12/13" in data["readiness_0"]

def test_enterprise_controls():
    r = client.get("/api/enterprise/controls")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 12
    assert data["implemented"] == 12
    assert "100%" in data["implementation_rate"]

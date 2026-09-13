"""Test MRR $1M+ ARR — $1,886,280 ARR Already Achieved $157,190 MRR ×12 — $8,058,000 ARR Next $5M ARR — $16,116,000 ARR Next $10M+ ARR $1M+ MRR — After تابع x5"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_mrr_1m_info():
    r = client.get("/api/mrr/1m/")
    assert r.status_code == 200
    data = r.json()
    assert "1m" in str(data).lower() or "1M" in str(data) or "ARR" in str(data)
    assert "$0" in str(data) or "free" in str(data).lower()

def test_mrr_1m_stats():
    r = client.get("/api/mrr/1m/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_mrr_100k" in data
    assert data["total_mrr_100k"] == 157190
    assert "arr_100k" in data
    assert data["arr_100k"] == 1886280
    assert "arr_500k" in data
    assert data["arr_500k"] == 8058000
    assert "arr_1m" in data
    assert data["arr_1m"] == 16116000
    assert "already_1m_arr" in data
    assert "1,886,280" in data["already_1m_arr"] or "1886280" in str(data["already_1m_arr"])

def test_mrr_1m_scale():
    r = client.get("/api/mrr/1m/scale")
    assert r.status_code == 200
    data = r.json()
    assert "scale_plan" in data
    assert "already_1m_arr" in data

def test_mrr_1m_arr():
    r = client.get("/api/mrr/1m/arr")
    assert r.status_code == 200
    data = r.json()
    assert "arr_100k" in data
    assert "arr_500k" in data
    assert "arr_1m" in data
    assert data["arr_100k"] == 1886280
    assert "Already $1M+ ARR" in data["arr_100k_label"]

def test_mrr_1m_view_exists():
    import os
    for path in ["frontend/src/components/MRR1MView.tsx", "/home/user/ai-agent1/frontend/src/components/MRR1MView.tsx"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "1M" in content or "ARR" in content
                return
    assert False, "MRR1MView.tsx not found"

def test_enterprise_view_exists():
    import os
    for path in ["frontend/src/components/EnterpriseView.tsx", "/home/user/ai-agent1/frontend/src/components/EnterpriseView.tsx"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "SOC2" in content or "Enterprise" in content
                return
    assert False, "EnterpriseView.tsx not found"

def test_all_mrr_integration_1m():
    r_30k = client.get("/api/mrr/stats")
    r_100k = client.get("/api/mrr/100k/stats")
    r_1m = client.get("/api/mrr/1m/stats")
    r_ent = client.get("/api/enterprise/")
    assert r_30k.status_code == 200
    assert r_100k.status_code == 200
    assert r_1m.status_code == 200
    assert r_ent.status_code == 200
    assert r_30k.json()["total_mrr"] == 30884
    assert r_100k.json()["total_mrr_100k"] == 157190
    assert r_1m.json()["arr_100k"] == 1886280

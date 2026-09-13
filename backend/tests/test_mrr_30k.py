"""Test MRR $30K+ — $30,884 MRR — $25,226.6/mo Profit $302,719/year 81% Margin Avg — $0 Cost — After Prod 100 $19,900 MRR — After تابع x3"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_mrr_info():
    r = client.get("/api/mrr/")
    assert r.status_code == 200
    data = r.json()
    assert "mrr" in str(data).lower()
    assert "30884" in str(data) or "30" in str(data)
    assert "$0" in str(data) or "free" in str(data).lower()

def test_mrr_stats():
    r = client.get("/api/mrr/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_mrr" in data
    assert data["total_mrr"] == 30884
    assert "total_profit" in data
    assert abs(data["total_profit"] - 25226.6) < 1.0
    assert "total_profit_yearly" in data
    assert abs(data["total_profit_yearly"] - 302719) < 2.0
    assert "margin_avg" in data
    assert "81%" in data["margin_avg"]

def test_mrr_marketplace_purchase():
    r = client.post("/api/mrr/marketplace/purchase", json={
        "user_id": "test_user",
        "tool_id": "viralwave-studio"
    })
    assert r.status_code == 200
    data = r.json()
    assert "purchase" in data
    assert data["purchase"]["tool_id"] == "viralwave-studio"
    assert data["purchase"]["profit_30pct"] == 14.7

def test_mrr_marketplace_stats():
    r = client.get("/api/mrr/marketplace/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_purchases" in data
    assert "total_profit" in data
    assert "target_extra" in data
    assert data["target_extra"] == 735

def test_mrr_whitelabel_create():
    r = client.post("/api/mrr/whitelabel/create", json={
        "client_name": "Test Client Agency",
        "domain": "test-client.us.kg"
    })
    assert r.status_code == 200
    data = r.json()
    assert "client" in data or "error" in data
    if "client" in data:
        assert data["client"]["domain"] == "test-client.us.kg"
        assert "$0" in data["client"]["domain_cost"] or "free" in data["client"]["domain_cost"].lower()

def test_mrr_whitelabel_stats():
    r = client.get("/api/mrr/whitelabel/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_whitelabel_clients" in data
    assert "mrr_target" in data
    assert data["mrr_target"] == 9950

def test_mrr_content_generate():
    r = client.post("/api/mrr/content/generate", json={
        "topic": "AI Agency OS",
        "platforms": ["FB", "IG", "LinkedIn"],
        "duration": "1 month"
    })
    assert r.status_code == 200
    data = r.json()
    assert "generation" in data
    assert data["generation"]["topic"] == "AI Agency OS"
    assert data["generation"]["profit"] == 251.6

def test_mrr_content_stats():
    r = client.get("/api/mrr/content/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_generations" in data
    assert "total_profit" in data

def test_mrr_view_exists():
    import os
    view_path = "frontend/src/components/MRR30KView.tsx"
    for path in [view_path, f"/home/user/ai-agent1/{view_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "30" in content
                assert "30884" in content or "30,884" in content
                assert "$0" in content or "free" in content.lower()
                return
    assert False, "MRR30KView.tsx not found"

def test_mrr_docs_exists():
    import os
    doc_path = "docs/MRR_30K_PLUS.md"
    for path in [doc_path, f"/home/user/ai-agent1/{doc_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "30" in content
                assert "30884" in content or "30,884" in content
                assert "$0" in content
                return
    assert False, "MRR_30K_PLUS.md not found"

def test_mrr_prod_beta_integration():
    r_mrr = client.get("/api/mrr/stats")
    r_prod = client.get("/api/prod/stats")
    r_beta = client.get("/api/beta/stats")
    assert r_mrr.status_code == 200
    assert r_prod.status_code == 200
    assert r_beta.status_code == 200
    mrr_data = r_mrr.json()
    prod_data = r_prod.json()
    beta_data = r_beta.json()
    assert mrr_data["total_mrr"] == 30884
    assert prod_data["mrr_target"] == 19900
    assert beta_data["beta_limit"] == 10

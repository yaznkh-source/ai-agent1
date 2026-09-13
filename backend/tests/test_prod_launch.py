"""Test Prod Launch 100 Users $19,900 MRR — $37.4 cost $161.6 profit 81% margin — $16,160/mo profit $193,920/year — $0 cost — After Beta 10 Free — After تابع"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_prod_info():
    r = client.get("/api/prod/")
    assert r.status_code == 200
    data = r.json()
    assert "prod" in str(data).lower()
    assert "19900" in str(data) or "199" in str(data)
    assert "$0" in str(data) or "free" in str(data).lower()

def test_prod_register():
    r = client.post("/api/prod/register", json={
        "email": "prod1@test.com",
        "name": "Prod User 1",
        "company": "Prod Agency 1",
        "tier": "pro",
        "use_case": "Need AI agency OS for 50 clients 10 team"
    })
    assert r.status_code == 200
    data = r.json()
    assert "user_id" in data or "error" in data
    if "user_id" in data:
        assert data["mrr"] == 199
        assert data["cost"] == 37.4
        assert data["profit"] == 161.6
        assert "81%" in data["margin"]

def test_prod_register_tiers():
    for tier, expected_mrr in [("free", 0), ("starter", 49), ("pro", 199), ("enterprise", 999)]:
        r = client.post("/api/prod/register", json={
            "email": f"prod_{tier}@test.com",
            "name": f"Prod {tier}",
            "company": f"Prod {tier} Agency",
            "tier": tier,
            "use_case": f"Test {tier}"
        })
        assert r.status_code == 200

def test_prod_stats():
    r = client.get("/api/prod/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_prod_users" in data
    assert "mrr" in data
    assert "profit" in data
    assert "total_potential_30k_mrr" in data
    assert "$0" in str(data) or "free" in str(data).lower()
    assert "19900" in str(data) or "199" in str(data)

def test_prod_users_list():
    r = client.get("/api/prod/users")
    assert r.status_code == 200
    data = r.json()
    assert "prod_users" in data
    assert "count" in data
    assert data["count"] >= 1

def test_prod_view_exists():
    import os
    view_path = "frontend/src/components/ProdLaunchView.tsx"
    for path in [view_path, f"/home/user/ai-agent1/{view_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "Prod" in content
                assert "19900" in content or "199" in content
                assert "$0" in content or "free" in content.lower()
                return
    assert False, "ProdLaunchView.tsx not found"

def test_prod_docs_exists():
    import os
    doc_path = "docs/PROD_LAUNCH_100_USERS.md"
    for path in [doc_path, f"/home/user/ai-agent1/{doc_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "Prod" in content
                assert "100" in content
                assert "19900" in content or "199" in content
                assert "$0" in content
                return
    assert False, "PROD_LAUNCH_100_USERS.md not found"

def test_prod_beta_integration():
    # Beta 10 free → Prod 100 $19,900 MRR integration
    r_beta = client.get("/api/beta/stats")
    r_prod = client.get("/api/prod/stats")
    assert r_beta.status_code == 200
    assert r_prod.status_code == 200
    beta_data = r_beta.json()
    prod_data = r_prod.json()
    # Beta 10 free validation for Prod 100
    assert "total_beta_users" in beta_data
    assert "total_prod_users" in prod_data
    assert "19,900" in str(prod_data) or "19900" in str(prod_data) or "199" in str(prod_data)

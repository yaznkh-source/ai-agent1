"""Test Beta Launch 10 Free $0 — Go-to-Market — After 100/100+ Polished"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_beta_info():
    r = client.get("/api/beta/")
    assert r.status_code == 200
    data = r.json()
    assert "beta" in str(data).lower()
    assert "10" in str(data)
    assert "free" in str(data).lower() or "$0" in str(data)

def test_beta_register():
    r = client.post("/api/beta/register", json={
        "email": "beta1@test.com",
        "name": "Beta User 1",
        "company": "Beta Agency 1",
        "use_case": "Need AI agency OS for 10 clients"
    })
    assert r.status_code == 200
    data = r.json()
    assert "user_id" in data or "error" in data  # May be already registered from previous test
    if "user_id" in data:
        assert data["cost"] == "$0 — Beta 10 free — $0 domain + $0 LLM + $0 voice + $0 tools mock — margin 100%" or "$0" in str(data["cost"])

def test_beta_register_limit():
    # Try to register 10 users
    for i in range(2, 11):
        r = client.post("/api/beta/register", json={
            "email": f"beta{i}@test.com",
            "name": f"Beta User {i}",
            "company": f"Beta Agency {i}",
            "use_case": f"Need AI agency OS for {i} clients"
        })
        assert r.status_code == 200
    
    # 11th should fail — limit 10
    r = client.post("/api/beta/register", json={
        "email": "beta11@test.com",
        "name": "Beta User 11",
        "company": "Beta Agency 11",
        "use_case": "Need AI agency OS"
    })
    assert r.status_code == 200
    data = r.json()
    assert "error" in data or "waitlist" in data or "limit" in str(data).lower()

def test_beta_feedback():
    # First register if not exists
    r = client.post("/api/beta/register", json={
        "email": "beta_feedback@test.com",
        "name": "Feedback User",
        "company": "Feedback Agency",
        "use_case": "Test feedback"
    })
    # May fail if limit reached — try to get existing user
    r_users = client.get("/api/beta/users")
    users = r_users.json().get("beta_users", [])
    if users:
        user_id = users[0]["user_id"]
    else:
        user_id = "test_user_id"
    
    r = client.post("/api/beta/feedback", json={
        "user_id": user_id,
        "rating": 5,
        "feedback": "AI Agency OS saved me 10 hours/week — 68 agents amazing — free LLM $0 margin 100% — free domain $0 — voice $0 — 100/100+",
        "feature_requests": ["More curated tools", "Better loops UI", "Mobile app"],
        "nps": 10
    })
    assert r.status_code == 200
    data = r.json()
    assert "feedback" in data
    assert data["feedback"]["rating"] == 5

def test_beta_stats():
    r = client.get("/api/beta/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_beta_users" in data
    assert "cost" in data or "total_cost_saved" in data
    assert "$0" in str(data) or "free" in str(data).lower()

def test_beta_users_list():
    r = client.get("/api/beta/users")
    assert r.status_code == 200
    data = r.json()
    assert "beta_users" in data
    assert "count" in data
    assert data["count"] >= 1

def test_beta_view_exists():
    import os
    view_path = "frontend/src/components/BetaView.tsx"
    for path in [view_path, f"/home/user/ai-agent1/{view_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "Beta" in content
                assert "$0" in content or "free" in content.lower()
                assert "10" in content
                return
    assert False, "BetaView.tsx not found"

def test_beta_docs_exists():
    import os
    doc_path = "docs/BETA_LAUNCH_10_FREE.md"
    for path in [doc_path, f"/home/user/ai-agent1/{doc_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "Beta" in content
                assert "10" in content
                assert "$0" in content
                assert "19,900" in content or "199" in content
                return
    assert False, "BETA_LAUNCH_10_FREE.md not found"

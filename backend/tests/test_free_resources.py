"""Test Free Resources Integration - D1 FreeDomain, D2 Curated Tools, D3 Free LLM, D4 Loops - 10 tests"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_free_domain_info():
    r = client.get("/api/domain/free/")
    assert r.status_code == 200
    data = r.json()
    assert "us.kg" in str(data).lower() or "dpdns.org" in str(data).lower()
    assert "199k" in str(data) or "FreeDomain" in str(data)

def test_free_domain_check():
    r = client.get("/api/domain/free/check/ai-agency-os")
    assert r.status_code == 200
    data = r.json()
    assert "available" in data

def test_free_domain_guide():
    r = client.get("/api/domain/free/guide")
    assert r.status_code == 200
    data = r.json()
    assert "steps" in data
    assert len(data["steps"]) >= 5

def test_curated_tools_info():
    r = client.get("/api/tools/curated/")
    assert r.status_code == 200
    data = r.json()
    assert "tools" in str(data).lower()
    assert "viralwave" in str(data).lower() or "ViralWave" in str(data)

def test_curated_tools_list():
    r = client.get("/api/tools/curated/list")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 5
    assert "tools" in data

def test_curated_tools_featured():
    r = client.get("/api/tools/curated/featured")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 1

def test_free_llm_info():
    r = client.get("/api/llm/")
    assert r.status_code == 200
    data = r.json()
    assert "nvidia_nim" in str(data).lower() or "free" in str(data).lower()
    assert "providers" in data

def test_free_llm_providers():
    r = client.get("/api/llm/providers")
    assert r.status_code == 200
    data = r.json()
    assert "providers" in data

def test_loops_info():
    r = client.get("/api/loops/")
    assert r.status_code == 200
    data = r.json()
    assert "loopx" in str(data).lower() or "loops" in str(data).lower()
    assert "goals" in str(data).lower()

def test_loops_goals_crud():
    # Create goal
    r = client.post("/api/loops/goals", json={"title": "Test Goal Free Resources", "description": "Test", "owner": "user"})
    assert r.status_code == 200
    data = r.json()
    assert "goal" in data
    goal_id = data["goal"]["id"]
    
    # List goals
    r = client.get("/api/loops/goals")
    assert r.status_code == 200
    assert r.json()["count"] >= 1
    
    # Get goal
    r = client.get(f"/api/loops/goals/{goal_id}")
    assert r.status_code == 200
    
    # Create todo
    r = client.post(f"/api/loops/goals/{goal_id}/todos", json={"title": "Test Todo", "assignee": "backend-dev"})
    assert r.status_code == 200
    todo_id = r.json()["todo"]["id"]
    
    # Complete todo
    r = client.post(f"/api/loops/todos/{todo_id}/complete", json={"evidence": "Done"})
    assert r.status_code == 200
    
    # Create gate
    r = client.post(f"/api/loops/goals/{goal_id}/gates", json={"type": "owner", "description": "Owner approval"})
    assert r.status_code == 200
    gate_id = r.json()["gate"]["id"]
    
    # Approve gate
    r = client.post(f"/api/loops/gates/{gate_id}/approve", json={"reviewer": "user"})
    assert r.status_code == 200
    
    # Status
    r = client.get("/api/loops/status")
    assert r.status_code == 200
    
    r = client.get(f"/api/loops/status/{goal_id}")
    assert r.status_code == 200
    
    # Evidence
    r = client.get("/api/loops/evidence")
    assert r.status_code == 200
    
    r = client.get(f"/api/loops/evidence/{goal_id}")
    assert r.status_code == 200

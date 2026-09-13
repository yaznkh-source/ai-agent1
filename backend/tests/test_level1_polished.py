"""Test Level 1 Polished $0 — Voice Whisper + Loops Persistence + Grafana + Backup Postgres + Load 20 users"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_voice_info():
    r = client.get("/api/voice/")
    assert r.status_code == 200
    data = r.json()
    assert "whisper" in str(data).lower()
    assert "free" in str(data).lower() or "$0" in str(data)

def test_voice_transcribe_mock():
    # Test mock transcription — upload fake audio
    import io
    fake_audio = io.BytesIO(b"fake audio content for testing whisper local free $0")
    r = client.post("/api/voice/transcribe", files={"file": ("test.mp3", fake_audio, "audio/mpeg")}, data={"model": "base", "language": "auto"})
    assert r.status_code == 200
    data = r.json()
    assert "transcription" in data
    assert data["cost"] == 0.0
    assert "100%" in data["margin"]

def test_loops_persistence_file():
    # Test loops persistence to file $0 — Level 1 Polished
    r = client.post("/api/loops/goals", json={"title": "Persistence Test Goal", "description": "Test file persistence $0", "owner": "user"})
    assert r.status_code == 200
    goal_id = r.json()["goal"]["id"]
    
    # Check file exists
    import os
    persist_file = os.getenv("LOOPS_PERSIST_FILE", "/tmp/ai-agency-loops.json")
    assert os.path.exists(persist_file), f"Persist file {persist_file} should exist — Level 1 Polished $0"
    
    # Check file content
    import json
    with open(persist_file, 'r') as f:
        data = json.load(f)
        assert "goals" in data
        assert len(data["goals"]) >= 1

def test_grafana_dashboard_exists():
    import os, json
    dashboard_path = "grafana/dashboards/ai-agency-os.json"
    # Try both relative and absolute
    for path in [dashboard_path, f"/home/user/ai-agent1/{dashboard_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                assert "dashboard" in data
                assert "panels" in data["dashboard"]
                assert len(data["dashboard"]["panels"]) >= 5
                return
    assert False, f"Grafana dashboard {dashboard_path} not found — Level 1 Polished $0"

def test_backup_cron_postgres():
    import os
    cron_path = "scripts/backup-cron.sh"
    for path in [cron_path, f"/home/user/ai-agent1/{cron_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "pg_dump" in content, "backup-cron.sh should contain pg_dump — Level 1 Polished $0"
                assert "postgres" in content.lower()
                assert "redis" in content.lower() or "rdb" in content.lower()
                assert "sqlite" in content.lower()
                return
    assert False, f"backup-cron.sh not found"

def test_locustfile_exists():
    import os
    locust_path = "locustfile.py"
    for path in [locust_path, f"/home/user/ai-agent1/{locust_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "HttpUser" in content
                assert "20" in content or "users" in content.lower()
                assert "free" in content.lower() or "domain" in content.lower() or "llm" in content.lower()
                return
    assert False, "locustfile.py not found — Level 1 Polished $0"

def test_database_models_goals():
    from app.core.database import GoalModel, TodoModel, GateModel, EvidenceModel
    # Check models exist
    assert GoalModel.__tablename__ == "goals"
    assert TodoModel.__tablename__ == "todos"
    assert GateModel.__tablename__ == "gates"
    assert EvidenceModel.__tablename__ == "evidence"
    
    # Check columns
    assert hasattr(GoalModel, "title")
    assert hasattr(GoalModel, "status")
    assert hasattr(GoalModel, "quota_used")
    assert hasattr(TodoModel, "goal_id")
    assert hasattr(GateModel, "type")
    assert hasattr(EvidenceModel, "content")

def test_voice_view_exists():
    import os
    view_path = "frontend/src/components/VoiceView.tsx"
    for path in [view_path, f"/home/user/ai-agent1/{view_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                assert "Whisper" in content
                assert "$0" in content or "free" in content.lower()
                return
    assert False, "VoiceView.tsx not found"

def test_frontend_build_views_count():
    import os, json
    # Check App.tsx has 31+ views now (was 26, now 31 with free-domain free-llm loops curated-tools voice)
    app_path = "frontend/src/App.tsx"
    for path in [app_path, f"/home/user/ai-agent1/{app_path}"]:
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
                # Count cases
                case_count = content.count("case '")
                assert case_count >= 31, f"App.tsx should have >=31 views, got {case_count} — Level 1 Polished + voice"
                assert "voice" in content.lower()
                assert "free-domain" in content.lower()
                assert "free-llm" in content.lower()
                assert "loops" in content.lower()
                return
    assert False, "App.tsx not found"

def test_free_domain_enhanced():
    r = client.get("/api/domain/free/")
    assert r.status_code == 200
    data = r.json()
    # Should have 5 extensions
    assert len(data.get("extensions", {})) >= 4
    # Should have quick_start 5 steps
    assert len(data.get("quick_start", {})) >= 4

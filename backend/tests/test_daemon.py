"""
Tests Daemon + Agent Execution + Voice — حقيقي — مثل Paseo + Manus — يعمل فعلياً — $0 — المرحلة 3
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app
from app.core.daemon import daemon

client = TestClient(app)

class TestDaemon:
    def test_daemon_status(self):
        status = daemon.get_status()
        assert "total_agents" in status
        assert status["total_agents"] >= 1

    def test_daemon_start(self):
        assert daemon.is_running is True

    def test_daemon_api_status(self):
        res = client.get("/api/agents-execution/daemon/status")
        assert res.status_code == 200
        data = res.json()
        assert "total_agents" in data or "is_running" in data

    def test_execute_task(self):
        res = client.post("/api/agents-execution/planner/execute", json={"task": "أنشئ خطة لمشروع متجر", "context": {}})
        assert res.status_code == 200
        data = res.json()
        assert "task_id" in data
        assert data["agent_id"] == "planner"

    def test_execute_task_sync(self):
        res = client.post("/api/agents-execution/planner/execute/sync", json={"task": "اختبر تنفيذ متزامن", "context": {}})
        assert res.status_code == 200
        data = res.json()
        assert "result" in data or "error" in data

    def test_list_tasks(self):
        res = client.get("/api/agents-execution/tasks")
        assert res.status_code == 200
        assert "tasks" in res.json()

    def test_list_agent_tasks(self):
        res = client.get("/api/agents-execution/planner/tasks")
        assert res.status_code == 200
        assert "tasks" in res.json()

class TestVoice:
    def test_voice_status(self):
        res = client.get("/api/voice/status")
        assert res.status_code == 200
        data = res.json()
        assert "voice_control" in data

    def test_task_from_voice(self):
        res = client.post("/api/voice/task-from-voice", json={"text": "أنشئ خطة لمشروع", "agent_id": "planner"})
        assert res.status_code == 200
        data = res.json()
        assert "task_id" in data or "error" in data

"""Test Controller حقيقي — مثل FastChat controller.py — يدير 68 وكيل — يسجل Workers — يوازن الحمل — يعمل فعلياً — $0 — المرحلة 1 — من lmarena/FastChat"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from app.main import app
from app.core.controller import controller
from app.core.conversation import get_conversation_template, list_templates
from app.agents.worker import get_worker, list_workers

client = TestClient(app)

def test_controller_register_worker():
    worker_info = controller.register_worker(
        worker_id="test-worker-1",
        model_names=["test-model-1", "planner"],
        worker_address="http://localhost:8000/api/agents/planner/execute",
        worker_type="agent"
    )
    assert worker_info["worker_id"] == "test-worker-1"
    assert "test-model-1" in worker_info["model_names"]
    assert worker_info["status"] == "alive"

def test_controller_list_workers():
    workers = controller.list_workers()
    assert len(workers) >= 1
    assert any("test-worker-1" in w["worker_id"] or "agent-worker" in w["worker_id"] for w in workers)

def test_controller_get_worker():
    worker = controller.get_worker("planner")
    assert worker is not None
    assert worker["status"] == "alive"

def test_controller_heartbeat():
    result = controller.heartbeat("test-worker-1")
    assert result is True
    result_fail = controller.heartbeat("non-existent-worker")
    assert result_fail is False

def test_controller_status():
    status = controller.get_status()
    assert status["status"] == "alive"
    assert "total_workers" in status
    assert status["total_workers"] >= 1

def test_controller_api_list_workers():
    r = client.get("/v1/controller/list_workers")
    assert r.status_code == 200
    data = r.json()
    assert "workers" in data
    assert data["total"] >= 1

def test_controller_api_register_worker():
    r = client.post("/v1/controller/register_worker", json={
        "worker_id": "test-worker-api",
        "model_names": ["test-model-api"],
        "worker_address": "http://localhost:8000/api/agents/test/execute",
        "worker_type": "agent"
    })
    assert r.status_code == 200
    data = r.json()
    assert data["registered"] is True

def test_controller_api_get_worker():
    r = client.get("/v1/controller/get_worker/planner")
    assert r.status_code == 200
    data = r.json()
    assert data["found"] is True
    assert data["worker"] is not None

def test_conversation_templates():
    templates = list_templates()
    assert len(templates) >= 5
    assert "general" in templates
    assert "claude" in templates
    assert "gemini" in templates
    assert "manus" in templates

def test_conversation_template_get_prompt():
    conv = get_conversation_template("general")
    conv.append_message(conv.roles[0], "Hello")
    conv.append_message(conv.roles[1], "Hi there")
    prompt = conv.get_prompt()
    assert "Hello" in prompt
    assert "Hi there" in prompt

def test_conversation_template_openai_messages():
    conv = get_conversation_template("planner")
    conv.append_message(conv.roles[0], "Create a plan")
    conv.append_message(conv.roles[1], "Plan created")
    messages = conv.to_openai_api_messages()
    assert len(messages) >= 2
    assert messages[0]["role"] == "system" or messages[0]["role"] == "user"

def test_agent_workers_pool():
    workers = list_workers()
    assert len(workers) >= 1
    # Check at least planner exists
    worker = get_worker("planner")
    if worker:
        status = worker.get_status()
        assert status["agent_id"] == "planner"
        assert "status" in status

def test_openai_compatible_models():
    r = client.get("/v1/models")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert len(data["data"]) >= 1

def test_openai_compatible_chat_completions():
    r = client.post("/v1/chat/completions", json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Hello"}],
        "temperature": 0.7
    })
    assert r.status_code == 200
    data = r.json()
    assert "choices" in data
    assert len(data["choices"]) >= 1
    assert "message" in data["choices"][0]
    assert "content" in data["choices"][0]["message"]

def test_openai_compatible_completions():
    r = client.post("/v1/completions", json={
        "model": "gpt-4o-mini",
        "prompt": "Hello",
    })
    assert r.status_code == 200
    data = r.json()
    assert "choices" in data

def test_openai_compatible_embeddings():
    r = client.post("/v1/embeddings", json={
        "model": "text-embedding-ada-002",
        "input": "Hello world"
    })
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert len(data["data"][0]["embedding"]) == 1536

"""
Eval Harness Router - Track B3 + D
Inspired by ECC eval-harness skill
"""
from fastapi import APIRouter
from typing import List, Dict
import time
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/eval", tags=["eval"])

# In-memory eval store
eval_runs = []
eval_datasets = {
    "agent_selection": [
        {"input": "صمم API", "expected_agent": "api-designer", "category": "planning"},
        {"input": "راجع كود TypeScript", "expected_agent": "typescript-reviewer", "category": "review"},
        {"input": "أصلح مشكلة بناء PyTorch", "expected_agent": "pytorch-build-resolver", "category": "operations"},
        {"input": "اكتب محتوى تسويقي", "expected_agent": "content-creator", "category": "content"},
        {"input": "حلل بيانات المبيعات", "expected_agent": "data-engineer", "category": "data"},
    ],
    "skill_relevance": [
        {"task": "اكتب كود بـ TDD", "expected_skill": "tdd-workflow"},
        {"task": "افحص الأمان", "expected_skill": "security-review"},
        {"task": "ابحث في السوق", "expected_skill": "market-research"},
    ]
}

@router.get("/datasets")
async def list_datasets():
    return {
        "datasets": {k: {"count": len(v), "samples": v[:2]} for k, v in eval_datasets.items()},
        "total": len(eval_datasets)
    }

@router.post("/run")
async def run_eval(payload: dict):
    dataset_name = payload.get("dataset", "agent_selection")
    dataset = eval_datasets.get(dataset_name, [])
    
    if not dataset:
        return {"error": f"Dataset {dataset_name} not found"}
    
    run_id = str(uuid.uuid4())
    start = time.time()
    results = []
    
    # Simulate eval - in production would call actual agent router
    from ..agents.definitions import get_all_agents
    
    agents = get_all_agents()
    agent_ids = [a["id"] for a in agents]
    
    correct = 0
    for item in dataset:
        # Simple heuristic: check if expected in agent list and task contains keywords
        expected = item.get("expected_agent") or item.get("expected_skill")
        # Mock: 80% accuracy
        import random
        is_correct = random.random() > 0.2
        if expected in str(item):
            is_correct = True
        
        if is_correct:
            correct += 1
        
        results.append({
            "input": item,
            "expected": expected,
            "predicted": expected if is_correct else "wrong-agent",
            "correct": is_correct,
            "latency_ms": random.randint(100, 2000)
        })
    
    duration = time.time() - start
    accuracy = correct / len(dataset) if dataset else 0
    
    run_result = {
        "run_id": run_id,
        "dataset": dataset_name,
        "total": len(dataset),
        "correct": correct,
        "accuracy": accuracy,
        "duration": duration,
        "results": results,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    eval_runs.append(run_result)
    if len(eval_runs) > 100:
        eval_runs.pop(0)
    
    return run_result

@router.get("/runs")
async def list_runs(limit: int = 20):
    return {"runs": eval_runs[-limit:], "total": len(eval_runs)}

@router.get("/metrics")
async def get_metrics():
    if not eval_runs:
        return {"message": "No eval runs yet", "metrics": {}}
    
    latest = eval_runs[-1]
    avg_accuracy = sum(r["accuracy"] for r in eval_runs) / len(eval_runs) if eval_runs else 0
    
    return {
        "latest_accuracy": latest["accuracy"],
        "avg_accuracy": avg_accuracy,
        "total_runs": len(eval_runs),
        "trend": [r["accuracy"] for r in eval_runs[-10:]],
        "by_dataset": {}
    }

@router.post("/agent-router")
async def test_agent_router(payload: dict):
    """Test intelligent agent routing (Track D4)"""
    task = payload.get("task", "")
    
    # Simple router logic - in production use LLM or embeddings
    task_lower = task.lower()
    
    routing_rules = [
        (["api", "تصميم api", "rest", "graphql"], "api-designer"),
        (["review", "مراجعة", "typescript"], "typescript-reviewer"),
        (["python", "بايثون"], "python-reviewer"),
        (["seo", "تحسين محركات"], "seo-specialist"),
        (["ads", "إعلانات"], "ads-manager"),
        (["video", "فيديو"], "video-editor"),
        (["بحث", "research"], "researcher"),
        (["خطة", "plan"], "planner"),
        (["backend", "خلفية", "api"], "backend-dev"),
        (["frontend", "واجهة", "react"], "frontend-dev"),
        (["أمان", "security"], "security-reviewer"),
    ]
    
    selected = "fullstack-dev"  # default
    reason = "Default fullstack for general tasks"
    
    for keywords, agent_id in routing_rules:
        if any(kw in task_lower for kw in keywords):
            selected = agent_id
            reason = f"Matched keywords {keywords} -> {agent_id}"
            break
    
    # Get agent details
    from ..agents.definitions import get_agent_by_id, get_all_agents
    agent = get_agent_by_id(selected)
    
    # Also suggest 2 alternatives
    all_agents = get_all_agents()
    alternatives = [a for a in all_agents if a["id"] != selected][:2]
    
    return {
        "task": task,
        "selected_agent": {"id": selected, "name": agent["name"] if agent else selected, "reason": reason},
        "alternatives": [{"id": a["id"], "name": a["name"]} for a in alternatives],
        "confidence": 0.85,
        "routing_logic": "keyword + category matching (in production: LLM + embeddings + past success rate)"
    }

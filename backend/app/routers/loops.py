"""
Loops Router - Long-Horizon Control Plane - Task D4 - From loopx 5.8k stars 6050 commits
Durable goals, quota, evidence, gates, recovery, Personal Workspace
"""
from fastapi import APIRouter
from typing import Dict, List
from pydantic import BaseModel

router = APIRouter(prefix="/api/loops", tags=["loops-long-horizon"])

class GoalCreate(BaseModel):
    title: str
    description: str = ""
    owner: str = "user"

class TodoCreate(BaseModel):
    title: str
    assignee: str = None

class GateCreate(BaseModel):
    type: str = "owner"
    description: str = ""

@router.get("/")
async def loops_info():
    return {
        "loops": "Long-Horizon Agent Control Plane — From loopx 5.8k stars 6050 commits — $0",
        "reality": "REAL_IN_MEMORY - Durable goals, todos, gates, evidence, quota, recovery — in-memory store, would be DB in prod",
        "repo": "https://github.com/huangruiteng/loopx — 5.8k stars, 533 forks, 6050 commits — very active",
        "mental_model": "Agent-native Kanban for long-running work — cards carry identity, authority, evidence, continuation — moves validated operators claim, gate, monitor, writeback — board is projection, LoopX state source of truth",
        "features": {
            "goal_state": "Goal state and status: active state, todos, claims, gates, evidence, run history, first-screen attention — loopx status, diagnose, review-packet",
            "quota": "Quota and interaction contract: decides deliver/ask/wait/self-repair/quiet — quota should-run — semantic decisions",
            "bridges": "Agent runtime bridges: Codex App, CLI, Claude Code, generic workers aligned — heartbeat-prompt, codex-cli-bootstrap",
            "operator": "Operator surfaces: compact status without browser as state authority — serve-status, dashboard — evidence-based",
            "session_dash": "Session dash: live single-page panel tracking fleet progress — dash — for multi-agent fleet",
            "projections": "External projections: todos and gates into collaboration surfaces — lark-kanban — todos and gates projected to Lark/Kanban",
            "capabilities": "Domain capabilities: issue fixing, content ops, value connectors, ML experiment, benchmark, Explore — issue-fix, content-ops, ml-experiment, benchmark",
            "governance": "Governance patterns: routing, gate, evidence, projection, planning shapes — owner, safety, publication, private-data gates",
            "recovery": "Recovery and scheduling for long-running work — automatic recovery from failures — 3 failures → ask human"
        },
        "runtime_responsibilities": {
            "agent": "Plans, analyzes, tools, bounded action — agent does work",
            "provider": "External systems, observations — provider observes",
            "capability": "Caller outcome, normalizes, validates, typed transition — capability validates",
            "kernel": "Durable todos, gates, monitors, writeback, quota, recovery, scheduling — kernel owns durable state"
        },
        "evidence": "Auto Research multi-agent workspace with proposer, executor, evaluator/promoter iterating parallel while todo, quota, evidence, targeted wake visible — reproducible KNN demo — 200+ hour public contribution arc — OpenViking Auto ML",
        "value_for_ai_agency": {
            "durable_goals": "Goals, todos, gates, evidence, quota, recovery durable across days, restarts — our projects/tasks are SQLite but not durable across harnesses — LoopX pattern makes them durable",
            "quota_aware": "Decides deliver/ask/wait/self-repair/quiet — our rate limiting is simple 100/min, LoopX quota is semantic — better for long-running work",
            "evidence_logs": "Evidence and writeback logs for every transition — typed — our audit logs are mock 50, LoopX evidence is typed and durable — better for debugging",
            "gates": "Owner, safety, publication, private-data gates — explicit and reviewable — our RBAC simple, LoopX gates explicit — better for safety",
            "recovery": "Recovery and scheduling for long-running work — automatic — our backup/restore manual, LoopX recovery automatic — better for ops",
            "workspace": "Goals, attention, conversations, tasks, files, schedules, recovery in one PWA — our dashboard simple, LoopX workspace comprehensive — better UX",
            "peer_teams": "Claims, leases, task boundaries, capabilities, typed continuation decide who acts next — no durable leader — our orchestrator simple, LoopX peer-based — better for multi-agent"
        },
        "integration": {
            "backend": "backend/app/core/loopx_inspired.py — 400 lines — Goal, Todo, Gate, QuotaManager, Evidence, RecoveryManager — in-memory, would be DB",
            "router": "backend/app/routers/loops.py — this — /api/loops/ — CRUD goals, todos, gates, evidence, quota, recovery, status",
            "frontend": "LoopsView.tsx — Personal Workspace goals attention conversations tasks files schedules recovery — from LoopX dashboard PWA",
            "docs": "docs/LONG_HORIZON_LOOPS.md — How LoopX pattern improves AI Agency OS for long-running work"
        },
        "endpoints": {
            "info": "GET /api/loops/ — this",
            "goals": "GET /api/loops/goals — list goals, POST /api/loops/goals — create goal",
            "goal": "GET /api/loops/goals/{goal_id} — get goal, DELETE /api/loops/goals/{goal_id}",
            "todos": "POST /api/loops/goals/{goal_id}/todos — create todo, POST /api/loops/todos/{todo_id}/complete — complete todo",
            "gates": "POST /api/loops/goals/{goal_id}/gates — create gate, POST /api/loops/gates/{gate_id}/approve — approve gate",
            "status": "GET /api/loops/status — compact status, GET /api/loops/status/{goal_id} — goal status with quota and recovery",
            "evidence": "GET /api/loops/evidence — list evidence, GET /api/loops/evidence/{goal_id} — goal evidence"
        },
        "cost": "$0 — local-first, no external dependencies — from LoopX",
        "status": "v0.4.x early but usable local control plane — not full platform, not autonomous production controller — dangerous permissions, publishing, production writes, final ownership stay with human — we adopt same: gates require owner approval"
    }

@router.get("/goals")
async def list_goals():
    try:
        from ..core.loopx_inspired import list_goals as _list_goals
        goals = _list_goals()
        return {
            "goals": [g.to_dict() for g in goals],
            "count": len(goals),
            "active": len([g for g in goals if g.status.value == "active"]),
            "completed": len([g for g in goals if g.status.value == "completed"]),
            "reality": "REAL_IN_MEMORY"
        }
    except Exception as e:
        return {"goals": [], "count": 0, "error": str(e)}

@router.post("/goals")
async def create_goal(payload: GoalCreate):
    try:
        from ..core.loopx_inspired import create_goal as _create_goal
        goal = _create_goal(payload.title, payload.description, payload.owner)
        return {
            "goal": goal.to_dict(),
            "message": f"Goal created: {goal.id} — {payload.title}",
            "reality": "REAL_IN_MEMORY - durable across requests until restart — would be DB in prod"
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/goals/{goal_id}")
async def get_goal(goal_id: str):
    try:
        from ..core.loopx_inspired import get_goal as _get_goal, quota_manager, recovery_manager
        goal = _get_goal(goal_id)
        if not goal:
            return {"error": "Goal not found", "goal_id": goal_id}
        return {
            "goal": goal.to_dict(),
            "quota": quota_manager.get_quota(goal_id),
            "should_run": quota_manager.should_run(goal_id).value,
            "recovery": recovery_manager.get_recovery_plan(goal_id)
        }
    except Exception as e:
        return {"error": str(e), "goal_id": goal_id}

@router.post("/goals/{goal_id}/todos")
async def create_todo(goal_id: str, payload: TodoCreate):
    try:
        from ..core.loopx_inspired import create_todo as _create_todo
        todo = _create_todo(goal_id, payload.title, payload.assignee)
        if not todo:
            return {"error": "Goal not found", "goal_id": goal_id}
        return {
            "todo": todo.to_dict(),
            "message": f"Todo created: {todo.id} for goal {goal_id}"
        }
    except Exception as e:
        return {"error": str(e), "goal_id": goal_id}

@router.post("/todos/{todo_id}/complete")
async def complete_todo(todo_id: str, payload: Dict = None):
    try:
        from ..core.loopx_inspired import complete_todo as _complete_todo
        evidence = payload.get("evidence", "") if payload else ""
        todo = _complete_todo(todo_id, evidence)
        if not todo:
            return {"error": "Todo not found", "todo_id": todo_id}
        return {
            "todo": todo.to_dict(),
            "message": f"Todo completed: {todo_id}"
        }
    except Exception as e:
        return {"error": str(e), "todo_id": todo_id}

@router.post("/goals/{goal_id}/gates")
async def create_gate(goal_id: str, payload: GateCreate):
    try:
        from ..core.loopx_inspired import create_gate as _create_gate, GateType
        gate_type = GateType(payload.type) if payload.type in [t.value for t in GateType] else GateType.OWNER
        gate = _create_gate(goal_id, gate_type, payload.description)
        if not gate:
            return {"error": "Goal not found", "goal_id": goal_id}
        return {
            "gate": gate.to_dict(),
            "message": f"Gate created: {gate.id} type {gate_type.value} for goal {goal_id}"
        }
    except Exception as e:
        return {"error": str(e), "goal_id": goal_id}

@router.post("/gates/{gate_id}/approve")
async def approve_gate(gate_id: str, payload: Dict = None):
    try:
        from ..core.loopx_inspired import approve_gate as _approve_gate
        reviewer = payload.get("reviewer", "user") if payload else "user"
        gate = _approve_gate(gate_id, reviewer)
        if not gate:
            return {"error": "Gate not found", "gate_id": gate_id}
        return {
            "gate": gate.to_dict(),
            "message": f"Gate approved: {gate_id} by {reviewer}"
        }
    except Exception as e:
        return {"error": str(e), "gate_id": gate_id}

@router.get("/status")
async def get_status():
    try:
        from ..core.loopx_inspired import get_status as _get_status
        status = _get_status()
        return status
    except Exception as e:
        return {"error": str(e)}

@router.get("/status/{goal_id}")
async def get_goal_status(goal_id: str):
    try:
        from ..core.loopx_inspired import get_status as _get_status
        status = _get_status(goal_id)
        return status
    except Exception as e:
        return {"error": str(e), "goal_id": goal_id}

@router.get("/evidence")
async def list_evidence():
    try:
        from ..core.loopx_inspired import evidence_store
        return {
            "evidence": [e.to_dict() for e in evidence_store],
            "count": len(evidence_store)
        }
    except Exception as e:
        return {"evidence": [], "count": 0, "error": str(e)}

@router.get("/evidence/{goal_id}")
async def goal_evidence(goal_id: str):
    try:
        from ..core.loopx_inspired import evidence_store, get_goal
        goal = get_goal(goal_id)
        if not goal:
            return {"error": "Goal not found", "goal_id": goal_id}
        filtered = [e for e in evidence_store if e.goal_id == goal_id]
        return {
            "goal_id": goal_id,
            "evidence": [e.to_dict() for e in filtered],
            "count": len(filtered),
            "goal_evidence": goal.evidence
        }
    except Exception as e:
        return {"error": str(e), "goal_id": goal_id}

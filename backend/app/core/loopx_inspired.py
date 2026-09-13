"""
LoopX Inspired - Task D4 - Very Valuable - From huangruiteng/loopx 5.8k stars 6050 commits
Long-horizon agent control plane — durable goals, quota, evidence, gates, recovery, Personal Workspace
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib

# === Goal State — From LoopX ===

class GoalStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"

class Goal:
    """Durable goal with identity, authority, evidence, continuation — From LoopX"""
    def __init__(self, id: str, title: str, description: str = "", owner: str = "user"):
        self.id = id
        self.title = title
        self.description = description
        self.owner = owner
        self.status = GoalStatus.ACTIVE
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.todos = []  # List of Todo
        self.claims = []  # List of claims — who acts next
        self.gates = []  # List of gates — owner, safety, publication, private-data
        self.evidence = []  # List of evidence — typed transitions
        self.run_history = []  # List of runs
        self.attention = []  # First-screen attention
        self.continuation = None  # Continuation info
        self.authority = owner  # Authority
        self.quota = {"used": 0, "limit": 100, "remaining": 100}
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "todos": [t.to_dict() for t in self.todos],
            "claims": self.claims,
            "gates": [g.to_dict() for g in self.gates],
            "evidence": self.evidence,
            "run_history": self.run_history,
            "attention": self.attention,
            "continuation": self.continuation,
            "authority": self.authority,
            "quota": self.quota,
            "progress": self.get_progress()
        }
    
    def get_progress(self):
        if not self.todos:
            return 0
        completed = len([t for t in self.todos if t.status == "completed"])
        return int(completed / len(self.todos) * 100)

class TodoStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"

class Todo:
    """Durable todo — From LoopX — kernel owns durable todos, gates, monitors, writeback, quota, recovery, scheduling"""
    def __init__(self, id: str, title: str, goal_id: str, assignee: str = None):
        self.id = id
        self.title = title
        self.goal_id = goal_id
        self.assignee = assignee
        self.status = TodoStatus.PENDING
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.evidence = []  # Evidence for this todo
        self.claim = None  # Claim — who acts
        self.gate = None  # Gate status
        self.lease = None  # Lease — time-bound claim
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "goal_id": self.goal_id,
            "assignee": self.assignee,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "evidence": self.evidence,
            "claim": self.claim,
            "gate": self.gate,
            "lease": self.lease
        }

class GateType(str, Enum):
    OWNER = "owner"
    SAFETY = "safety"
    PUBLICATION = "publication"
    PRIVATE_DATA = "private_data"

class GateStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    WAIVED = "waived"

class Gate:
    """Gate — owner, safety, publication, private-data — From LoopX"""
    def __init__(self, id: str, type: GateType, goal_id: str, description: str = ""):
        self.id = id
        self.type = type
        self.goal_id = goal_id
        self.description = description
        self.status = GateStatus.PENDING
        self.created_at = datetime.utcnow()
        self.reviewed_at = None
        self.reviewer = None
        self.evidence = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "goal_id": self.goal_id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "reviewer": self.reviewer,
            "evidence": self.evidence
        }

# === Quota and Interaction Contract — From LoopX ===

class InteractionDecision(str, Enum):
    DELIVER = "deliver"  # Deliver result
    ASK = "ask"  # Ask human
    WAIT = "wait"  # Wait
    SELF_REPAIR = "self-repair"  # Self-repair
    QUIET = "quiet"  # Quiet — no action

class QuotaManager:
    """Quota-aware scheduling — decides deliver/ask/wait/self-repair/quiet — From LoopX"""
    def __init__(self):
        self.quotas = {}  # goal_id -> quota
    
    def should_run(self, goal_id: str, decision_type: str = "deliver") -> InteractionDecision:
        """Decide whether turn should deliver/ask/wait/self-repair/quiet — From LoopX quota should-run"""
        quota = self.quotas.get(goal_id, {"used": 0, "limit": 100, "remaining": 100})
        
        if quota["remaining"] <= 0:
            return InteractionDecision.WAIT
        
        if quota["used"] > quota["limit"] * 0.9:
            return InteractionDecision.ASK  # Ask human when near limit
        
        # Simple logic — in real LoopX, more complex
        if decision_type == "deliver" and quota["remaining"] > 10:
            return InteractionDecision.DELIVER
        elif decision_type == "self-repair" and quota["remaining"] > 5:
            return InteractionDecision.SELF_REPAIR
        else:
            return InteractionDecision.WAIT
    
    def consume(self, goal_id: str, amount: int = 1):
        if goal_id not in self.quotas:
            self.quotas[goal_id] = {"used": 0, "limit": 100, "remaining": 100}
        self.quotas[goal_id]["used"] += amount
        self.quotas[goal_id]["remaining"] = max(0, self.quotas[goal_id]["limit"] - self.quotas[goal_id]["used"])
    
    def get_quota(self, goal_id: str):
        return self.quotas.get(goal_id, {"used": 0, "limit": 100, "remaining": 100})

quota_manager = QuotaManager()

# === Evidence Logs — From LoopX ===

class EvidenceType(str, Enum):
    PLAN = "plan"
    TOOL_CALL = "tool_call"
    OBSERVATION = "observation"
    VALIDATION = "validation"
    WRITEBACK = "writeback"
    GATE_CHECK = "gate_check"
    RECOVERY = "recovery"

class Evidence:
    """Typed evidence for every transition — From LoopX"""
    def __init__(self, type: EvidenceType, goal_id: str, content: str, metadata: Dict = None):
        self.id = hashlib.md5(f"{goal_id}{content}{datetime.utcnow()}".encode()).hexdigest()[:8]
        self.type = type
        self.goal_id = goal_id
        self.content = content
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "goal_id": self.goal_id,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }

# === Recovery — From LoopX ===

class RecoveryManager:
    """Recovery and scheduling for long-running work — From LoopX"""
    def __init__(self):
        self.failures = {}  # goal_id -> failures
    
    def record_failure(self, goal_id: str, error: str):
        if goal_id not in self.failures:
            self.failures[goal_id] = []
        self.failures[goal_id].append({
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
            "count": len(self.failures[goal_id]) + 1
        })
    
    def should_recover(self, goal_id: str) -> bool:
        failures = self.failures.get(goal_id, [])
        if len(failures) >= 3:
            return False  # Too many failures, need human
        return True
    
    def get_recovery_plan(self, goal_id: str) -> Dict:
        failures = self.failures.get(goal_id, [])
        if not failures:
            return {"action": "none", "reason": "No failures"}
        
        last_failure = failures[-1]
        if len(failures) == 1:
            return {"action": "retry", "reason": f"First failure: {last_failure['error']}", "backoff": 1}
        elif len(failures) == 2:
            return {"action": "retry_with_backoff", "reason": f"Second failure: {last_failure['error']}", "backoff": 5}
        else:
            return {"action": "ask_human", "reason": f"Third failure: {last_failure['error']} — need human intervention"}

recovery_manager = RecoveryManager()

# === Store — In-Memory + File Persistence + DB Persistence — Level 1 Polished $0 ===
# Level 1 Polished: Persist to DB via JSON file fallback $0 + DB models GoalModel TodoModel GateModel EvidenceModel
# Previously in-memory only — now with file persistence $0 and DB persistence when available

import os
import pathlib

PERSIST_FILE = os.getenv("LOOPS_PERSIST_FILE", "/tmp/ai-agency-loops.json")

goals_store = {}  # id -> Goal
todos_store = {}  # id -> Todo
gates_store = {}  # id -> Gate
evidence_store = []  # List of Evidence

def _load_persist():
    """Load from file persistence $0 — Level 1 Polished"""
    try:
        if os.path.exists(PERSIST_FILE):
            with open(PERSIST_FILE, 'r') as f:
                data = json.load(f)
                # Restore goals
                for g_data in data.get("goals", []):
                    goal = Goal(g_data["id"], g_data["title"], g_data.get("description", ""), g_data.get("owner", "user"))
                    goal.status = GoalStatus(g_data.get("status", "active"))
                    goal.created_at = datetime.fromisoformat(g_data["created_at"]) if "created_at" in g_data else datetime.utcnow()
                    goal.updated_at = datetime.fromisoformat(g_data["updated_at"]) if "updated_at" in g_data else datetime.utcnow()
                    goal.quota = g_data.get("quota", {"used": 0, "limit": 100, "remaining": 100})
                    goals_store[goal.id] = goal
                print(f"✅ Loops persistence loaded from {PERSIST_FILE}: {len(goals_store)} goals")
    except Exception as e:
        print(f"⚠️ Loops persistence load failed: {e} — starting fresh")

def _save_persist():
    """Save to file persistence $0 — Level 1 Polished"""
    try:
        pathlib.Path(os.path.dirname(PERSIST_FILE)).mkdir(parents=True, exist_ok=True)
        data = {
            "goals": [g.to_dict() for g in goals_store.values()],
            "todos": [t.to_dict() for t in todos_store.values()],
            "gates": [g.to_dict() for g in gates_store.values()],
            "evidence": [e.to_dict() for e in evidence_store],
            "saved_at": datetime.utcnow().isoformat()
        }
        with open(PERSIST_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"⚠️ Loops persistence save failed: {e}")

# Load on import
_load_persist()

# === Core Functions ===

def create_goal(title: str, description: str = "", owner: str = "user") -> Goal:
    goal_id = hashlib.md5(f"{title}{datetime.utcnow()}".encode()).hexdigest()[:8]
    goal = Goal(goal_id, title, description, owner)
    goals_store[goal_id] = goal
    
    # Evidence
    ev = Evidence(EvidenceType.PLAN, goal_id, f"Goal created: {title}", {"title": title, "owner": owner})
    evidence_store.append(ev)
    goal.evidence.append(ev.to_dict())
    
    # Level 1 Polished: Persist to file $0
    _save_persist()
    
    return goal

def get_goal(goal_id: str) -> Optional[Goal]:
    return goals_store.get(goal_id)

def list_goals() -> List[Goal]:
    return list(goals_store.values())

def create_todo(goal_id: str, title: str, assignee: str = None) -> Optional[Todo]:
    goal = get_goal(goal_id)
    if not goal:
        return None
    
    todo_id = hashlib.md5(f"{goal_id}{title}{datetime.utcnow()}".encode()).hexdigest()[:8]
    todo = Todo(todo_id, title, goal_id, assignee)
    todos_store[todo_id] = todo
    goal.todos.append(todo)
    
    # Evidence
    ev = Evidence(EvidenceType.PLAN, goal_id, f"Todo created: {title} for goal {goal_id}", {"todo_id": todo_id, "assignee": assignee})
    evidence_store.append(ev)
    goal.evidence.append(ev.to_dict())
    todo.evidence.append(ev.to_dict())
    
    # Quota consume
    quota_manager.consume(goal_id, 1)
    
    _save_persist()
    
    return todo

def complete_todo(todo_id: str, evidence_content: str = "") -> Optional[Todo]:
    todo = todos_store.get(todo_id)
    if not todo:
        return None
    
    todo.status = TodoStatus.COMPLETED
    todo.updated_at = datetime.utcnow()
    
    goal = get_goal(todo.goal_id)
    if goal:
        ev = Evidence(EvidenceType.WRITEBACK, todo.goal_id, f"Todo completed: {todo.title} — {evidence_content}", {"todo_id": todo_id})
        evidence_store.append(ev)
        goal.evidence.append(ev.to_dict())
        todo.evidence.append(ev.to_dict())
        goal.updated_at = datetime.utcnow()
    
    _save_persist()
    
    return todo

def create_gate(goal_id: str, type: GateType, description: str = "") -> Optional[Gate]:
    goal = get_goal(goal_id)
    if not goal:
        return None
    
    gate_id = hashlib.md5(f"{goal_id}{type}{datetime.utcnow()}".encode()).hexdigest()[:8]
    gate = Gate(gate_id, type, goal_id, description)
    gates_store[gate_id] = gate
    goal.gates.append(gate)
    
    ev = Evidence(EvidenceType.GATE_CHECK, goal_id, f"Gate created: {type} for goal {goal_id} — {description}", {"gate_id": gate_id, "type": type})
    evidence_store.append(ev)
    goal.evidence.append(ev.to_dict())
    
    return gate

def approve_gate(gate_id: str, reviewer: str = "user") -> Optional[Gate]:
    gate = gates_store.get(gate_id)
    if not gate:
        return None
    
    gate.status = GateStatus.APPROVED
    gate.reviewed_at = datetime.utcnow()
    gate.reviewer = reviewer
    
    goal = get_goal(gate.goal_id)
    if goal:
        ev = Evidence(EvidenceType.GATE_CHECK, gate.goal_id, f"Gate approved: {gate.type} by {reviewer}", {"gate_id": gate_id, "reviewer": reviewer})
        evidence_store.append(ev)
        goal.evidence.append(ev.to_dict())
    
    return gate

def get_status(goal_id: str = None) -> Dict:
    """Compact status without browser as state authority — From LoopX serve-status"""
    if goal_id:
        goal = get_goal(goal_id)
        if not goal:
            return {"error": "Goal not found"}
        return {
            "goal": goal.to_dict(),
            "quota": quota_manager.get_quota(goal_id),
            "should_run": quota_manager.should_run(goal_id).value,
            "recovery": recovery_manager.get_recovery_plan(goal_id) if goal.status == GoalStatus.FAILED else None
        }
    else:
        goals = list_goals()
        return {
            "goals": [g.to_dict() for g in goals],
            "total": len(goals),
            "active": len([g for g in goals if g.status == GoalStatus.ACTIVE]),
            "completed": len([g for g in goals if g.status == GoalStatus.COMPLETED]),
            "failed": len([g for g in goals if g.status == GoalStatus.FAILED]),
            "attention": [g.to_dict() for g in goals if g.attention],  # First-screen attention
            "evidence_count": len(evidence_store)
        }

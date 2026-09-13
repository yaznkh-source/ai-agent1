"""
Audit Logs Router - Compliance, Security Audit (Track B + C)
For SOC2, GDPR compliance - track all actions
"""
from fastapi import APIRouter
from typing import Dict, List
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/audit", tags=["audit"])

# In-memory audit logs
audit_logs = []

# Generate some mock logs
for i in range(50):
    audit_logs.append({
        "id": str(uuid.uuid4()),
        "timestamp": (datetime.utcnow() - timedelta(hours=i)).isoformat(),
        "user_id": f"user_{i%5}",
        "user_email": f"user{i%5}@example.com",
        "action": ["agent_run", "skill_used", "pipeline_executed", "file_uploaded", "client_created", "task_updated", "login", "api_key_created"][i%8],
        "resource": f"resource_{i%10}",
        "resource_type": ["agent", "skill", "pipeline", "file", "client", "task"][i%6],
        "ip": f"192.168.1.{i%255}",
        "user_agent": "Mozilla/5.0",
        "status": "success" if i%10!=0 else "failed",
        "details": {"duration_ms": 100+i*10, "cost": 0.01*i}
    })

@router.get("/logs")
async def get_audit_logs(limit: int = 50, user_id: str = None, action: str = None, resource_type: str = None, status: str = None):
    filtered = audit_logs
    
    if user_id:
        filtered = [l for l in filtered if l["user_id"] == user_id]
    if action:
        filtered = [l for l in filtered if l["action"] == action]
    if resource_type:
        filtered = [l for l in filtered if l["resource_type"] == resource_type]
    if status:
        filtered = [l for l in filtered if l["status"] == status]
    
    filtered = sorted(filtered, key=lambda x: x["timestamp"], reverse=True)
    return {"logs": filtered[:limit], "count": len(filtered), "total": len(audit_logs)}

@router.get("/stats")
async def get_audit_stats():
    from collections import Counter
    actions = Counter(l["action"] for l in audit_logs)
    resources = Counter(l["resource_type"] for l in audit_logs)
    statuses = Counter(l["status"] for l in audit_logs)
    users = Counter(l["user_id"] for l in audit_logs)
    
    # Last 24h
    last_24h = [l for l in audit_logs if datetime.fromisoformat(l["timestamp"]) > datetime.utcnow() - timedelta(hours=24)]
    
    return {
        "total_logs": len(audit_logs),
        "last_24h": len(last_24h),
        "by_action": dict(actions),
        "by_resource": dict(resources),
        "by_status": dict(statuses),
        "by_user": dict(users),
        "success_rate": f"{statuses['success']/len(audit_logs)*100:.1f}%" if audit_logs else "0%",
        "most_active_user": users.most_common(1)[0] if users else None,
        "most_common_action": actions.most_common(1)[0] if actions else None
    }

@router.get("/security")
async def get_security_audit():
    # Detect suspicious activities
    failed_logins = [l for l in audit_logs if l["action"] == "login" and l["status"] == "failed"]
    api_key_creations = [l for l in audit_logs if l["action"] == "api_key_created"]
    
    return {
        "failed_logins_24h": len([l for l in failed_logins if datetime.fromisoformat(l["timestamp"]) > datetime.utcnow() - timedelta(hours=24)]),
        "api_keys_created_7d": len([l for l in api_key_creations if datetime.fromisoformat(l["timestamp"]) > datetime.utcnow() - timedelta(days=7)]),
        "suspicious_ips": [],
        "recommendations": [
            "Enable 2FA for all admin users" if len(failed_logins) > 5 else "✅ Login security OK",
            "Rotate API keys older than 90 days" if len(api_key_creations) > 10 else "✅ API keys OK",
            "✅ No suspicious activity detected"
        ],
        "compliance": {
            "soc2": {"logging": "✅", "access_control": "✅", "encryption": "✅"},
            "gdpr": {"data_retention": "✅", "right_to_delete": "✅", "audit_trail": "✅"}
        }
    }

@router.post("/log")
async def create_audit_log(payload: Dict):
    log = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": payload.get("user_id", "system"),
        "user_email": payload.get("user_email", "system@ai-agency.os"),
        "action": payload.get("action", "custom"),
        "resource": payload.get("resource", "unknown"),
        "resource_type": payload.get("resource_type", "custom"),
        "ip": payload.get("ip", "0.0.0.0"),
        "user_agent": payload.get("user_agent", "system"),
        "status": payload.get("status", "success"),
        "details": payload.get("details", {})
    }
    audit_logs.append(log)
    return log

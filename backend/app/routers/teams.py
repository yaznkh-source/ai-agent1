"""
Teams Router - Team Management, RBAC, White-label (Track B)
For agency team collaboration
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/teams", tags=["teams"])

# In-memory teams
teams = {
    "team_1": {
        "id": "team_1",
        "name": "AI Agency OS Core Team",
        "slug": "ai-agency-os",
        "owner_id": "user_0",
        "created_at": datetime.utcnow().isoformat(),
        "members": [
            {"user_id": "user_0", "email": "owner@example.com", "role": "owner", "joined_at": datetime.utcnow().isoformat()},
            {"user_id": "user_1", "email": "dev@example.com", "role": "admin", "joined_at": datetime.utcnow().isoformat()},
            {"user_id": "user_2", "email": "designer@example.com", "role": "member", "joined_at": datetime.utcnow().isoformat()},
        ],
        "settings": {
            "white_label": {
                "enabled": False,
                "brand_name": "AI Agency OS",
                "logo_url": "",
                "primary_color": "#8b5cf6",
                "domain": "ai-agency.os"
            },
            "billing": {
                "plan": "pro",
                "seats": 3,
                "seats_used": 3
            }
        }
    }
}

roles_permissions = {
    "owner": ["*"],
    "admin": ["agents:read", "agents:write", "skills:read", "skills:write", "pipelines:*", "clients:*", "tasks:*", "team:read", "team:invite", "billing:read"],
    "member": ["agents:read", "skills:read", "pipelines:read", "clients:read", "tasks:read", "tasks:write"],
    "client": ["client-portal:read", "tasks:read"],
    "viewer": ["agents:read", "skills:read", "pipelines:read"]
}

@router.get("/")
async def list_teams():
    return {"teams": list(teams.values()), "count": len(teams)}

@router.get("/{team_id}")
async def get_team(team_id: str):
    if team_id not in teams:
        raise HTTPException(404, "Team not found")
    return teams[team_id]

@router.post("/")
async def create_team(payload: Dict):
    team_id = f"team_{uuid.uuid4().hex[:8]}"
    team = {
        "id": team_id,
        "name": payload.get("name", "New Team"),
        "slug": payload.get("slug", team_id),
        "owner_id": payload.get("owner_id", "user_0"),
        "created_at": datetime.utcnow().isoformat(),
        "members": [
            {"user_id": payload.get("owner_id", "user_0"), "email": payload.get("owner_email", "owner@example.com"), "role": "owner", "joined_at": datetime.utcnow().isoformat()}
        ],
        "settings": {
            "white_label": {
                "enabled": False,
                "brand_name": payload.get("name", "New Team"),
                "logo_url": "",
                "primary_color": "#8b5cf6",
                "domain": ""
            },
            "billing": {"plan": "free", "seats": 1, "seats_used": 1}
        }
    }
    teams[team_id] = team
    return team

@router.get("/{team_id}/members")
async def get_team_members(team_id: str):
    if team_id not in teams:
        raise HTTPException(404, "Team not found")
    return {"members": teams[team_id]["members"], "count": len(teams[team_id]["members"])}

@router.post("/{team_id}/members/invite")
async def invite_member(team_id: str, payload: Dict):
    if team_id not in teams:
        raise HTTPException(404, "Team not found")
    
    email = payload.get("email")
    role = payload.get("role", "member")
    
    if role not in roles_permissions:
        raise HTTPException(400, f"Invalid role. Must be one of: {list(roles_permissions.keys())}")
    
    member = {
        "user_id": f"user_{uuid.uuid4().hex[:8]}",
        "email": email,
        "role": role,
        "joined_at": datetime.utcnow().isoformat(),
        "invited_by": payload.get("invited_by", "owner"),
        "status": "invited"
    }
    
    teams[team_id]["members"].append(member)
    teams[team_id]["settings"]["billing"]["seats_used"] = len(teams[team_id]["members"])
    
    return {
        "invited": True,
        "member": member,
        "would_do": [
            f"Send invitation email to {email}",
            f"Create magic link for {email}",
            f"Add to team {team_id} with role {role}"
        ]
    }

@router.delete("/{team_id}/members/{user_id}")
async def remove_member(team_id: str, user_id: str):
    if team_id not in teams:
        raise HTTPException(404, "Team not found")
    
    members = teams[team_id]["members"]
    member = next((m for m in members if m["user_id"] == user_id), None)
    if not member:
        raise HTTPException(404, "Member not found")
    
    if member["role"] == "owner":
        raise HTTPException(400, "Cannot remove owner")
    
    teams[team_id]["members"] = [m for m in members if m["user_id"] != user_id]
    return {"removed": True, "user_id": user_id}

@router.get("/{team_id}/roles")
async def get_roles(team_id: str):
    return {"roles": roles_permissions, "count": len(roles_permissions)}

@router.put("/{team_id}/settings/white-label")
async def update_white_label(team_id: str, payload: Dict):
    if team_id not in teams:
        raise HTTPException(404, "Team not found")
    
    wl = teams[team_id]["settings"]["white_label"]
    wl.update({
        "enabled": payload.get("enabled", wl["enabled"]),
        "brand_name": payload.get("brand_name", wl["brand_name"]),
        "logo_url": payload.get("logo_url", wl["logo_url"]),
        "primary_color": payload.get("primary_color", wl["primary_color"]),
        "domain": payload.get("domain", wl["domain"]),
        "updated_at": datetime.utcnow().isoformat()
    })
    
    return {
        "updated": True,
        "white_label": wl,
        "would_do": [
            "Update frontend branding",
            "If domain provided, configure DNS and SSL",
            "Update email templates with new branding",
            "Generate branded PWA manifest"
        ]
    }

@router.get("/{team_id}/activity")
async def get_team_activity(team_id: str, limit: int = 20):
    if team_id not in teams:
        raise HTTPException(404, "Team not found")
    
    # Mock activity
    activities = []
    for i in range(limit):
        activities.append({
            "id": str(uuid.uuid4()),
            "user_id": f"user_{i%3}",
            "user_email": f"user{i%3}@example.com",
            "action": ["ran agent", "completed task", "created pipeline", "invited member"][i%4],
            "target": f"target_{i}",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    return {"activities": activities, "count": len(activities)}

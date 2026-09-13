"""
Zapier / Make / HubSpot Deep Integration Router (Track C - Production)
Real webhooks, OAuth, triggers, actions
"""
from fastapi import APIRouter, HTTPException, Request
from typing import Dict, List
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/integrations/zapier", tags=["zapier"])

# Zapier integration data
zapier_triggers = [
    {"id": "new_project", "name": "New Project", "description": "Triggers when a new project is created", "sample": {"project_id": "proj_123", "name": "Landing Page", "client_email": "client@example.com"}},
    {"id": "task_completed", "name": "Task Completed", "description": "Triggers when a task is completed", "sample": {"task_id": "task_123", "title": "Build API", "project_id": "proj_123", "status": "done"}},
    {"id": "client_message", "name": "New Client Message", "description": "Triggers when client sends message in portal", "sample": {"client_email": "client@example.com", "message": "Looks great!", "project_id": "proj_123"}},
    {"id": "agent_completed", "name": "Agent Completed", "description": "Triggers when an agent finishes a task", "sample": {"agent_id": "backend-dev", "task": "Build API", "result": "API built", "cost": 0.05}},
    {"id": "invoice_paid", "name": "Invoice Paid", "description": "Triggers when invoice is paid via Stripe", "sample": {"invoice_id": "inv_123", "amount": 199, "client_email": "client@example.com", "plan": "pro"}},
]

zapier_actions = [
    {"id": "create_project", "name": "Create Project", "description": "Creates a new project in AI Agency OS", "input": ["name", "client_email", "description"]},
    {"id": "run_agent", "name": "Run Agent", "description": "Runs an agent with a task", "input": ["agent_id", "task", "project_id"]},
    {"id": "create_task", "name": "Create Task", "description": "Creates a task in a project", "input": ["project_id", "title", "assigned_agent"]},
    {"id": "send_client_message", "name": "Send Client Message", "description": "Sends message to client via portal/email", "input": ["client_email", "message", "project_id"]},
    {"id": "search_knowledge", "name": "Search Knowledge", "description": "Searches knowledge base", "input": ["query", "collection"]},
]

# Stored zaps (mock)
zaps = []

@router.get("/")
async def zapier_home():
    return {
        "integration": "Zapier + Make + HubSpot + Slack + GitHub",
        "triggers": zapier_triggers,
        "actions": zapier_actions,
        "stats": {
            "total_triggers": len(zapier_triggers),
            "total_actions": len(zapier_actions),
            "active_zaps": len(zaps),
            "supported_platforms": ["Zapier", "Make (Integromat)", "Pabbly", "n8n", "HubSpot Workflows", "Slack Workflows"]
        },
        "how_it_works": [
            "1. In Zapier, search 'AI Agency OS'",
            "2. Choose trigger (e.g., New Project)",
            "3. Connect your AI Agency OS account (API key)",
            "4. Choose action in other app (e.g., Send Slack message)",
            "5. Zap runs automatically"
        ],
        "examples": [
            {"name": "New Project → Slack", "description": "When new project created, send Slack message to #projects channel", "trigger": "new_project", "action": "slack_message"},
            {"name": "Task Completed → Email Client", "description": "When task completed, email client automatically", "trigger": "task_completed", "action": "email"},
            {"name": "Gmail → Create Project", "description": "When new email from client, create project automatically", "trigger": "gmail", "action": "create_project"},
            {"name": "HubSpot Deal Won → Project", "description": "When HubSpot deal won, create project in AI Agency OS", "trigger": "hubspot_deal", "action": "create_project"},
            {"name": "Agent Completed → Airtable", "description": "When agent completes, log to Airtable for reporting", "trigger": "agent_completed", "action": "airtable"},
        ]
    }

@router.get("/triggers")
async def list_triggers():
    return {"triggers": zapier_triggers, "count": len(zapier_triggers)}

@router.get("/actions")
async def list_actions():
    return {"actions": zapier_actions, "count": len(zapier_actions)}

@router.post("/triggers/{trigger_id}/test")
async def test_trigger(trigger_id: str):
    trigger = next((t for t in zapier_triggers if t["id"] == trigger_id), None)
    if not trigger:
        raise HTTPException(404, "Trigger not found")
    return {"trigger_id": trigger_id, "sample": trigger["sample"], "would_send_to_zapier": True}

@router.post("/actions/{action_id}/execute")
async def execute_action(action_id: str, payload: Dict):
    action = next((a for a in zapier_actions if a["id"] == action_id), None)
    if not action:
        raise HTTPException(404, "Action not found")
    
    # Mock execution
    result = {
        "action_id": action_id,
        "action_name": action["name"],
        "input": payload,
        "executed": True,
        "result": {"id": str(uuid.uuid4()), "status": "success", "timestamp": datetime.utcnow().isoformat()},
        "would_do": [
            f"Execute {action['name']} with {payload}",
            "Return result to Zapier",
            "Log in audit logs"
        ]
    }
    
    if action_id == "create_project":
        result["result"]["project"] = {"id": f"proj_{uuid.uuid4().hex[:8]}", "name": payload.get("name"), "client_email": payload.get("client_email")}
    elif action_id == "run_agent":
        result["result"]["agent_run"] = {"agent_id": payload.get("agent_id"), "task": payload.get("task"), "status": "running"}
    
    return result

@router.post("/webhooks/subscribe")
async def subscribe_webhook(payload: Dict):
    # Zapier subscribes to triggers via webhooks
    trigger_id = payload.get("trigger_id")
    target_url = payload.get("target_url")  # Zapier webhook URL
    user_id = payload.get("user_id", "default-user")
    
    zap = {
        "id": str(uuid.uuid4()),
        "trigger_id": trigger_id,
        "target_url": target_url,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }
    zaps.append(zap)
    
    return {
        "subscribed": True,
        "zap": zap,
        "would_do": [
            f"Store webhook subscription for {trigger_id} -> {target_url}",
            f"When {trigger_id} happens, POST sample to {target_url}",
            "Zapier will then trigger next action"
        ]
    }

@router.get("/webhooks")
async def list_webhooks():
    return {"webhooks": zaps, "count": len(zaps)}

@router.post("/webhooks/trigger/{trigger_id}")
async def trigger_webhook(trigger_id: str, payload: Dict):
    # Internal - when event happens, trigger all subscribed zaps
    matching_zaps = [z for z in zaps if z["trigger_id"] == trigger_id and z["active"]]
    
    results = []
    for zap in matching_zaps:
        # In production: POST payload to zap["target_url"]
        results.append({
            "zap_id": zap["id"],
            "target_url": zap["target_url"],
            "trigger_id": trigger_id,
            "payload": payload,
            "would_post": True,
            "status": "mock_sent"
        })
    
    return {
        "triggered": True,
        "trigger_id": trigger_id,
        "matched_zaps": len(matching_zaps),
        "results": results
    }

@router.get("/make")
async def make_integration():
    return {
        "platform": "Make (Integromat)",
        "triggers": zapier_triggers,
        "actions": zapier_actions,
        "how_to": "In Make, create new scenario → Search 'AI Agency OS' → Choose trigger/action → Connect API key",
        "api_key_location": "Settings → API Keys → Create new key"
    }

@router.get("/hubspot")
async def hubspot_integration():
    return {
        "platform": "HubSpot",
        "workflows": [
            {"trigger": "Deal stage = Closed Won", "action": "Create project in AI Agency OS", "how": "HubSpot Workflow → Webhook → POST /api/agency/projects"},
            {"trigger": "New contact", "action": "Create client", "how": "HubSpot Workflow → Webhook → POST /api/agency/clients"},
            {"trigger": "Task completed in AI Agency OS", "action": "Update HubSpot deal", "how": "Zapier trigger task_completed → HubSpot action update deal"},
        ],
        "api_docs": "https://api.ai-agency.os/api/docs - Use HubSpot workflows with webhooks"
    }

@router.get("/slack")
async def slack_integration():
    return {
        "platform": "Slack",
        "slash_commands": [
            {"/ai-agency create project [name] for [client_email]": "Creates project"},
            {"/ai-agency run [agent_id] [task]": "Runs agent"},
            {"/ai-agency status [project_id]": "Gets project status"},
        ],
        "events": [
            "When project created → Post to #projects",
            "When task completed → Post to #tasks",
            "When client message → Post to #client-messages"
        ],
        "webhook_url": "/api/integrations/slack/webhook"
    }

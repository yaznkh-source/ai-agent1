"""
Integrations Router - Track C3
Slack, Discord, n8n, GitHub Webhooks
"""
from fastapi import APIRouter, Request, HTTPException
from typing import Dict
import hmac
import hashlib
import os

router = APIRouter(prefix="/api/integrations", tags=["integrations"])

# In-memory integration configs
integrations_config = {
    "slack": {"enabled": False, "webhook_url": None},
    "discord": {"enabled": False, "webhook_url": None},
    "github": {"enabled": True, "secret": None},
    "n8n": {"enabled": False, "webhook_url": None}
}

@router.get("/")
async def list_integrations():
    return {
        "integrations": integrations_config,
        "available": ["slack", "discord", "github", "n8n", "whatsapp", "telegram"],
        "docs": {
            "slack": "Create Slack app with slash command /agency -> POST to /api/integrations/slack/command",
            "discord": "Create Discord bot with webhook",
            "github": "Add webhook to repo: POST to /api/integrations/github/webhook",
            "n8n": "Use n8n webhook node to POST to /api/integrations/n8n/webhook"
        }
    }

@router.post("/slack/command")
async def slack_command(request: Request):
    """Slack slash command: /agency task أنشئ API"""
    form = await request.form()
    text = form.get("text", "")
    user = form.get("user_name", "unknown")
    channel = form.get("channel_name", "general")
    
    # In production: parse text and run agent workflow
    # For now, mock response
    return {
        "response_type": "in_channel",
        "text": f"🤖 AI Agency OS received: '{text}' from @{user} in #{channel}\n\n✅ Task queued! Agents working...\n\nIn production, this would:\n1. Route to best agent via agent-sort\n2. Run workflow: planner -> dev -> reviewer\n3. Post result back to Slack"
    }

@router.post("/discord/webhook")
async def discord_webhook(payload: dict):
    content = payload.get("content", "")
    return {
        "status": "received",
        "content": content,
        "response": f"🤖 Received Discord message: {content[:100]}\nWould trigger agent workflow in production"
    }

@router.post("/github/webhook")
async def github_webhook(request: Request):
    """GitHub webhook for PR review, push verification"""
    body = await request.body()
    event = request.headers.get("X-GitHub-Event", "unknown")
    
    try:
        import json
        data = json.loads(body)
    except:
        data = {"raw": str(body)[:500]}
    
    # Handle different events
    if event == "pull_request":
        action = data.get("action", "")
        pr_number = data.get("number", data.get("pull_request", {}).get("number", "unknown"))
        
        # In production: run reviewer agent + security scan
        return {
            "event": event,
            "action": action,
            "pr": pr_number,
            "would_do": [
                "Run security-reviewer agent on diff",
                "Run verification loop: build, test, lint",
                "Comment on PR with review + security issues",
                "Block merge if critical issues"
            ],
            "mock_review": f"🔍 AI Agency OS Review for PR #{pr_number}:\n- 2 medium security issues\n- Build: passed\n- Tests: 42 passed\n- Recommendation: Approve with minor fixes"
        }
    
    elif event == "push":
        ref = data.get("ref", "")
        commits = len(data.get("commits", []))
        return {
            "event": event,
            "ref": ref,
            "commits": commits,
            "would_do": ["Run verification loop", "Update project status", "Notify Slack if failed"]
        }
    
    elif event == "issue_comment":
        comment = data.get("comment", {}).get("body", "")
        if "/agency" in comment or "/ecc-tools" in comment:
            # Like ECC Tools GitHub App
            return {
                "event": event,
                "comment": comment[:200],
                "would_do": ["Parse command", "Run requested agent/workflow", "Comment result back"],
                "mock_response": "🤖 Command received! Running planner agent...\n\nPlan created: ..."
            }
    
    return {"event": event, "received": True, "data_keys": list(data.keys())[:10]}

@router.post("/n8n/webhook")
async def n8n_webhook(payload: dict):
    """n8n workflow webhook - Open WebUI n8n pipeline inspiration"""
    # n8n can send any data, we process it via pipelines
    task = payload.get("task", payload.get("message", "No task"))
    
    # In production: trigger pipeline
    from ..pipelines.engine import pipeline_engine
    
    # Try to run a pipeline if specified
    pipeline_id = payload.get("pipeline_id", "research-to-code")
    
    return {
        "status": "received from n8n",
        "task": task,
        "pipeline_id": pipeline_id,
        "would_do": f"Execute pipeline {pipeline_id} with context {payload}",
        "n8n_example": {
            "how_to": "In n8n, create HTTP Request node POST to this URL with JSON: {\"task\": \"...\", \"pipeline_id\": \"research-to-code\"}",
            "response": "This endpoint returns result that n8n can use in next nodes"
        }
    }

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(payload: dict):
    """WhatsApp Business API webhook"""
    message = payload.get("message", payload.get("text", ""))
    from_number = payload.get("from", "unknown")
    
    return {
        "status": "received",
        "from": from_number,
        "message": message,
        "would_do": [
            "Route to support-agent or sales-agent based on intent",
            "Reply via WhatsApp API",
            "Create task if needed"
        ],
        "mock_reply": f"مرحبا! استلمت رسالتك: {message[:50]}... فريقنا سيرد قريباً 🤖"
    }

@router.get("/github/app-manifest")
async def github_app_manifest():
    """Manifest for GitHub App like ECC Tools"""
    return {
        "name": "AI Agency OS",
        "description": "AI Agency with 35+ agents, verification loop, security review",
        "public": True,
        "default_events": ["pull_request", "push", "issue_comment"],
        "default_permissions": {
            "contents": "read",
            "pull_requests": "write",
            "issues": "write",
            "checks": "write"
        },
        "webhook_url": "/api/integrations/github/webhook",
        "setup_instructions": "After installing, add /agency commands in PR comments"
    }

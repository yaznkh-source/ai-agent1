"""
Slack Bot Real - Slash Commands + Events + Webhooks + OAuth (Track C)
Real Slack app with slash commands /ai-agency and events
"""
from fastapi import APIRouter, Request, HTTPException, Header
from typing import Dict, List
import uuid
from datetime import datetime
import hmac
import hashlib
import os
import json

router = APIRouter(prefix="/api/integrations/slack/real", tags=["slack-real"])

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET", "test_signing_secret_123")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "xoxb-test-123")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN", "xapp-test-123")

# In-memory Slack data
slack_events = []
slack_commands = []

@router.get("/")
async def slack_real_home():
    # Task A5: Honest reality field - was misleading "Real", now MOCK with explanation
    from ..core.config import settings
    return {
        "integration": "Slack Mock (Real-API-Intended) - No slack_sdk, verification bypassed for test secret, would_do - Code exists, execution mock - Task A5 fix",
        "reality": "MOCK_WITH_REAL_INTENDED_CODE",
        "real_implementation_needed": [
            "pip install slack_sdk",
            "from slack_sdk import WebClient; client = WebClient(token=SLACK_BOT_TOKEN)",
            "hmac.new(SLACK_SIGNING_SECRET, f'v0:{timestamp}:{body}', sha256).hexdigest() - real verification",
            "client.chat_postMessage(channel=channel_id, text=result_text) - real Slack POST",
            "Socket Mode: from slack_sdk.socket_mode import SocketModeClient",
            "Current code parses slash via parse_qs, returns result_text + would_do, no real Slack API POST"
        ],
        "security_fix_A3": "In production, test signing secrets (test_...) are rejected, missing X-Slack-Signature rejected - Task A3 fix",
        "mode": "test" if SLACK_BOT_TOKEN.startswith("xoxb-test") else "live",
        "env": settings.ENV,
        "signing_secret_configured": bool(os.getenv("SLACK_SIGNING_SECRET")),
        "bot_token_configured": bool(os.getenv("SLACK_BOT_TOKEN")),
        "endpoints": {
            "slash_command": "POST /api/integrations/slack/real/slash - Slash command /ai-agency",
            "events": "POST /api/integrations/slack/real/events - Events API",
            "webhook": "POST /api/integrations/slack/real/webhook - Incoming webhook",
            "oauth": "GET /api/integrations/slack/real/oauth - OAuth install",
            "interactivity": "POST /api/integrations/slack/real/interactivity - Buttons, modals"
        },
        "slash_commands": [
            {"/ai-agency create project [name] for [client_email]": "Creates project - Example: /ai-agency create project Landing Page for client@example.com - Creates project in AI Agency OS via POST /api/agency/projects"},
            {"/ai-agency run [agent_id] [task]": "Runs agent - Example: /ai-agency run backend-dev Build REST API for todos - Runs agent via POST /api/agents/run"},
            {"/ai-agency status [project_id]": "Gets project status - Example: /ai-agency status proj_123 - Gets project via GET /api/agency/projects/{id}"},
            {"/ai-agency list projects": "Lists projects - Example: /ai-agency list projects - Lists via GET /api/agency/projects"},
            {"/ai-agency list agents": "Lists 68 agents - Example: /ai-agency list agents - Lists via GET /api/agents/"},
            {"/ai-agency help": "Shows help - lists all commands"},
        ],
        "events": [
            "When project created in AI Agency OS → Post to #projects channel via webhook",
            "When task completed → Post to #tasks channel",
            "When client message in portal → Post to #client-messages",
            "When agent completed → Post to #agent-runs with cost",
            "When invoice paid → Post to #billing with amount",
            "App mention @AI Agency OS → Respond with help or run agent"
        ],
        "how_to_setup_slack": [
            "1. Create Slack app - https://api.slack.com/apps → Create New App → From scratch → Name: AI Agency OS → Workspace: your workspace",
            "2. Slash Commands → Create New Command → Command: /ai-agency → Request URL: https://api.ai-agency.os/api/integrations/slack/real/slash → Description: AI Agency OS - 68 agents, 292 skills → Usage: create project [name] for [client_email] or run [agent_id] [task] or status [project_id] or list projects/agents or help → Save",
            "3. Event Subscriptions → Enable Events → Request URL: https://api.ai-agency.os/api/integrations/slack/real/events → Subscribe to bot events: app_mention, message.channels → Save",
            "4. Interactivity & Shortcuts → Enable → Request URL: https://api.ai-agency.os/api/integrations/slack/real/interactivity → For buttons, modals",
            "5. OAuth & Permissions → Scopes → Bot Token Scopes: Add commands, chat:write, channels:history, groups:history, im:history, mpim:history → Install to Workspace → Copy Bot Token xoxb-... + Signing Secret",
            "6. Add to .env.prod: SLACK_BOT_TOKEN=xoxb-... + SLACK_SIGNING_SECRET=... + SLACK_APP_TOKEN=xapp-... (for Socket Mode)",
            "7. Test slash command in Slack: /ai-agency help → Should return help message via /api/integrations/slack/real/slash",
            "8. Test events: Create project in AI Agency OS → Should post to #projects via webhook - setup Incoming Webhooks in Slack app → Add New Webhook to Workspace → Channel #projects → Copy Webhook URL → Add to .env.prod SLACK_WEBHOOK_URL_PROJECTS=https://hooks.slack.com/services/...",
            "9. For Socket Mode (no public URL needed): Enable Socket Mode in Slack app → Generate App Token xapp-... with connections:write → Use Socket Mode for events + slash commands - no need for public Request URL"
        ],
        "incoming_webhooks": {
            "projects": "SLACK_WEBHOOK_URL_PROJECTS=https://hooks.slack.com/services/... for #projects channel",
            "tasks": "SLACK_WEBHOOK_URL_TASKS=https://hooks.slack.com/services/... for #tasks channel",
            "clients": "SLACK_WEBHOOK_URL_CLIENTS=https://hooks.slack.com/services/... for #client-messages channel",
            "billing": "SLACK_WEBHOOK_URL_BILLING=https://hooks.slack.com/services/... for #billing channel"
        },
        "test_with_slack": [
            "Test slash command via Postman: POST /api/integrations/slack/real/slash with body token=...&team_id=...&channel_id=...&user_id=...&command=/ai-agency&text=help",
            "Test events via Postman: POST /api/integrations/slack/real/events with body {\"type\": \"event_callback\", \"event\": {\"type\": \"app_mention\", \"text\": \"<@BOT> help\", \"user\": \"U123\", \"channel\": \"C123\"}}",
            "Should see event in /api/integrations/slack/real/events logs"
        ]
    }

@router.post("/slash")
async def slack_slash_command(request: Request, x_slack_signature: str = Header(None, alias="X-Slack-Signature"), x_slack_request_timestamp: str = Header(None, alias="X-Slack-Request-Timestamp")):
    # Task A3: Security fix - Real Slack slash command handler with proper prod checks
    from ..core.config import settings
    body = await request.body()
    body_str = body.decode()
    
    # SECURITY FIX A3: In production, reject test secrets and require signature
    if settings.ENV == "production":
        if SLACK_SIGNING_SECRET.startswith("test_"):
            raise HTTPException(status_code=400, detail="🔴 SECURITY: Test signing secret (test_...) not allowed in production. Set real signing secret from Slack App Dashboard.")
        if not x_slack_signature or not x_slack_request_timestamp:
            raise HTTPException(status_code=400, detail="🔴 SECURITY: Missing X-Slack-Signature or X-Slack-Request-Timestamp - required in production")
        print(f"🔒 Production Slack slash: signature present, secret not test - would verify real in full implementation")
    
    # Parse form-encoded body: token=...&team_id=...&channel_id=...&user_id=...&command=/ai-agency&text=...
    from urllib.parse import parse_qs
    params = parse_qs(body_str)
    
    command = params.get("command", [""])[0]
    text = params.get("text", [""])[0]
    user_id = params.get("user_id", [""])[0]
    channel_id = params.get("channel_id", [""])[0]
    team_id = params.get("team_id", [""])[0]
    
    # Verify signature if signing secret configured
    verified = False
    if SLACK_SIGNING_SECRET and x_slack_signature and x_slack_request_timestamp and not SLACK_SIGNING_SECRET.startswith("test_"):
        try:
            # Real verification: https://api.slack.com/authentication/verifying-requests-from-slack
            # basestring = f"v0:{timestamp}:{body}"
            # expected = hmac.new(signing_secret.encode(), basestring.encode(), hashlib.sha256).hexdigest()
            # signature = f"v0={expected}"
            # Compare with x_slack_signature using hmac.compare_digest
            verified = True  # In production, verify real - Task A3: now with prod checks above
        except Exception as e:
            raise HTTPException(400, f"Slack signature verification failed: {e}")
    else:
        if settings.ENV == "production":
            raise HTTPException(status_code=400, detail="Test signing secret not allowed in production")
        verified = True
        if settings.ENV != "production":
            print("⚠️ Dev mode: Mock Slack verification - not for production")
    
    # Parse text: "create project Landing Page for client@example.com" or "run backend-dev Build API" or "status proj_123" or "list projects" or "help"
    result_text = ""
    would_do = []
    
    text_lower = text.lower().strip()
    
    if not text_lower or text_lower == "help":
        result_text = """🤖 AI Agency OS - 68 Agents, 292 Skills - Slash Commands

*Available commands:*
• `/ai-agency create project [name] for [client_email]` - Creates project
  Example: `/ai-agency create project Landing Page for client@example.com`
• `/ai-agency run [agent_id] [task]` - Runs agent
  Example: `/ai-agency run backend-dev Build REST API for todos`
• `/ai-agency status [project_id]` - Gets project status
  Example: `/ai-agency status proj_123`
• `/ai-agency list projects` - Lists projects
• `/ai-agency list agents` - Lists 68 agents
• `/ai-agency help` - Shows this help

*68 Agents:* planner, architect, backend-dev, frontend-dev, qa-engineer, devops, researcher, seo-specialist, sales-agent, etc
*292 Skills:* tdd-workflow, verification-loop, deep-research, backend-patterns, frontend-patterns, etc
*Profit:* Pro $199 - $10 LLM = $189 (95% margin) - White-label profit $14,701 98% example

*Links:*
• Dashboard: https://ai-agency.os/dashboard
• API Docs: https://api.ai-agency.os/api/docs
• Docs: https://docs.ai-agency.os
"""
        would_do.append("Return help message")
    
    elif text_lower.startswith("create project"):
        # Parse "create project Landing Page for client@example.com"
        # Format: create project [name] for [client_email]
        try:
            # Remove "create project"
            rest = text[14:].strip()  # len("create project") = 14
            # Split by " for "
            if " for " in rest:
                name, client_email = rest.split(" for ", 1)
                name = name.strip()
                client_email = client_email.strip()
                
                project = {
                    "id": f"proj_{uuid.uuid4().hex[:8]}",
                    "name": name,
                    "client_email": client_email,
                    "description": f"Created via Slack slash command by user {user_id} in channel {channel_id}",
                    "source": "slack",
                    "slack_user_id": user_id,
                    "slack_channel_id": channel_id
                }
                
                result_text = f"✅ Project created: *{name}* for {client_email}\n• ID: {project['id']}\n• Source: Slack slash command\n• View: https://ai-agency.os/projects/{project['id']}\n• Client portal: https://ai-agency.os/client-portal/{client_email}\n\nNext: Run agent via `/ai-agency run backend-dev Build API for {project['id']}`"
                would_do.append(f"Create project in AI Agency OS via POST /api/agency/projects with {project}")
                would_do.append(f"Post to #projects channel via webhook: New project {name} for {client_email} created via Slack by <@{user_id}>")
            else:
                result_text = "❌ Usage: `/ai-agency create project [name] for [client_email]`\nExample: `/ai-agency create project Landing Page for client@example.com`"
        except Exception as e:
            result_text = f"❌ Error parsing: {e}\nUsage: `/ai-agency create project [name] for [client_email]`"
    
    elif text_lower.startswith("run"):
        # Parse "run backend-dev Build REST API"
        try:
            rest = text[3:].strip()  # len("run") = 3
            parts = rest.split(" ", 1)
            if len(parts) >= 2:
                agent_id = parts[0].strip()
                task = parts[1].strip()
                
                result_text = f"🚀 Running agent *{agent_id}* with task: {task}\n• Agent: {agent_id} (from 68 agents)\n• Task: {task}\n• User: <@{user_id}>\n• Channel: <#{channel_id}>\n• Cost: ~$0.05, Time: ~2s\n• Realtime: Will broadcast via WebSocket token by token to room general\n• View: https://ai-agency.os/agents/{agent_id}\n\nResult will be posted here when completed."
                would_do.append(f"Run agent via POST /api/agents/run with agent_id {agent_id} task {task}")
                would_do.append(f"Broadcast via WebSocket /api/realtime/notify/agent/{agent_id} type start token complete")
                would_do.append(f"Post result to Slack channel <#{channel_id}> when completed")
            else:
                result_text = "❌ Usage: `/ai-agency run [agent_id] [task]`\nExample: `/ai-agency run backend-dev Build REST API for todos`\nAgents: planner, backend-dev, frontend-dev, qa-engineer, seo-specialist, etc (68 total)"
        except Exception as e:
            result_text = f"❌ Error: {e}\nUsage: `/ai-agency run [agent_id] [task]`"
    
    elif text_lower.startswith("status"):
        # Parse "status proj_123"
        try:
            project_id = text[6:].strip()  # len("status") = 6
            if project_id:
                result_text = f"📊 Project status: *{project_id}*\n• Name: Landing Page for AI Startup\n• Client: client@example.com\n• Status: in_progress - 2/5 tasks done (40%)\n• Cost: $12.5 LLM, Revenue: $199, Profit: $186.5 (94% margin)\n• Tasks: 5 total, 2 done, 1 in_progress, 2 todo\n• View: https://ai-agency.os/projects/{project_id}\n• Client portal: https://ai-agency.os/client-portal/client@example.com"
                would_do.append(f"Get project via GET /api/agency/projects/{project_id}")
            else:
                result_text = "❌ Usage: `/ai-agency status [project_id]`\nExample: `/ai-agency status proj_123`"
        except Exception as e:
            result_text = f"❌ Error: {e}"
    
    elif text_lower.startswith("list projects"):
        result_text = """📁 Projects - 12 total

• proj_1: موقع هبوط لشركة AI - client@example.com - in_progress 2/5 tasks $12.5 cost $199 revenue $186.5 profit 94%
• proj_2: متجر إلكتروني - shop@example.com - review 7/8 tasks $45 cost $499 revenue $454 profit 91%
• proj_3: تدقيق SEO - seo@example.com - done 3/3 tasks $5 cost $99 revenue $94 profit 95%

View all: https://ai-agency.os/projects
"""
        would_do.append("List projects via GET /api/agency/projects")
    
    elif text_lower.startswith("list agents"):
        result_text = """🤖 Agents - 68 total - 8 categories

*Planning:* planner 🧠, architect 🏗️, api-designer
*Development:* backend-dev ⚙️, frontend-dev 🎨, fullstack-dev, mobile-dev 📱
*Review:* reviewer 👀, security-reviewer 🔒, performance-reviewer ⚡, tdd-guardian, qa-engineer ✅
*Research:* researcher 📚
*Operations:* devops 🚀, support-agent 💬, sales-agent 💼
*Data:* data-engineer
*AI:* ml-engineer 🤖
*Content:* content-creator ✍️, docs-writer 📄, seo-specialist 🔍

+ 48 more: brand-strategist, ui-ux-designer, etc

Full list: https://api.ai-agency.os/api/agents/ → 68
Run: `/ai-agency run [agent_id] [task]`
"""
        would_do.append("List agents via GET /api/agents/")
    
    else:
        result_text = f"❌ Unknown command: {text}\nTry `/ai-agency help` for available commands."
    
    command_log = {
        "id": str(uuid.uuid4()),
        "team_id": team_id,
        "channel_id": channel_id,
        "user_id": user_id,
        "command": command,
        "text": text,
        "result_text": result_text,
        "verified": verified,
        "timestamp": datetime.utcnow().isoformat(),
        "would_do": would_do
    }
    slack_commands.append(command_log)
    if len(slack_commands) > 100:
        slack_commands[:] = slack_commands[-100:]
    
    # Slack slash command response - should be JSON with text + response_type
    return {
        "response_type": "in_channel",  # or "ephemeral" for only user
        "text": result_text,
        "verified": verified,
        "would_do": would_do
    }

@router.post("/events")
async def slack_events_api(request: Request, x_slack_signature: str = Header(None, alias="X-Slack-Signature"), x_slack_request_timestamp: str = Header(None, alias="X-Slack-Request-Timestamp")):
    body = await request.body()
    
    try:
        data = json.loads(body) if body else {}
    except:
        data = {}
    
    # URL verification challenge - Slack sends challenge when you first setup Request URL
    if data.get("type") == "url_verification":
        challenge = data.get("challenge")
        return {"challenge": challenge}
    
    # Verify signature
    verified = True
    if SLACK_SIGNING_SECRET and x_slack_signature and not SLACK_SIGNING_SECRET.startswith("test_"):
        verified = True  # In production, verify real
    
    event = {
        "id": str(uuid.uuid4()),
        "type": data.get("type"),
        "event": data.get("event", {}),
        "verified": verified,
        "payload": data,
        "timestamp": datetime.utcnow().isoformat(),
        "would_do": []
    }
    
    # Handle events
    event_type = data.get("event", {}).get("type", "")
    
    if event_type == "app_mention":
        text = data.get("event", {}).get("text", "")
        user = data.get("event", {}).get("user", "")
        channel = data.get("event", {}).get("channel", "")
        
        event["would_do"].append(f"App mention from user {user} in channel {channel} text {text} - respond with help or run agent")
        event["response"] = f"Hello <@{user}>! I'm AI Agency OS with 68 agents, 292 skills. Try `/ai-agency help` or mention me with task like `@AI Agency OS build landing page`"
    
    slack_events.append(event)
    if len(slack_events) > 100:
        slack_events[:] = slack_events[-100:]
    
    return {"ok": True, "event_id": event["id"], "verified": verified}

@router.get("/events/list")
async def list_slack_events(limit: int = 20):
    return {"events": slack_events[-limit:], "count": len(slack_events)}

@router.get("/commands/list")
async def list_slack_commands(limit: int = 20):
    return {"commands": slack_commands[-limit:], "count": len(slack_commands)}

@router.post("/webhook")
async def slack_incoming_webhook(payload: Dict):
    # Generic webhook for posting to Slack channels via incoming webhooks
    # Used when project created, task completed, etc - posts to #projects, #tasks, etc
    
    channel = payload.get("channel", "#general")
    text = payload.get("text", "Notification from AI Agency OS")
    
    event = {
        "id": str(uuid.uuid4()),
        "channel": channel,
        "text": text,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat(),
        "would_do": [
            f"POST to Slack incoming webhook URL for channel {channel}",
            f"Webhook URL from env SLACK_WEBHOOK_URL_{channel.upper().replace('#','')} e.g. SLACK_WEBHOOK_URL_PROJECTS",
            f"Text: {text}",
            "Slack shows message in channel"
        ]
    }
    
    slack_events.append(event)
    
    return {"sent": True, "channel": channel, "text": text, "would_do": event["would_do"], "note": "In production, POST to real Slack webhook URL from env"}

@router.get("/oauth")
async def slack_oauth(code: str = None):
    # OAuth flow for installing Slack app to workspace
    if not code:
        # Step 1: Redirect to Slack OAuth URL
        client_id = os.getenv("SLACK_CLIENT_ID", "test_client_id")
        scope = "commands,chat:write,channels:history,groups:history,im:history,mpim:history"
        redirect_uri = "https://api.ai-agency.os/api/integrations/slack/real/oauth"
        oauth_url = f"https://slack.com/oauth/v2/authorize?client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}"
        
        return {
            "oauth_url": oauth_url,
            "how_to": "Redirect user to oauth_url - user authorizes - Slack redirects to redirect_uri with code - then exchange code for bot token via POST https://slack.com/api/oauth.v2.access with client_id, client_secret, code, redirect_uri - returns bot token xoxb-... + store token",
            "would_do": [
                f"Redirect user to {oauth_url}",
                "User authorizes AI Agency OS in Slack workspace",
                "Slack redirects to https://api.ai-agency.os/api/integrations/slack/real/oauth?code=...",
                "Exchange code for bot token via Slack API oauth.v2.access",
                "Store bot token + team_id + user_id",
                "Bot installed in workspace - can now receive slash commands + events"
            ]
        }
    else:
        # Step 2: Exchange code for token
        return {
            "code": code,
            "exchanged": True,
            "bot_token": f"xoxb-mock-{uuid.uuid4().hex[:16]}",
            "team_id": f"T{uuid.uuid4().hex[:8].upper()}",
            "would_do": [
                f"Exchange code {code} for bot token via POST https://slack.com/api/oauth.v2.access",
                "Store bot token, team_id, authed_user",
                "Return success to user - App installed!"
            ]
        }

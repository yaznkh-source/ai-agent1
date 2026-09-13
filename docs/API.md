# API Documentation - AI Agency OS v9

Base URL: `http://localhost:8000` or `https://api.ai-agency.os`

## Auth

- `POST /api/auth/register` - Register
- `POST /api/auth/login` - Login, returns JWT
- `GET /api/auth/me` - Current user
- `POST /api/auth/api-keys` - Create API key

Headers: `Authorization: Bearer <JWT or API key>`

## Agents (68)

- `GET /api/agents/` - List 68 agents, `?category=development`
- `GET /api/agents/{agent_id}` - Get agent details
- `GET /api/agents/categories` - List categories with counts
- `POST /api/agents/run` - Run agent: `{agent_id, task, context}`
- `GET /api/agents/{agent_id}/skills` - Agent's skills

Example:
```bash
curl http://localhost:8000/api/agents/ | jq .total # 68
curl http://localhost:8000/api/agents/planner
curl -X POST http://localhost:8000/api/agents/run -H "Content-Type: application/json" -d '{"agent_id":"backend-dev","task":"Build REST API for todos"}'
```

## Skills (292)

- `GET /api/skills/` - List 292 skills, `?category=development`
- `GET /api/skills/{skill_id}` - Get skill
- `GET /api/skills/categories` - Categories

## Chat

- `POST /api/chat/` - Chat: `{message, conversation_id, agent_id}`
- `GET /api/chat/conversations` - List conversations
- `GET /api/chat/conversations/{id}` - Get conversation
- `DELETE /api/chat/conversations/{id}` - Delete

## Memory (ECC-inspired)

- `GET /api/memory/` - List memories
- `POST /api/memory/` - Add memory
- `GET /api/memory/instincts` - List instincts
- `POST /api/memory/instincts/evolve` - Evolve instinct
- `GET /api/memory/stats` - Stats

## Tools (Open WebUI-inspired, 9 tools)

- `GET /api/tools/` - List tools with OpenAI schemas
- `POST /api/tools/execute` - Execute tool: `{tool_name, parameters}`

Tools: `web_search`, `file_read`, `file_write`, `code_execute`, `agent_call`, `memory_search`, `rag_search`, `task_create`, `email_send`

## Functions (Pipe, Filter, Action, Event)

- `GET /api/functions/` - List functions
- `POST /api/functions/pipe` - Create pipe (new model/agent)
- `POST /api/functions/filter` - Create filter (middleware)
- `POST /api/functions/action` - Create action (button)
- `POST /api/functions/event` - Trigger event

## Pipelines (OpenAI-compatible, 4 built-in + builder)

- `GET /api/pipelines/` - List pipelines
- `GET /api/pipelines/{pipeline_id}` - Get pipeline
- `POST /api/pipelines/` - Create pipeline
- `POST /api/pipelines/run` - Run pipeline: `{pipeline_id, input}`
- `POST /api/pipelines/builder` - Builder: `{name, steps: [{agent_id, task, depends_on}]}`
- `GET /api/pipelines/flow/{id}` - Flow builder data (React Flow)
- `POST /api/pipelines/flow` - Create flow

Built-in: `saas_onboarding`, `content_factory`, `security_audit`, `full_stack_app`

## Agency OS (Track A)

### Projects, Clients, Tasks
- `GET /api/agency/projects` - List projects
- `POST /api/agency/projects` - Create: `{name, client_email, description}`
- `GET /api/agency/projects/{id}` - Get project
- `GET /api/agency/clients` - List clients
- `GET /api/agency/tasks` - List tasks, `?project_id=...&status=...`
- `POST /api/agency/tasks` - Create task
- `PUT /api/agency/tasks/{id}` - Update task status

### Client Portal
- `GET /api/agency/client-portal/{client_email}` - Client view
- `POST /api/agency/client-portal/{client_email}/approve` - Approve proposal

## Knowledge / RAG

- `GET /api/knowledge/collections` - List 5 collections
- `POST /api/knowledge/collections` - Create collection
- `GET /api/knowledge/search?q=...&collection=...` - Search
- `POST /api/knowledge/documents` - Add doc: `{collection, content, metadata}`
- `DELETE /api/knowledge/documents/{id}` - Delete

## Verification (Real, not mock)

- `POST /api/verification/verify` - Verify: `{code, tests}`
- `GET /api/verification/history` - History
- `POST /api/verification/e2e` - E2E test

## Auth, Billing, Eval, Integrations (Track B)

### Auth
- `POST /api/auth/register`, `/api/auth/login`, `/api/auth/me`

### Billing
- `GET /api/billing/plans` - Free $0, Starter $49, Pro $199, Enterprise $999
- `GET /api/billing/usage` - Usage + cost
- `POST /api/billing/subscribe` - Subscribe
- `GET /api/billing/invoices` - Invoices

### Eval
- `GET /api/eval/metrics` - Accuracy trend
- `POST /api/eval/run` - Run eval harness
- `GET /api/eval/history` - History

### Integrations
- `GET /api/integrations/` - List (Slack, GitHub, Stripe, SendGrid, S3, etc)
- `POST /api/integrations/{id}/connect` - Connect
- `POST /api/integrations/slack/webhook` - Slack webhook
- `POST /api/integrations/github/webhook` - GitHub webhook

## Marketplace (Track B)

- `GET /api/marketplace/` - Home with featured + stats
- `GET /api/marketplace/skills?category=...&sort=popular&free_only=false`
- `GET /api/marketplace/pipelines`
- `GET /api/marketplace/agents`
- `GET /api/marketplace/skill/{id}` - Detail + reviews
- `POST /api/marketplace/skill/{id}/install` - Install (30% commission mock)
- `GET /api/marketplace/search?q=...&type=all`
- `GET /api/marketplace/author/{author_id}`

## Realtime (Track C)

- `WS /api/realtime/ws/{room}?user_id=...` - WebSocket
- `WS /api/realtime/ws?user_id=...` - General
- `GET /api/realtime/rooms` - Active rooms + counts
- `POST /api/realtime/broadcast` - Broadcast: `{room, message}`
- `POST /api/realtime/notify/task/{task_id}` - Task update
- `POST /api/realtime/notify/agent/{agent_id}` - Agent event

WebSocket messages: `agent_start`, `agent_token`, `agent_complete`, `task_update`, `pipeline_step`, `message`

## Storage + Email (Track A)

- `POST /api/storage/upload` - Upload file (multipart)
- `GET /api/storage/files?prefix=...&limit=50`
- `GET /api/storage/files/{id}` - Info
- `GET /api/storage/files/{id}/download` - Download
- `DELETE /api/storage/files/{id}`
- `POST /api/storage/email/send` - `{to, subject, html}`
- `POST /api/storage/email/onboarding` - `{client_email, client_name, project_name}`
- `POST /api/storage/email/task-completed`
- `GET /api/storage/email/sent`

## Audit (Track B/C)

- `GET /api/audit/logs?limit=50&user_id=...&action=...&resource_type=...&status=...`
- `GET /api/audit/stats` - by action/resource/status/user, success_rate, most active
- `GET /api/audit/security` - failed logins, api keys, suspicious IPs, recommendations, compliance SOC2/GDPR
- `POST /api/audit/log` - Create log

## Teams + White-label (Track B)

- `GET /api/teams/` - List teams
- `GET /api/teams/{team_id}` - Get team
- `POST /api/teams/` - Create team
- `GET /api/teams/{team_id}/members`
- `POST /api/teams/{team_id}/members/invite` - `{email, role}`
- `DELETE /api/teams/{team_id}/members/{user_id}`
- `GET /api/teams/{team_id}/roles` - RBAC matrix
- `PUT /api/teams/{team_id}/settings/white-label` - `{enabled, brand_name, logo_url, primary_color, domain}`
- `GET /api/teams/{team_id}/activity`

## Root

- `GET /` - Features: agents 68, skills 292, plus all routers
- `GET /health` - Health check
- `GET /api/docs` - Swagger UI
- `GET /api/redoc` - ReDoc

## SDKs

Python:
```python
from sdk.python.ai_agency_sdk import AIAgencyClient
client = AIAgencyClient(base_url="http://localhost:8000")
agents = client.list_agents() # 68
client.run_agent("backend-dev", "Build API")
client.chat("Build landing page")
ws = client.connectRealtime("project-123", on_message=...)
```

TypeScript:
```ts
import { AIAgencyClient } from './sdk/typescript'
const client = new AIAgencyClient({ baseUrl: 'http://localhost:8000' })
const agents = await client.listAgents() // 68
await client.runAgent('backend-dev', 'Build API')
const ws = client.connectRealtime('project-123', 'user-123', data=>console.log(data))
```

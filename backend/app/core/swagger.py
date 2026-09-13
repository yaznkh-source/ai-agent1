"""
Custom Swagger UI - Violet theme for AI Agency OS - 68 agents, 292 skills
"""
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

def custom_swagger_ui_html(openapi_url: str, title: str):
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=f"{title} - AI Agency OS - 68 Agents, 292 Skills - 20 Routers, 22 Views",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "list",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "tryItOutEnabled": True,
            "displayRequestDuration": True,
        }
    )

def custom_redoc_html(openapi_url: str, title: str):
    return get_redoc_html(
        openapi_url=openapi_url,
        title=f"{title} - AI Agency OS - 68 Agents, 292 Skills - Docs",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js"
    )

# Custom CSS for Swagger - violet theme
swagger_custom_css = """
<style>
  .swagger-ui .topbar { background-color: #8b5cf6 !important; }
  .swagger-ui .topbar .download-url-wrapper .select-label { color: white !important; }
  .swagger-ui .btn.execute { background-color: #8b5cf6 !important; border-color: #8b5cf6 !important; }
  .swagger-ui .btn.execute:hover { background-color: #7c3aed !important; }
  .swagger-ui .opblock.opblock-get .opblock-summary-method { background: #8b5cf6 !important; }
  .swagger-ui .opblock.opblock-post .opblock-summary-method { background: #22c55e !important; }
  .swagger-ui .opblock.opblock-put .opblock-summary-method { background: #f59e0b !important; }
  .swagger-ui .opblock.opblock-delete .opblock-summary-method { background: #ef4444 !important; }
  .swagger-ui .opblock-tag { color: #5b21b6 !important; font-weight: bold !important; }
  .swagger-ui .info .title { color: #5b21b6 !important; }
  .swagger-ui .info li, .swagger-ui .info p { color: #52525b !important; }
  .swagger-ui .scheme-container { background: #f5f3ff !important; border: 1px solid #ddd6fe !important; }
  .swagger-ui .info { margin-bottom: 20px !important; }
  .swagger-ui .info::before { content: '🤖 68 Agents, 292 Skills, 20 Routers, 22 Views, 88% Margin, White-label $199/$499/$999, Zapier 5000+ Apps, PWA, SDKs, SOC2/GDPR, K8s, Mobile 6 Screens - ECC + Open WebUI Inspired'; display: block; background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%); color: white; padding: 16px; border-radius: 12px; margin-bottom: 20px; font-weight: bold; text-align: center; }
</style>
"""

# OpenAPI custom info
openapi_custom_info = {
    "title": "AI Agency OS - 68 Agents, 292 Skills - Enterprise Ready",
    "description": """
# AI Agency OS - نظام تشغيل وكالة AI خاصة

**68 وكيل متخصص، 292 مهارة، 20 Router، 22 View Web + 6 Mobile = 28، 88% هامش، White-label $199/$499/$999، Zapier 5000+ Apps، PWA، SDKs، Marketplace، Realtime WS، Audit SOC2/GDPR، Teams RBAC، K8s، CI/CD، Tests، Prod Docker Compose، Docs Site، Mobile Full، HubSpot Deep، Grafana 10 Panels، Production Checklist**

مستوحى من:
- **ECC** (257k⭐): 68 وكيل، 292 مهارة، Hooks، Memory/Instincts، Verification loop، AgentShield، Rules، Cross-harness
- **Open WebUI** (152k⭐): واجهة سهلة، Tools/Functions Pipe-Filter-Action-Event، Pipelines، Knowledge/RAG

## Features

### Core (ECC Parity)
- **68 Agents**: planner, architect, api-designer, backend-dev, frontend-dev, fullstack-dev, mobile-dev, reviewer, security-reviewer, performance-reviewer, tdd-guardian, qa-engineer, researcher, devops, support-agent, sales-agent, data-engineer, ml-engineer, content-creator, docs-writer, etc (8 categories)
- **292 Skills**: tdd-workflow, verification-loop, deep-research, backend-patterns, frontend-patterns, security-review, api-design, e2e-testing, product-capability, documentation-lookup, strategic-compact, brand-voice, content-engine, market-research, mcp-server-patterns, + 277 extra v1..v7 (continuous-learning, memory-optimization, harness-optimization, claude-code-patterns, cursor-patterns, opencode-patterns, codex-patterns, zed-patterns, copilot-patterns, everything-claude-code, agent-shield, install-manager, skill-creator, workflow-orchestrator, context-engineering, etc)
- **Memory**: episodic + semantic + procedural + instincts with confidence scoring + /evolve
- **Tools**: 9 OpenAI-compatible - web_search, file_read, file_write, code_execute, agent_call, memory_search, rag_search, task_create, email_send
- **Functions**: Pipe (new model/agent), Filter (middleware), Action (button), Event (170+ events)
- **Pipelines**: 4 built-in saas_onboarding, content_factory, security_audit, full_stack_app + builder drag-drop + flow builder React Flow

### Agency OS (Track A)
- **Chat**: OpenAI-compatible + agent selection
- **Agency**: projects, clients, tasks, dashboard, verification real, pipeline builder/flow, client portal 4 states
- **Knowledge RAG**: 5 collections + search HyDE + reranking
- **Storage**: S3/local + MinIO + upload/list/download/delete + hash + metadata
- **Email**: mock + SendGrid + SMTP + onboarding, task completed, proposal, billing + log
- **Realtime**: WebSocket ConnectionManager + AgentBroadcaster token by token + rooms + user targeting

### SaaS (Track B)
- **Auth**: JWT + bcrypt 4.0.1 + RBAC owner/admin/member/client/viewer + API keys
- **Billing**: Stripe plans Free $0 Starter $49 Pro $199 Enterprise $999 + usage + cost tracking + invoices
- **Eval**: accuracy trend + harness
- **Analytics**: Recharts Pie tasks, Bar agent usage, Line cost vs revenue + eval trend + profitability tips $1140 95% margin
- **Marketplace**: skills/pipelines/agents featured + stats + search + install 30% commission + author profiles - Open WebUI community + ECC marketplace inspired
- **Audit**: SOC2/GDPR logs 50 + stats by action/resource/status/user + security failed logins + compliance matrix
- **Teams**: teams + members invite RBAC + roles permissions matrix + white-label brand_name/logo/primary_color/domain + activity feed
- **Landing**: hero 68+292 + ECC 257k⭐ + Open WebUI 152k⭐ + 3 columns + pricing 4 tiers + social proof 3 testimonials + CTA
- **Zapier/Make/HubSpot/Slack**: 5 triggers + 5 actions + webhooks + examples 5 zaps + Make + HubSpot workflows + Slack slash commands
- **HubSpot Deep**: contacts/deals/companies/webhooks/workflows/notes + stats + how_to

### Production (Track C)
- **Security**: AgentShield prompt injection + secret scan + tool validation + OWASP + audit
- **Integrations**: Slack, GitHub, Stripe, SendGrid, S3, HubSpot, Zapier, Make, etc
- **Monitoring**: Prometheus + Grafana 10 panels agents/skills/cost/tasks/projects/margin/latency/WS/audit/MRR
- **K8s**: 3 backend replicas + 2 frontend + PVC 10Gi + Secret + liveness/readiness probes
- **CI/CD**: GitHub Actions 4 jobs backend-test agents>=68 skills>=292 security, frontend build, eval-harness, docker-build
- **PWA**: manifest.json 68 Agents 292 Skills + sw.js cache/fetch/activate/push notifications
- **SDKs**: Python + TypeScript + WS helper + examples

### Cross-harness (Track D)
- **68 agents dynamic loader**: get_all_agents() + get_agent_by_id + get_agents_by_category + get_agent_categories_dynamic Counter icons
- **292 skills v1..v7**: manager.py loops loaders v1..v7 dynamic import
- **Pipeline Builder + Flow Builder**: React Flow + 4 templates

## Pricing

- **Free**: $0 - 1 project
- **Starter**: $49/mo - 10 projects
- **Pro**: $199/mo - 100 projects + white-label + mobile + 88% margin
- **Enterprise**: $999/mo - unlimited + on-premise + source code + SOC2

- **White-label**: Starter $199/mo brand+domain+10 clients, Pro $499/mo remove Powered by + priority, Enterprise $999/mo on-premise + source
- **Profit Example**: 50 clients × $299 white-label = $14,950 MRR - $249 cost (white-label $199 + LLM $50) = $14,701 profit (98% margin)

## Quickstart

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend && npm install && npm run dev

# Docker Prod
cp .env.prod.example .env.prod && docker-compose -f docker-compose.prod.yml up -d

# Tests
cd backend && python tests/test_agents.py # 🎉 All tests passed - 68 agents, 292 skills

# Mobile
cd mobile && npm install && npm run android # or ios, PWA already via frontend URL Add to Home Screen
```

## Links

- Frontend 22 Views: https://5173-...e2b.app
- Backend 68/292: https://8000-...e2b.app/api/docs
- Docs: docs/ - BUSINESS_PLAN, WHITELABEL, ARCHITECTURE, API, VIDEO_SCRIPT, SOC2_COMPLIANCE, PRODUCTION_CHECKLIST
- SDKs: sdk/python + sdk/typescript
- Mobile: mobile/ - 6 screens RN + PWA
- Docs Site: docs-site/ - Docusaurus config + custom.css violet + homepage
- Postman: postman/collection.json - 80+ endpoints
- Monitoring: monitoring/grafana/dashboards/ai-agency-os.json - 10 panels
- Scripts: scripts/install.sh - one-command on-premise installer
- K8s: k8s/deployment.yaml
- CI/CD: .github/workflows/ci.yml
    """,
    "version": "13.0.0 - Enterprise Final - 68 Agents, 292 Skills, 20 Routers, 22 Views Web + 6 Mobile, K8s, CI/CD, Tests, Landing, Analytics, Business Plan, Marketplace, Realtime, Audit, Teams, Zapier, HubSpot, SDKs, PWA, Prod Compose, Docs Site, Mobile Full, SOC2, Postman, Grafana, Production Checklist",
    "contact": {
        "name": "AI Agency OS",
        "url": "https://ai-agency.os",
        "email": "support@ai-agency.os"
    },
    "license": {
        "name": "Private - For Your Agency",
        "url": "https://ai-agency.os/license"
    }
}

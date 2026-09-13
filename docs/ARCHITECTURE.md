# Architecture - AI Agency OS v9

## Overview

AI Agency OS is a full-stack AI agency automation system inspired by ECC (68 agents, 292 skills) and Open WebUI (user-friendly chat, Tools/Functions, Pipelines).

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React + Vite)                  │
│  21 Views: Landing, Dashboard, Analytics, Marketplace, Realtime, │
│  Audit, Teams, Chat, Agents (68), Skills (292), Pipelines,      │
│  Builder, Flow Builder, Tools, Memory, Knowledge RAG, Agency,    │
│  Client Portal, Security, Auth, Billing, Eval, Integrations      │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 │ REST + WebSocket
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI) - 18 Routers              │
│                                                                 │
│  Core:                                                          │
│  - Agents: 68 specialized (ECC parity)                          │
│  - Skills: 292 reusable (ECC parity)                            │
│  - Memory: episodic + semantic + procedural + instincts         │
│  - Tools: 9 OpenAI-compatible functions                         │
│  - Functions: Pipe (new model), Filter (middleware), Action     │
│  - Pipelines: OpenAI-compatible, 4 built-in + builder           │
│                                                                 │
│  Agency OS (Track A):                                           │
│  - Chat, Agency (projects, clients, tasks), Knowledge RAG       │
│  - Client Portal, Verification (real), Pipeline Builder/Flow    │
│  - Storage (S3/local), Email (SendGrid/SMTP), Realtime WS       │
│                                                                 │
│  SaaS (Track B):                                                │
│  - Auth (JWT, RBAC), Billing (Stripe), Eval (accuracy),         │
│  - Analytics (cost, revenue), Marketplace, Audit (SOC2/GDPR),   │
│  - Teams (RBAC + white-label), Landing Page                     │
│                                                                 │
│  Production (Track C):                                          │
│  - Security (AgentShield, prompt injection), Integrations       │
│  - Realtime, Audit, K8s, CI/CD, PWA, SDKs                       │
│                                                                 │
│  Cross-harness (Track D):                                       │
│  - 68 agents with dynamic loader, 292 skills v1-v7,             │
│  - Pipeline Builder + Flow Builder (React Flow)                 │
└─────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │  PostgreSQL  │ │    Redis     │ │   ChromaDB   │
        │  (projects,  │ │  (cache,     │ │  (vectors,   │
        │   tasks,     │ │   sessions,  │ │   RAG)       │
        │   users)     │ │   queue)     │ │              │
        └──────────────┘ └──────────────┘ └──────────────┘
                │                │                │
                └────────────────┼────────────────┘
                                 ▼
        ┌─────────────────────────────────────────┐
        │           External Services             │
        │  - LLM: Ollama (local) + OpenAI API     │
        │  - Storage: S3 / MinIO / Local          │
        │  - Email: SendGrid / SMTP               │
        │  - Billing: Stripe                      │
        │  - Monitoring: Prometheus + Grafana     │
        └─────────────────────────────────────────┘
```

## Data Flow

### 1. Client Onboarding
```
User creates project → Agency Router → Email Service (onboarding) → Client Portal
                     → Task creation → Agent assignment → Pipeline execution
```

### 2. Agent Execution (Real-time)
```
User message → Chat Router → Agent selection (68) → Skill injection (292)
             → Tool calling (9) → Memory retrieval → LLM (Ollama/OpenAI)
             → WebSocket broadcast (token by token) → Frontend live update
             → Verification loop → Task update → Email to client
```

### 3. RAG
```
Document upload → Storage (S3) → Chunking → Embedding (ChromaDB)
                → Query → HyDE + reranking → Context → Agent
```

### 4. Billing
```
Agent run → Cost tracking (tokens * price) → Billing Router
          → Usage aggregation → Stripe invoice → Email
```

## Tech Stack

- **Backend**: FastAPI, Python 3.11, Pydantic, JWT, Bcrypt, SQLAlchemy (optional), ChromaDB, Boto3, SendGrid
- **Frontend**: React 18, Vite 5, TailwindCSS, Recharts, React Flow, Lucide Icons, Axios
- **Infra**: Docker, K8s (3 backend replicas, 2 frontend, PVC 10Gi), CI/CD (GitHub Actions), PWA (manifest + SW)
- **LLM**: Ollama (local) + OpenAI compatible API
- **Storage**: S3/MinIO/Local, Postgres, Redis, ChromaDB
- **Monitoring**: Prometheus, Grafana, Audit logs (SOC2/GDPR)

## Security

- **AgentShield**: Prompt injection detection, secret scanning, tool validation
- **Auth**: JWT, RBAC (owner/admin/member/client/viewer), bcrypt 4.0.1
- **Audit**: All actions logged with IP, user, timestamp for SOC2/GDPR
- **Verification**: Real test execution, not mock
- **Secrets**: K8s secrets, .env, not in Git

## Scalability

- **Horizontal**: K8s 3 backend replicas, stateless, Redis for sessions
- **Vertical**: Agent execution queue, pipeline parallel steps
- **Cost**: Ollama for simple tasks (88% margin), OpenAI for complex, cost tracking per client

## White-label

- Brand name, logo, primary color, domain via API + env vars
- PWA manifest dynamic, email templates branded, Stripe own account
- Pricing: $199/$499/$999 for Starter/Pro/Enterprise white-label

## Marketplace

- Skills, Pipelines, Agents with rating, downloads, price, author
- 30% commission, install via API, search, featured
- Inspiration: Open WebUI community + ECC marketplace

## SDKs

- Python: `AIAgencyClient` with all APIs
- TypeScript: same + WebSocket helper
- Future: Go, Rust, etc.

## PWA / Mobile

- Manifest + Service Worker + Push notifications
- Installable on mobile, offline cache, task update push
- Future: React Native app with same APIs

## Roadmap

- Q1 2024: MVP done (68 agents, 292 skills, 21 views)
- Q2 2024: Polish, docs, SDKs, PWA, white-label, marketplace
- Q3 2024: Scale, 1000 users, mobile app, Zapier/HubSpot deep
- Q4 2024: Enterprise, on-premise, SOC2 cert, $150K MRR

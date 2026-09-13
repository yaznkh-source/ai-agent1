# AI Agency OS - Architecture Deep Dive

## Overview
AI Agency OS يجمع أفضل ما في ECC و Open WebUI:

### ECC Inspiration (Everything Claude Code)
- **Original**: https://github.com/affaan-m/ECC - 257k stars, 38.5k forks
- **Core Idea**: Agent harness performance optimization system
- **Key Concepts Adopted**:
  1. **Agents**: 68 specialized agents with isolated context
  2. **Skills**: 292 reusable workflows loaded on-demand (context optimization)
  3. **Hooks**: SessionStart, SessionEnd, PreToolUse, PostToolUse - run outside model context
  4. **Memory**: Session summaries + long-term memory with char cap
  5. **Instincts**: Continuous learning v2 - patterns extracted with confidence scoring, clustered into skills via /evolve
  6. **Verification Loop**: Build, test, lint, typecheck, security - deterministic gate
  7. **AgentShield**: Security scanning for prompts, hooks, MCP, secrets
  8. **Workflow**: plan -> test -> implement -> review -> verify -> remember -> improve

### Open WebUI Inspiration
- **Original**: https://github.com/open-webui/open-webui - 152k stars, 22.2k forks
- **Core Idea**: User-friendly AI Interface (Supports Ollama, OpenAI API, ...)
- **Key Concepts Adopted**:
  1. **Multi-Provider LLM**: OpenAI, Anthropic, Ollama, OpenAI-compatible
  2. **Tools**: Extend LLM abilities (weather, search, real-time data) - called by model during inference
  3. **Functions**:
     - **Pipe**: Adds custom model/agent (appears as selectable model) - model providers, agents, non-LLM interfaces, proxies
     - **Filter**: Intercepts data flowing to/from models (inlet, outlet, stream) - translation, moderation, logging, rate limiting
     - **Action**: Adds interactive buttons to messages - export, summarize, trigger workflows
     - **Event**: Reacts to system-wide activity (170+ events) - auth.signup, chat.deleted, etc
  4. **Pipelines**: OpenAI API compatible framework for offloading heavy processing - standalone pipelines instance acts as intermediary
  5. **Knowledge Collections / RAG**: Internal knowledge search
  6. **Workspace**: Prompts, models, knowledge management
  7. **Chat Interface**: User-friendly chat with model selector, history, etc

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │   Chat   │ │  Agents  │ │  Skills  │ │Pipelines │ │ Agency │ │
│  │  (Open   │ │  (ECC)   │ │  (ECC)   │ │(OpenWebUI│ │(New)   │ │
│  │  WebUI)  │ │          │ │          │ │)         │ │        │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └───┬────┘ │
│       │            │            │            │           │      │
└───────┼────────────┼────────────┼────────────┼───────────┼──────┘
        │            │            │            │           │
┌───────▼────────────▼────────────▼────────────▼───────────▼──────┐
│                     Backend (FastAPI)                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    Core Layer                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐ │  │
│  │  │  Config  │ │   LLM    │ │       AgentShield        │ │  │
│  │  │(OpenWebUI│ │(Multi-   │ │       (ECC)              │ │  │
│  │  │+ ECC)    │ │ Provider)│ │                          │ │  │
│  │  └──────────┘ └──────────┘ └──────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   Agent Layer (ECC)                     │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐ │  │
│  │  │Definitions│ │Orchestr. │ │  Workflows               │ │  │
│  │  │20 agents │ │plan→test │ │  full_feature, quick,    │ │  │
│  │  │→68 ext.  │ │→impl→rev │ │  research_first, security│ │  │
│  │  └──────────┘ └──────────┘ └──────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                   Skills Layer (ECC)                    │  │
│  │  15 skills → 292 extensible, MD-based, on-demand load  │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              Memory & Learning Layer (ECC)              │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐ │  │
│  │  │  Memory  │ │Instincts │ │  Hooks                   │ │  │
│  │  │ Session  │ │Continuous│ │  SessionStart/End,       │ │  │
│  │  │ + Long   │ │ Learning │ │  Pre/PostToolUse,        │ │  │
│  │  │          │ │ v2       │ │  Pre/PostMessage         │ │  │
│  │  └──────────┘ └──────────┘ └──────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              Extensibility Layer (Open WebUI)           │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐ │  │
│  │  │  Tools   │ │Functions │ │  Pipelines               │ │  │
│  │  │ 9 tools  │ │Pipe/Filter│ │  4 pipelines,            │ │  │
│  │  │ OpenAI   │ │Action/Ev.│ │  OpenAI API compat       │ │  │
│  │  │ func call│ │          │ │  Heavy offload           │ │  │
│  │  └──────────┘ └──────────┘ └──────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                Agency Layer (New)                       │  │
│  │  Clients → Projects → Tasks + Dashboard + Verification  │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                 API Layer (8 Routers)                   │  │
│  │  /chats, /agents, /skills, /memory, /tools, /functions, │  │
│  │  /pipelines, /agency                                    │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      Persistence                                │
│  SQLite (chats, messages, memory, clients, projects, tasks)    │
│  ChromaDB (optional vector search)                              │
│  File System (skills/*.md)                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      LLM Providers                              │
│  OpenAI API, Anthropic, Ollama (local), Custom OpenAI-compat   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### 1. Chat with Agent (ECC + Open WebUI)
```
User Message → PreMessage Hook (filter) → Agent Selection → Skill Injection → Memory Retrieval → LLM Call (with Tools) → Tool Execution (with PreToolUse security) → PostToolUse Hook (instinct) → PostMessage Hook → SessionEnd Hook (summary) → Response
```

### 2. Multi-Agent Workflow (ECC: plan→test→implement→review)
```
Task → Planner Agent (creates plan artifact) → Architect Agent (design) → Backend Dev (TDD: RED→GREEN→REFACTOR) → Frontend Dev → Reviewer Agent (FRESH CONTEXT - ECC key insight) → QA Engineer → Verification Loop (build, test, lint, typecheck, security) → Memory Save
```

### 3. Pipeline Execution (Open WebUI Pipelines)
```
Context {task, client_name} → Step 1: Agent (researcher) → Step 2: Agent (planner) → Step 3: Tool (proposal_generator) → Step 4: LLM (checklist) → Final Result + History
```

### 4. Memory & Instincts (ECC Continuous Learning)
```
Session → SessionStart Hook loads memories → Interaction → Tool Use → PostToolUse records instinct pattern → SessionEnd Hook distills summary → Save memory → If 3+ related instincts with high confidence → Evolve to Skill via /evolve
```

## Security (AgentShield)

Inspired by ECC's AgentShield:
- Scans: prompts, hooks, MCP config, permissions, secrets, agent files
- Patterns:
  - Secrets: OpenAI keys, Anthropic keys, GitHub tokens, AWS keys, private keys, Google API keys
  - Injection: "ignore previous instructions", "system: you are now", <script, eval(, exec(, __import__, os.system, subprocess
  - Dangerous: rm -rf, chmod 777, mkfs, fork bomb, curl|sh
- Severity: critical, high, medium, low
- Status: secure, warning, critical

## Extensibility

### Adding Agent (ECC: 68 agents)
Edit `backend/app/agents/definitions.py`:
```python
{
  "id": "my-agent",
  "name": "My Agent",
  "role": "...",
  "category": "development",
  "system_prompt": "...",
  "skills": ["tdd-workflow"],
  "tools": ["code_write"],
  "model": "gpt-4o-mini",
  "color": "#8B5CF6"
}
```

### Adding Skill (ECC: 292 skills)
Create `backend/app/skills/definitions/my-skill.md`:
```markdown
# My Skill
Content...
```
Or via API: POST /api/skills/

### Adding Tool (Open WebUI Tools)
Edit `backend/app/tools/registry.py`:
```python
{
  "id": "my_tool",
  "name": "My Tool",
  "schema": {
    "type": "function",
    "function": {
      "name": "my_tool",
      "description": "...",
      "parameters": {...}
    }
  }
}
```
And implementation in `register_builtin_implementations()`

### Adding Pipeline (Open WebUI Pipelines)
Via API: POST /api/pipelines/ or edit `backend/app/pipelines/engine.py`

### Adding Function (Open WebUI Functions)
Via API: POST /api/functions/ with type pipe/filter/action/event

## Performance Considerations

- **Context Optimization**: Skills loaded on-demand, not always (ECC)
- **Memory Cap**: 10k chars max to avoid blowing context window
- **Fresh Context Reviewer**: Isolated context for review to avoid blind spots
- **Hooks Outside Model**: Deterministic checks outside prompt (ECC)
- **Pipelines Offload**: Heavy processing offloaded from main instance (Open WebUI)

## Deployment

- **Dev**: `npm run dev` + `uvicorn --reload`
- **Docker**: `docker-compose up`
- **Preview Support**: host 0.0.0.0, CORS *, allowedHosts true, X-Frame-Options ALLOWALL

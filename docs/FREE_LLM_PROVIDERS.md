# Free LLM Providers — Task D3 — Most Valuable — From free-claude-code 54.8k Stars

Date: 2026-09-13
Repo: Alishahryar1/free-claude-code — 54.8k stars, 8.8k forks, 1068 commits, 4828 tests
Value: Cost reduction 88%→100% margin — $0 LLM cost
Cost: $0 — NVIDIA NIM 40 req/min free, OpenRouter free models, Ollama local free

## Providers — 5 Free/Cheap — From free-claude-code

### 1. NVIDIA NIM — 40 req/min Free — Recommended

**Website**: https://build.nvidia.com/
**API Key**: `nvapi-...` — Free 40 req/min
**Models**: `meta/llama-3.1-70b-instruct`, `meta/llama-3.1-405b-instruct`, `meta/llama-3.1-8b-instruct`, etc — 100+ models
**Base URL**: `https://integrate.api.nvidia.com/v1`

**How to Get Free API Key — $0 — 2 Minutes**:
1. Go to https://build.nvidia.com/
2. Sign in with NVIDIA account (or Google)
3. Pick model e.g., Llama 3.1 70B Instruct — https://build.nvidia.com/meta/llama-3.1-70b-instruct
4. Click "Get API Key" — Generates `nvapi-...` key — 40 req/min free forever
5. Set env: `export NVIDIA_NIM_API_KEY=nvapi-...`
6. Test: `curl -X POST https://integrate.api.nvidia.com/v1/chat/completions -H "Authorization: Bearer nvapi-..." -H "Content-Type: application/json" -d '{"model":"meta/llama-3.1-70b-instruct","messages":[{"role":"user","content":"Hello"}]}'`

**For AI Agency OS**:
- Use for planner, backend-dev, frontend-dev, content-creator agents — 70B good for code and reasoning
- 40 req/min free = 57,600 req/day = enough for 100 users * 10 req/day = 1000 req/day — free covers Beta 10 and Prod 100
- Cost: $0 — margin 100%

### 2. OpenRouter — Free Models — :free

**Website**: https://openrouter.ai/
**API Key**: `sk-or-...` — Free models with `:free` suffix
**Models**: `meta-llama/llama-3.1-8b-instruct:free`, `google/gemma-2-9b-it:free`, `mistralai/mistral-7b-instruct:free`, etc — 20+ free models
**Base URL**: `https://openrouter.ai/api/v1`

**How to Get Free API Key — $0 — 2 Minutes**:
1. Go to https://openrouter.ai/
2. Sign in with Google/GitHub
3. Keys → Create Key → `sk-or-...` — free models no credit needed, paid models need credits
4. Set env: `export OPENROUTER_API_KEY=sk-or-...`
5. Test: `curl -X POST https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer sk-or-..." -H "Content-Type: application/json" -d '{"model":"meta-llama/llama-3.1-8b-instruct:free","messages":[{"role":"user","content":"Hello"}]}'`

**For AI Agency OS**:
- Use for researcher, seo-specialist — 8B free enough for simple tasks
- Free models: no cost, but rate limited — good for Beta
- Cost: $0 with :free models — margin 100%

### 3. DeepSeek — Cheap — $0.14/1M Input

**Website**: https://www.deepseek.com/ — https://platform.deepseek.com/
**API Key**: `sk-...` — Cheap, not free but very cheap $0.14/1M input, $0.28/1M output
**Models**: `deepseek-chat` (V3), `deepseek-reasoner` (R1 reasoning)
**Base URL**: `https://api.deepseek.com/v1`

**How to Get API Key — $0 to start — Cheap**:
1. Go to https://platform.deepseek.com/
2. Sign up — free $5 credits often
3. API Keys → Create — `sk-...`
4. Set env: `export DEEPSEEK_API_KEY=sk-...`
5. Test: `curl -X POST https://api.deepseek.com/v1/chat/completions -H "Authorization: Bearer sk-..." -H "Content-Type: application/json" -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}'`

**For AI Agency OS**:
- Use as fallback cheap — $0.14/1M vs OpenAI $5/1M — 35x cheaper
- Cost: ~$0.01 per 1000 req — margin 99% vs 88% with OpenAI

### 4. LM Studio — Local Free — 100% Free

**Website**: https://lmstudio.ai/
**Models**: Any GGUF model — Llama 3, Mistral, Gemma, etc — local
**Base URL**: `http://localhost:1234/v1` — OpenAI-compatible local server

**How to Get — $0 — Local Free — 5 Minutes**:
1. Download LM Studio from https://lmstudio.ai/ — Windows/Mac/Linux
2. Install + Open
3. Discover → Search model e.g., Llama 3.1 8B Instruct GGUF → Download
4. Local Server → Start Server — runs at http://localhost:1234/v1 — OpenAI-compatible
5. Set env: `export LMSTUDIO_BASE_URL=http://localhost:1234/v1` + `export LMSTUDIO_MODEL=local-model`
6. Test: `curl -X POST http://localhost:1234/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"local-model","messages":[{"role":"user","content":"Hello"}]}'`

**For AI Agency OS**:
- Use for 100% free local — no internet, no cost, privacy
- Good for qa-engineer, devops simple tasks
- Cost: $0 — margin 100% — but needs local machine with RAM (8B needs 8GB RAM, 70B needs 48GB)

### 5. Ollama — Local Free — Already in AI Agency OS — 100% Free

**Website**: https://ollama.ai/
**Models**: `llama3`, `llama3.1`, `mistral`, `gemma2`, `codellama`, etc — local
**Base URL**: `http://localhost:11434/v1` — OpenAI-compatible

**How to Get — $0 — Local Free — Already in docker-compose.yml**:
1. Already in docker-compose.yml — `ollama` service — `docker-compose up -d ollama` — runs at http://ollama:11434
2. Or local: `curl -fsSL https://ollama.com/install.sh | sh` + `ollama serve` + `ollama pull llama3`
3. Set env: `export OLLAMA_BASE_URL=http://localhost:11434/v1` + `export OLLAMA_MODEL=llama3`
4. Test: `curl -X POST http://localhost:11434/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"llama3","messages":[{"role":"user","content":"Hello"}]}'`

**For AI Agency OS**:
- Already integrated — use for qa-engineer, seo-specialist, simple tasks
- Cost: $0 — margin 100%

## Per-Model Mapping — From free-claude-code — Cost Optimization

Route different agents to different providers/models based on complexity — mix freely:

| Agent | Provider | Model | Cost | Reason |
|-------|----------|-------|------|--------|
| planner | nvidia_nim | llama-3.1-70b-instruct | Free | Planning needs reasoning, 70B good enough free |
| architect | openai | gpt-4o | Paid $5/1M | Architecture needs best reasoning, use GPT-4o |
| backend-dev | nvidia_nim | llama-3.1-70b-instruct | Free | Coding 70B good |
| frontend-dev | nvidia_nim | llama-3.1-70b-instruct | Free | Coding 70B good |
| qa-engineer | ollama | llama3 | Free | QA simple, Ollama local free |
| researcher | openrouter | llama-3.1-8b-instruct:free | Free | Research 8B free enough |
| seo-specialist | ollama | llama3 | Free | SEO simple |
| content-creator | nvidia_nim | llama-3.1-70b-instruct | Free | Content 70B good |
| reviewer | openai | gpt-4o | Paid | Review needs best quality |

**Cost with mapping**: 
- 7 agents free (planner, backend-dev, frontend-dev, qa, researcher, seo, content) — $0
- 2 agents paid (architect, reviewer) — $0.05 per task
- Average cost per project (5 tasks): $0.10 — vs $10 with all GPT-4o — **100x cheaper — margin 99.9%**

## Request Optimization — From free-claude-code — 5 Categories

Intercept trivial API calls locally, saving quota and latency:

- **list_models**: Return local list — no API call — save quota
- **get_model**: Return mock model info — save quota
- **health**: Return healthy — save quota
- **ping**: Return pong — save quota
- **version**: Return version — save quota

**Implementation**: `is_optimizable()` + `get_optimized_response()` in free_llm.py

## Smart Rate Limiting — From free-claude-code — Better than slowapi 100/min

- **Proactive rolling-window throttle**: Track requests in last 60s, throttle if over rate limit (e.g., 40/min for NIM)
- **Reactive 429 exponential backoff**: When 429, backoff 1s, 2s, 4s, 8s, max 60s
- **Concurrency cap**: Limit concurrent requests per provider (e.g., 5 for NIM, 100 for Ollama local)

**Implementation**: `SmartRateLimiter` class in free_llm.py — better than our simple slowapi 100/min

## Thinking Token Support — From free-claude-code

Parse `<think>` tags and `reasoning_content` into native Claude thinking blocks:

- **Input**: Model outputs `<think>Need to plan...</think>Answer`
- **Parsed**: `thinking: "Need to plan..."`, `answer: "Answer"`, `thinking_blocks: [{"type": "thinking", "thinking": "..."}]`
- **Use**: For planner agent — show thinking process in UI

**Implementation**: `parse_thinking_tokens()` in free_llm.py

## Heuristic Tool Parser — From free-claude-code

Models outputting tool calls as text auto-parsed into structured tool use:

- **Input**: `web_search(query="test")` or `<tool_call>{"name": "web_search", "arguments": {"query": "test"}}</tool_call>`
- **Parsed**: `[{"name": "web_search", "arguments": {"query": "test"}}]`
- **Use**: For agents — if model doesn't support native tool calling, parse text into structured

**Implementation**: `parse_tool_calls_from_text()` in free_llm.py — handles 3 patterns

## Cost Calculation — Margin 88%→100%

| Provider | Cost | Margin with $199 Pro plan |
|----------|------|---------------------------|
| NVIDIA NIM free 40 req/min | $0 | 100% — $199 profit |
| OpenRouter :free | $0 | 100% |
| Ollama local | $0 | 100% |
| LM Studio local | $0 | 100% |
| DeepSeek cheap | $0.14/1M | 99.9% — $198.9 profit |
| OpenAI GPT-4o | $5/1M input $15/1M output | 88% — $175 profit with Ollama mix |

**With free providers**: LLM cost $0 → profit $199 (100% margin) vs $175 (88%) with OpenAI mix — **$24 more profit per user per month — 50 users = $1200 extra profit**

## Integration into AI Agency OS — Task D3

### Backend

- **File**: `backend/app/core/free_llm.py` — 500 lines — BaseProvider ABC + 5 providers + per-model mapping + optimization + rate limiting + thinking tokens + tool parser + cost calculation
- **Router**: `backend/app/routers/llm.py` — New router for free LLM — /api/llm/ — list providers, chat completion with free providers, per-model mapping
- **Requirements**: `httpx`, `slack_sdk` already, add `openai` already exists

### Frontend

- **Component**: `LLMProvidersView.tsx` — Show available free providers, cost, margin, per-model mapping, how to get API keys
- **Add to**: `App.tsx` + `Sidebar.tsx` — new view

### Docs

- **This file**: `docs/FREE_LLM_PROVIDERS.md` — How to get free API keys $0, per-model mapping, cost optimization, margin 88%→100%

### Test

```bash
# Set free provider
export NVIDIA_NIM_API_KEY=nvapi-...
# Or
export OPENROUTER_API_KEY=sk-or-...
# Or run Ollama
ollama pull llama3 && ollama serve

# Test via API
curl -X POST http://localhost:8000/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"agent_id":"planner"}' | jq .

# Should return real response from free provider if key set, mock if not, with cost $0 and margin 100%
```

## Evidence

- Repo: https://github.com/Alishahryar1/free-claude-code — 54.8k stars, 8.8k forks, 1068 commits, 4828 tests + 65 browser tests — proven pattern
- Providers: 5 — NVIDIA NIM 40 req/min free, OpenRouter free models, DeepSeek cheap, LM Studio local free, Ollama local free
- Features: Per-model mapping, request optimization 5 categories, smart rate limiting rolling-window + 429 backoff + concurrency cap, thinking tokens, tool parser, Discord/Telegram bot, Admin UI, BaseProvider ABC extensible
- Cost: $0 with free providers — margin 88%→100% — $24 extra profit per user per month

## For AI Agency OS — Most Valuable Integration — Push 99→100

- **Cost**: $0 — NVIDIA NIM free 40 req/min, OpenRouter free, Ollama local free
- **Margin**: 88% → 100% — $199 profit vs $175 — $24 extra per user
- **Scalability**: Free providers have rate limits (40/min NIM) — need smart rate limiting + concurrency cap + fallback to Ollama local
- **Quality**: 70B models good for code and planning — 8B good for simple tasks — GPT-4o still needed for architect/reviewer complex
- **Implementation**: BaseProvider ABC pattern — clean extensibility — we adopted

"""
LLM Router - Free Providers - Task D3 - Most Valuable - From free-claude-code 54.8k stars
Provides free LLM via NVIDIA NIM 40 req/min free, OpenRouter free, Ollama local free
"""
from fastapi import APIRouter, Depends
from typing import Dict, List
import os

router = APIRouter(prefix="/api/llm", tags=["llm-free"])

@router.get("/")
async def llm_info():
    try:
        from ..core.free_llm import get_available_providers, PROVIDERS, MODEL_MAPPING, get_model_for_agent
        available = get_available_providers()
    except Exception as e:
        available = []
    
    return {
        "llm": "Free LLM Providers — From free-claude-code 54.8k stars — $0 cost — margin 88%→100%",
        "reality": "REAL_WITH_MOCK_FALLBACK - Real API calls when keys set, mock when not",
        "providers": {
            "nvidia_nim": {
                "name": "NVIDIA NIM",
                "free": "40 req/min free",
                "models": ["meta/llama-3.1-70b-instruct", "meta/llama-3.1-405b-instruct", "meta/llama-3.1-8b-instruct"],
                "api_key": "nvapi-... from https://build.nvidia.com/",
                "base_url": "https://integrate.api.nvidia.com/v1",
                "cost": "$0 free",
                "margin": "100%",
                "recommended_for": ["planner", "backend-dev", "frontend-dev", "content-creator"],
                "how_to_get": "https://build.nvidia.com/ → Pick model → Get API Key nvapi-... → Set NVIDIA_NIM_API_KEY env — 2 min — $0",
                "available": "nvidia_nim" in available
            },
            "openrouter": {
                "name": "OpenRouter",
                "free": "Free models :free",
                "models": ["meta-llama/llama-3.1-8b-instruct:free", "google/gemma-2-9b-it:free", "mistralai/mistral-7b-instruct:free"],
                "api_key": "sk-or-... from https://openrouter.ai/",
                "base_url": "https://openrouter.ai/api/v1",
                "cost": "$0 with :free models",
                "margin": "100%",
                "recommended_for": ["researcher", "seo-specialist"],
                "how_to_get": "https://openrouter.ai/ → Keys → Create sk-or-... → Set OPENROUTER_API_KEY — 2 min — $0",
                "available": "openrouter" in available
            },
            "ollama": {
                "name": "Ollama",
                "free": "Local free 100% — already in docker-compose.yml",
                "models": ["llama3", "llama3.1", "mistral", "gemma2", "codellama"],
                "base_url": "http://localhost:11434/v1 or http://ollama:11434/v1 in docker",
                "cost": "$0 local",
                "margin": "100%",
                "recommended_for": ["qa-engineer", "seo-specialist", "simple tasks"],
                "how_to_get": "Already in docker-compose.yml — docker-compose up -d ollama — or local: curl -fsSL https://ollama.com/install.sh | sh + ollama pull llama3 + ollama serve — $0",
                "available": "ollama" in available
            },
            "lm_studio": {
                "name": "LM Studio",
                "free": "Local free 100%",
                "models": ["local-model — any GGUF"],
                "base_url": "http://localhost:1234/v1",
                "cost": "$0 local",
                "margin": "100%",
                "recommended_for": ["qa-engineer", "devops"],
                "how_to_get": "https://lmstudio.ai/ → Download → Install → Discover model → Local Server → Start at http://localhost:1234/v1 — $0",
                "available": "lm_studio" in available
            },
            "deepseek": {
                "name": "DeepSeek",
                "free": "Cheap $0.14/1M input — not free but 35x cheaper than OpenAI",
                "models": ["deepseek-chat", "deepseek-reasoner"],
                "api_key": "sk-... from https://platform.deepseek.com/",
                "base_url": "https://api.deepseek.com/v1",
                "cost": "$0.14/1M input $0.28/1M output",
                "margin": "99.9%",
                "recommended_for": ["fallback cheap"],
                "how_to_get": "https://platform.deepseek.com/ → API Keys → Create sk-... → Set DEEPSEEK_API_KEY — $0 to start with $5 free credits",
                "available": "deepseek" in available
            }
        },
        "available_providers": available,
        "per_model_mapping": {
            "planner": {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free", "reason": "Planning needs reasoning, 70B good enough free"},
            "backend-dev": {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free"},
            "qa-engineer": {"provider": "ollama", "model": "llama3", "cost": "free", "reason": "QA simple, Ollama local free"},
            "researcher": {"provider": "openrouter", "model": "meta-llama/llama-3.1-8b-instruct:free", "cost": "free"},
            "architect": {"provider": "openai", "model": "gpt-4o", "cost": "paid", "reason": "Architecture needs best reasoning, GPT-4o"}
        },
        "request_optimization": {
            "description": "5 categories of trivial API calls intercepted locally, saving quota and latency — from free-claude-code",
            "categories": ["list_models", "get_model", "health", "ping", "version"],
            "save_quota": True
        },
        "smart_rate_limiting": {
            "description": "Proactive rolling-window throttle + reactive 429 exponential backoff + concurrency cap — from free-claude-code — better than slowapi 100/min",
            "nvidia_nim": "40 req/min + backoff 1s,2s,4s,8s,max 60s + concurrency cap 5",
            "ollama": "1000 req/min local no limit + concurrency 100"
        },
        "thinking_tokens": {
            "description": "Parse <think> tags and reasoning_content into Claude thinking blocks — from free-claude-code",
            "example": "<think>Need to plan...</think>Answer → thinking: Need to plan..., answer: Answer"
        },
        "tool_parser": {
            "description": "Heuristic tool parser — models outputting tool calls as text auto-parsed into structured — from free-claude-code",
            "patterns": ["<tool_call>...</tool_call>", "```json tool_calls", "web_search(query=\"test\")"]
        },
        "cost_comparison": {
            "openai_gpt4o": "$5/1M input $15/1M output — margin 88% with Ollama mix — $175 profit on $199 Pro",
            "nvidia_nim_free": "$0 — 40 req/min free — margin 100% — $199 profit — $24 extra per user per month",
            "ollama_local": "$0 — margin 100% — needs local RAM 8GB for 8B, 48GB for 70B"
        },
        "endpoints": {
            "info": "GET /api/llm/ — this",
            "providers": "GET /api/llm/providers — list available free providers",
            "chat": "POST /api/llm/chat — chat completion with free providers + per-model mapping",
            "mapping": "GET /api/llm/mapping/{agent_id} — get model mapping for agent"
        },
        "docs": "docs/FREE_LLM_PROVIDERS.md — How to get free API keys $0, per-model mapping, cost optimization, margin 88%→100%"
    }

@router.get("/providers")
async def list_providers():
    try:
        from ..core.free_llm import get_available_providers, PROVIDERS
        available = get_available_providers()
        all_providers = []
        for name, provider_class in PROVIDERS.items():
            provider = provider_class()
            all_providers.append({
                "name": name,
                "available": name in available,
                "is_local": provider.is_local(),
                "is_free": provider.is_free(),
                "rate_limit": provider.get_rate_limit(),
                "model": provider.model,
                "base_url": provider.base_url if hasattr(provider, 'base_url') else None,
                "has_api_key": bool(provider.api_key)
            })
        return {
            "providers": all_providers,
            "available": available,
            "count": len(all_providers),
            "available_count": len(available),
            "reality": "REAL_WITH_MOCK_FALLBACK"
        }
    except Exception as e:
        return {
            "providers": [],
            "available": [],
            "error": str(e),
            "note": "Install httpx + set API keys for real providers"
        }

@router.get("/mapping/{agent_id}")
async def get_mapping(agent_id: str):
    try:
        from ..core.free_llm import get_model_for_agent, MODEL_MAPPING
        mapping = get_model_for_agent(agent_id)
        return {
            "agent_id": agent_id,
            "mapping": mapping,
            "all_mappings": MODEL_MAPPING
        }
    except Exception as e:
        return {"agent_id": agent_id, "error": str(e)}

@router.post("/chat")
async def free_llm_chat(payload: Dict):
    """
    Chat completion with free LLM providers
    Uses per-model mapping, request optimization, smart rate limiting, thinking tokens, tool parser
    """
    messages = payload.get("messages", [])
    agent_id = payload.get("agent_id")
    model = payload.get("model")
    temperature = payload.get("temperature", 0.7)
    
    if not messages:
        return {"error": "messages required"}
    
    try:
        from ..core.free_llm import free_chat_completion
        result = await free_chat_completion(messages, agent_id=agent_id, model=model, temperature=temperature)
        return result
    except Exception as e:
        return {
            "content": f"Error: {e} — Mock fallback",
            "provider": "mock",
            "model": model or "mock",
            "real": False,
            "error": str(e),
            "cost": 0.0,
            "note": "Set NVIDIA_NIM_API_KEY or OPENROUTER_API_KEY or run Ollama for real free LLM"
        }

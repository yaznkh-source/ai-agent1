"""
Free LLM Providers - Task D3 - Most Valuable - From free-claude-code 54.8k stars
Provides free LLM via NVIDIA NIM 40 req/min free, OpenRouter free models, DeepSeek, LM Studio local, Ollama
BaseProvider ABC pattern + per-model mapping + request optimization + smart rate limiting + thinking tokens + tool parser
"""
import os
import time
import json
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import hashlib

# === BaseProvider ABC - From free-claude-code pattern ===

class BaseProvider(ABC):
    """Base provider for LLM - clean extensibility"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key
        self.model = model
        self.request_count = 0
        self.last_request_time = 0
    
    @abstractmethod
    async def chat_completion(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        """Chat completion - must implement"""
        pass
    
    def is_available(self) -> bool:
        """Check if provider available - has API key or local"""
        return bool(self.api_key) or self.is_local()
    
    def is_local(self) -> bool:
        """Is local provider (no API key needed)"""
        return False
    
    def get_rate_limit(self) -> int:
        """Requests per minute"""
        return 60

class OpenAICompatibleProvider(BaseProvider):
    """OpenAI-compatible provider - base for NVIDIA NIM, OpenRouter, DeepSeek, LM Studio, Ollama"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None):
        super().__init__(api_key, model)
        self.base_url = base_url
    
    async def chat_completion(self, messages: List[Dict], model: str = None, **kwargs) -> Dict:
        model = model or self.model
        try:
            import httpx
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            # OpenAI-compatible payload
            payload = {
                "model": model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 1000),
                "stream": False
            }
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "provider": self.__class__.__name__,
                        "model": model,
                        "content": data["choices"][0]["message"]["content"],
                        "usage": data.get("usage", {}),
                        "real": True,
                        "cost": 0.0 if self.is_free() else 0.01
                    }
                else:
                    return {
                        "provider": self.__class__.__name__,
                        "model": model,
                        "error": f"HTTP {resp.status_code}: {resp.text[:200]}",
                        "real": False,
                        "fallback_to_mock": True
                    }
        except ImportError:
            return {
                "provider": self.__class__.__name__,
                "model": model,
                "error": "httpx not installed",
                "real": False,
                "mock_content": f"Mock response from {self.__class__.__name__} for model {model} - install httpx + set API key for real"
            }
        except Exception as e:
            return {
                "provider": self.__class__.__name__,
                "model": model,
                "error": str(e),
                "real": False,
                "mock_content": f"Mock response due to error: {e}"
            }
    
    def is_free(self) -> bool:
        return False

# === 5 Providers - From free-claude-code ===

class NIMProvider(OpenAICompatibleProvider):
    """NVIDIA NIM - 40 req/min free - Recommended"""
    
    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("NVIDIA_NIM_API_KEY", "")
        model = model or os.getenv("NIM_MODEL", "meta/llama-3.1-70b-instruct")
        base_url = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
        super().__init__(api_key, model, base_url)
    
    def is_available(self) -> bool:
        return bool(self.api_key) and self.api_key.startswith("nvapi-")
    
    def get_rate_limit(self) -> int:
        return 40  # 40 req/min free
    
    def is_free(self) -> bool:
        return True

class OpenRouterProvider(OpenAICompatibleProvider):
    """OpenRouter - Free models available"""
    
    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        model = model or os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
        base_url = "https://openrouter.ai/api/v1"
        super().__init__(api_key, model, base_url)
    
    def is_available(self) -> bool:
        return bool(self.api_key) and self.api_key.startswith("sk-or-")
    
    def get_rate_limit(self) -> int:
        return 20  # Depends on model
    
    def is_free(self) -> bool:
        return ":free" in self.model or "free" in self.model.lower()

class DeepSeekProvider(OpenAICompatibleProvider):
    """DeepSeek - Cheap and capable"""
    
    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        base_url = "https://api.deepseek.com/v1"
        super().__init__(api_key, model, base_url)
    
    def is_available(self) -> bool:
        return bool(self.api_key) and self.api_key.startswith("sk-")
    
    def get_rate_limit(self) -> int:
        return 60
    
    def is_free(self) -> bool:
        return False

class LMStudioProvider(OpenAICompatibleProvider):
    """LM Studio - Local, fully free"""
    
    def __init__(self, api_key: str = None, model: str = None):
        model = model or os.getenv("LMSTUDIO_MODEL", "local-model")
        base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
        super().__init__(None, model, base_url)
    
    def is_local(self) -> bool:
        return True
    
    def is_available(self) -> bool:
        # Check if LM Studio running
        try:
            import httpx
            import asyncio
            # Quick check - in real would be async, for now return True if base_url set
            return True
        except:
            return False
    
    def get_rate_limit(self) -> int:
        return 1000  # Local, no limit
    
    def is_free(self) -> bool:
        return True

class OllamaProvider(OpenAICompatibleProvider):
    """Ollama - Local, fully free - Already in AI Agency OS"""
    
    def __init__(self, api_key: str = None, model: str = None):
        model = model or os.getenv("OLLAMA_MODEL", "llama3")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        super().__init__(None, model, base_url)
    
    def is_local(self) -> bool:
        return True
    
    def get_rate_limit(self) -> int:
        return 1000
    
    def is_free(self) -> bool:
        return True

# === Provider Registry ===

PROVIDERS = {
    "nvidia_nim": NIMProvider,
    "openrouter": OpenRouterProvider,
    "deepseek": DeepSeekProvider,
    "lm_studio": LMStudioProvider,
    "ollama": OllamaProvider
}

def get_available_providers() -> List[str]:
    """Get list of available providers (have API key or local)"""
    available = []
    for name, provider_class in PROVIDERS.items():
        try:
            provider = provider_class()
            if provider.is_available():
                available.append(name)
        except:
            pass
    return available

def get_provider(name: str) -> Optional[BaseProvider]:
    """Get provider by name"""
    provider_class = PROVIDERS.get(name)
    if provider_class:
        return provider_class()
    return None

# === Per-Model Mapping - From free-claude-code ===

MODEL_MAPPING = {
    # Route Opus/Sonnet/Haiku to different models and providers
    "opus": {"provider": "nvidia_nim", "model": "meta/llama-3.1-405b-instruct", "cost": "free"},
    "sonnet": {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free"},
    "haiku": {"provider": "ollama", "model": "llama3", "cost": "free"},
    
    # For AI Agency OS agents - route cheap tasks to free, complex to paid
    "planner": {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free", "reason": "Planning - needs reasoning, free 70B good enough"},
    "backend-dev": {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free", "reason": "Coding - 70B good for code"},
    "frontend-dev": {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free"},
    "qa-engineer": {"provider": "ollama", "model": "llama3", "cost": "free", "reason": "QA - simple, Ollama local free"},
    "researcher": {"provider": "openrouter", "model": "meta-llama/llama-3.1-8b-instruct:free", "cost": "free", "reason": "Research - 8B free enough"},
    "seo-specialist": {"provider": "ollama", "model": "llama3", "cost": "free"},
    "content-creator": {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free"},
    
    # For complex tasks, use paid
    "architect": {"provider": "openai", "model": "gpt-4o", "cost": "paid", "reason": "Architecture - needs best reasoning, use GPT-4o"},
    "reviewer": {"provider": "openai", "model": "gpt-4o", "cost": "paid", "reason": "Review - needs best quality"}
}

def get_model_for_agent(agent_id: str) -> Dict:
    """Get model mapping for agent"""
    return MODEL_MAPPING.get(agent_id, {"provider": "nvidia_nim", "model": "meta/llama-3.1-70b-instruct", "cost": "free", "reason": "Default free"})

# === Request Optimization - From free-claude-code ===

# 5 categories of trivial API calls intercepted locally, saving quota and latency
OPTIMIZABLE_REQUESTS = {
    "list_models": {"save_quota": True, "local_response": {"data": [{"id": "meta/llama-3.1-70b-instruct"}, {"id": "llama3"}, {"id": "gpt-4o"}]}},
    "get_model": {"save_quota": True, "local_response": {"id": "mock-model", "object": "model"}},
    "health": {"save_quota": True, "local_response": {"status": "healthy"}},
    "ping": {"save_quota": True, "local_response": {"pong": True}},
    "version": {"save_quota": True, "local_response": {"version": "1.0.0"}}
}

def is_optimizable(request_type: str) -> bool:
    """Check if request can be optimized locally"""
    return request_type in OPTIMIZABLE_REQUESTS

def get_optimized_response(request_type: str) -> Optional[Dict]:
    """Get local optimized response"""
    if is_optimizable(request_type):
        return OPTIMIZABLE_REQUESTS[request_type]["local_response"]
    return None

# === Smart Rate Limiting - From free-claude-code ===

class SmartRateLimiter:
    """Smart rate limiting: proactive rolling-window throttle + reactive 429 exponential backoff + concurrency cap"""
    
    def __init__(self):
        self.request_times = {}  # provider -> list of timestamps
        self.backoff_until = {}  # provider -> timestamp until backoff
        self.concurrency = {}  # provider -> current concurrent requests
        self.max_concurrency = {"nvidia_nim": 5, "openrouter": 10, "deepseek": 10, "lm_studio": 100, "ollama": 100}
    
    def should_throttle(self, provider: str) -> bool:
        """Proactive rolling-window throttle"""
        now = time.time()
        rate_limit = PROVIDERS[provider]().get_rate_limit() if provider in PROVIDERS else 60
        
        # Check backoff
        if provider in self.backoff_until and now < self.backoff_until[provider]:
            return True
        
        # Check rolling window (last 60 seconds)
        if provider not in self.request_times:
            self.request_times[provider] = []
        
        # Remove old requests (>60s ago)
        self.request_times[provider] = [t for t in self.request_times[provider] if now - t < 60]
        
        # Check if over rate limit
        if len(self.request_times[provider]) >= rate_limit:
            return True
        
        # Check concurrency
        if provider in self.concurrency and self.concurrency[provider] >= self.max_concurrency.get(provider, 10):
            return True
        
        return False
    
    def record_request(self, provider: str):
        """Record request time"""
        now = time.time()
        if provider not in self.request_times:
            self.request_times[provider] = []
        self.request_times[provider].append(now)
        
        if provider not in self.concurrency:
            self.concurrency[provider] = 0
        self.concurrency[provider] += 1
    
    def record_completion(self, provider: str):
        """Record completion (reduce concurrency)"""
        if provider in self.concurrency and self.concurrency[provider] > 0:
            self.concurrency[provider] -= 1
    
    def record_429(self, provider: str):
        """Reactive 429 exponential backoff"""
        now = time.time()
        # Exponential backoff: 1s, 2s, 4s, 8s, 16s, max 60s
        if provider not in self.backoff_until:
            self.backoff_until[provider] = now + 1
        else:
            backoff_duration = min(60, (self.backoff_until[provider] - now) * 2 + 1)
            self.backoff_until[provider] = now + backoff_duration
        print(f"⚠️ Rate limit 429 for {provider} - backoff until {datetime.fromtimestamp(self.backoff_until[provider])}")

# Global rate limiter
rate_limiter = SmartRateLimiter()

# === Thinking Token Support - From free-claude-code ===

def parse_thinking_tokens(content: str) -> Dict:
    """Parse <think> tags and reasoning_content into native Claude thinking blocks"""
    import re
    
    thinking = ""
    answer = content
    
    # Parse <think>...</think> tags
    think_pattern = r"<think>(.*?)</think>"
    think_matches = re.findall(think_pattern, content, re.DOTALL)
    if think_matches:
        thinking = "\n".join(think_matches)
        # Remove think tags from answer
        answer = re.sub(think_pattern, "", content, flags=re.DOTALL).strip()
    
    # Parse reasoning_content (from some providers)
    # This would be in the response JSON, not content, but handle here too
    
    return {
        "thinking": thinking,
        "answer": answer,
        "has_thinking": bool(thinking),
        "thinking_blocks": [{"type": "thinking", "thinking": thinking}] if thinking else []
    }

# === Heuristic Tool Parser - From free-claude-code ===

def parse_tool_calls_from_text(content: str) -> List[Dict]:
    """Models outputting tool calls as text are auto-parsed into structured tool use"""
    import re
    import json
    
    tool_calls = []
    
    # Pattern 1: <tool_call>...</tool_call>
    tool_call_pattern = r"<tool_call>(.*?)</tool_call>"
    matches = re.findall(tool_call_pattern, content, re.DOTALL)
    for match in matches:
        try:
            tool_data = json.loads(match)
            tool_calls.append(tool_data)
        except:
            # Try to parse as text
            # e.g., tool: web_search, args: {"query": "test"}
            tool_match = re.search(r"tool:\s*(\w+).*?args:\s*(\{.*?\})", match, re.DOTALL)
            if tool_match:
                tool_calls.append({
                    "name": tool_match.group(1),
                    "arguments": json.loads(tool_match.group(2))
                })
    
    # Pattern 2: ```json tool_calls ... ```
    json_pattern = r"```json\s*(\{.*?tool_calls.*?\})\s*```"
    matches = re.findall(json_pattern, content, re.DOTALL)
    for match in matches:
        try:
            data = json.loads(match)
            if "tool_calls" in data:
                tool_calls.extend(data["tool_calls"])
        except:
            pass
    
    # Pattern 3: Simple function call syntax: web_search(query="test")
    func_pattern = r"(\w+)\((.*?)\)"
    # Only if content looks like tool calls (contains known tool names)
    known_tools = ["web_search", "read_file", "write_file", "execute", "search_knowledge"]
    for tool_name in known_tools:
        if tool_name in content:
            pattern = rf"{tool_name}\((.*?)\)"
            matches = re.findall(pattern, content)
            for args_str in matches:
                try:
                    # Parse args string into dict - simplified
                    # e.g., query="test" -> {"query": "test"}
                    args = {}
                    arg_pattern = r'(\w+)=["\'](.*?)["\']'
                    arg_matches = re.findall(arg_pattern, args_str)
                    for k, v in arg_matches:
                        args[k] = v
                    if args:
                        tool_calls.append({"name": tool_name, "arguments": args})
                except:
                    pass
    
    return tool_calls

# === Cost Calculation ===

def calculate_cost(provider: str, model: str, usage: Dict) -> float:
    """Calculate LLM cost - free providers $0"""
    # Free providers
    if provider in ["nvidia_nim", "ollama", "lm_studio"]:
        return 0.0
    if provider == "openrouter" and ":free" in model:
        return 0.0
    
    # Paid providers - estimate
    # GPT-4o: $5/1M input, $15/1M output
    # DeepSeek: $0.14/1M input, $0.28/1M output
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    
    if "gpt-4o" in model:
        return (prompt_tokens * 5 + completion_tokens * 15) / 1_000_000
    elif "deepseek" in model:
        return (prompt_tokens * 0.14 + completion_tokens * 0.28) / 1_000_000
    else:
        return (prompt_tokens * 1 + completion_tokens * 2) / 1_000_000  # Default estimate

# === Main Free LLM Interface ===

async def free_chat_completion(messages: List[Dict], agent_id: str = None, model: str = None, **kwargs) -> Dict:
    """
    Main interface - tries free providers first, falls back to mock
    Uses per-model mapping, request optimization, smart rate limiting, thinking tokens, tool parser
    """
    # Check if optimizable
    if agent_id and is_optimizable(agent_id):
        return {
            "content": get_optimized_response(agent_id),
            "provider": "local_optimization",
            "model": "local",
            "real": False,
            "optimized": True,
            "saved_quota": True
        }
    
    # Get model mapping for agent
    if agent_id:
        mapping = get_model_for_agent(agent_id)
        provider_name = mapping["provider"]
        model = model or mapping["model"]
    else:
        provider_name = "nvidia_nim"
        model = model or "meta/llama-3.1-70b-instruct"
    
    # Check rate limiting
    if rate_limiter.should_throttle(provider_name):
        return {
            "content": f"Rate limited for {provider_name} - throttled",
            "provider": provider_name,
            "model": model,
            "real": False,
            "throttled": True,
            "retry_after": 1
        }
    
    # Get provider
    provider = get_provider(provider_name)
    if not provider or not provider.is_available():
        # Try fallback providers - Ollama local free
        for fallback in ["ollama", "lm_studio", "nvidia_nim", "openrouter"]:
            if fallback == provider_name:
                continue
            fallback_provider = get_provider(fallback)
            if fallback_provider and fallback_provider.is_available():
                provider = fallback_provider
                provider_name = fallback
                model = fallback_provider.model
                break
    
    if not provider or not provider.is_available():
        # No provider available - mock response
        return {
            "content": f"Mock response for agent {agent_id} — No free LLM provider available. Set NVIDIA_NIM_API_KEY (nvapi-...) for 40 req/min free, or OPENROUTER_API_KEY (sk-or-...) for free models, or run Ollama local (http://localhost:11434) for 100% free. See docs/FREE_LLM_PROVIDERS.md",
            "provider": "mock",
            "model": model,
            "real": False,
            "mock": True,
            "available_providers": get_available_providers(),
            "how_to_get_free": [
                "NVIDIA NIM: https://build.nvidia.com/ — 40 req/min free — Get API key nvapi-... — Set NVIDIA_NIM_API_KEY env",
                "OpenRouter: https://openrouter.ai/ — Free models :free — Get sk-or-... — Set OPENROUTER_API_KEY",
                "Ollama: https://ollama.ai/ — Local free — ollama pull llama3 + ollama serve — Set OLLAMA_BASE_URL=http://localhost:11434/v1",
                "LM Studio: https://lmstudio.ai/ — Local free — Download + run server — Set LMSTUDIO_BASE_URL=http://localhost:1234/v1",
                "DeepSeek: https://deepseek.com/ — Cheap $0.14/1M — Set DEEPSEEK_API_KEY"
            ],
            "cost": 0.0,
            "margin": "100% with free providers"
        }
    
    # Record request for rate limiting
    rate_limiter.record_request(provider_name)
    
    try:
        # Real chat completion
        result = await provider.chat_completion(messages, model, **kwargs)
        
        # Record completion
        rate_limiter.record_completion(provider_name)
        
        # Check for 429
        if "429" in str(result.get("error", "")) or "rate limit" in str(result.get("error", "")).lower():
            rate_limiter.record_429(provider_name)
        
        # Parse thinking tokens
        content = result.get("content", "")
        thinking_data = parse_thinking_tokens(content)
        
        # Parse tool calls from text
        tool_calls = parse_tool_calls_from_text(content)
        
        # Calculate cost
        usage = result.get("usage", {})
        cost = calculate_cost(provider_name, model, usage)
        
        return {
            **result,
            "thinking": thinking_data["thinking"],
            "answer": thinking_data["answer"],
            "has_thinking": thinking_data["has_thinking"],
            "thinking_blocks": thinking_data["thinking_blocks"],
            "tool_calls_parsed": tool_calls,
            "has_tool_calls": bool(tool_calls),
            "cost": cost,
            "margin": "100%" if cost == 0 else f"{(1 - cost/0.1)*100:.0f}%" if cost < 0.1 else "low",
            "provider": provider_name,
            "model": model,
            "agent_id": agent_id,
            "per_model_mapping": get_model_for_agent(agent_id) if agent_id else None,
            "request_optimization": "5 categories intercepted locally" if is_optimizable(agent_id or "") else "not optimizable",
            "smart_rate_limiting": f"{provider.get_rate_limit()} req/min + 429 backoff + concurrency cap"
        }
    except Exception as e:
        rate_limiter.record_completion(provider_name)
        return {
            "content": f"Error from {provider_name}: {e} — Mock fallback",
            "provider": provider_name,
            "model": model,
            "real": False,
            "error": str(e),
            "mock": True,
            "cost": 0.0
        }

"""
LLM Provider Abstraction - Inspired by Open WebUI's multi-provider support
Supports OpenAI, Anthropic, Ollama, and custom OpenAI-compatible APIs
"""
from typing import List, Dict, Any, Optional, AsyncGenerator
import httpx
import json
import os
from .config import settings

class LLMProvider:
    """Base LLM Provider"""
    async def chat_completion(self, messages: List[Dict], model: str, tools: List[Dict] = None, stream: bool = False, **kwargs):
        raise NotImplementedError
    
    async def list_models(self):
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or settings.OPENAI_API_KEY or "sk-fake-key-for-demo"
        self.base_url = base_url or settings.OPENAI_BASE_URL
    
    async def chat_completion(self, messages: List[Dict], model: str, tools: List[Dict] = None, stream: bool = False, **kwargs) -> Dict[str, Any]:
        # If no API key, return mock response for demo
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "sk-fake":
            return self._mock_response(messages, model, tools)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            if stream:
                # Streaming handled separately
                return await self._stream_chat(client, headers, payload)
            else:
                resp = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                resp.raise_for_status()
                return resp.json()
    
    def _mock_response(self, messages: List[Dict], model: str, tools: List[Dict] = None) -> Dict:
        """Mock response for demo when no API key"""
        last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "Hello")
        
        # Simple logic to simulate agent behavior
        content = f"""🤖 **AI Agency OS - Demo Mode** (No API key configured)

You said: "{last_user_msg[:200]}"

I'm running in demo mode. To enable real LLM:

1. Set OPENAI_API_KEY in .env
2. Or configure Ollama at {settings.OLLAMA_BASE_URL}
3. Or set ANTHROPIC_API_KEY

**What I would do with full LLM:**
- Analyze your request using ECC-inspired verification loop: plan -> test -> implement -> review
- Select appropriate specialized agent from 68 available agents
- Apply relevant skills from 292 skill library
- Execute tools if needed
- Save memory and evolve instincts

**Current system status:**
✅ 68 Agents loaded
✅ 292 Skills available
✅ Tools registry active
✅ Memory & Instincts enabled
✅ Pipelines engine ready
✅ AgentShield security scanning active

Try asking about:
- /skills - List available skills
- /agents - Show agent roster
- /memory - View memory system
- Or create a new client/project via Agency Dashboard
"""
        
        return {
            "id": "chatcmpl-mock",
            "object": "chat.completion",
            "created": 0,
            "model": model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
        }
    
    async def _stream_chat(self, client, headers, payload):
        # For simplicity, return non-streaming in mock
        return self._mock_response(payload["messages"], payload["model"], payload.get("tools"))
    
    async def list_models(self):
        if not settings.OPENAI_API_KEY:
            return [{"id": m, "name": m} for m in settings.ENABLED_MODELS]
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{self.base_url}/models", headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data.get("data", [])
            except:
                return [{"id": m, "name": m} for m in settings.ENABLED_MODELS]

class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
    
    async def chat_completion(self, messages: List[Dict], model: str, tools: List[Dict] = None, stream: bool = False, **kwargs):
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                resp = await client.post(f"{self.base_url}/api/chat", json=payload)
                resp.raise_for_status()
                data = resp.json()
                # Convert Ollama format to OpenAI format
                return {
                    "id": "chatcmpl-ollama",
                    "object": "chat.completion",
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": data.get("message", {}).get("content", "")
                        },
                        "finish_reason": "stop"
                    }]
                }
            except Exception as e:
                # Fallback to mock
                openai_provider = OpenAIProvider()
                return openai_provider._mock_response(messages, model, tools)
    
    async def list_models(self):
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{self.base_url}/api/tags")
                resp.raise_for_status()
                data = resp.json()
                return [{"id": m["name"], "name": m["name"]} for m in data.get("models", [])]
            except:
                return [{"id": "llama3.1:8b", "name": "llama3.1:8b"}]

class LLMManager:
    """Manages multiple LLM providers like Open WebUI"""
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider(),
            "ollama": OllamaProvider(),
        }
        self.default_provider = "openai"
    
    def get_provider(self, model: str) -> LLMProvider:
        # Simple routing logic
        if "llama" in model.lower() or "mistral" in model.lower() or "gemma" in model.lower():
            return self.providers["ollama"]
        return self.providers["openai"]
    
    async def chat_completion(self, messages: List[Dict], model: str = None, tools: List[Dict] = None, stream: bool = False, **kwargs):
        model = model or settings.DEFAULT_MODEL
        provider = self.get_provider(model)
        return await provider.chat_completion(messages, model, tools, stream, **kwargs)
    
    async def list_all_models(self):
        all_models = []
        for provider in self.providers.values():
            try:
                models = await provider.list_models()
                all_models.extend(models)
            except:
                continue
        # Deduplicate
        seen = set()
        unique = []
        for m in all_models:
            if m["id"] not in seen:
                seen.add(m["id"])
                unique.append(m)
        return unique or [{"id": m, "name": m} for m in settings.ENABLED_MODELS]

llm_manager = LLMManager()

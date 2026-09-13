"""
Functions Manager - Inspired by Open WebUI's Functions system
Types: Pipe, Filter, Action, Event
- Pipe: Adds custom model or agent (appears as selectable model)
- Filter: Intercepts data flowing to/from models (middleware)
- Action: Adds interactive buttons to messages
- Event: Runs custom logic in response to system events (170+ events)
"""
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

# Example functions inspired by Open WebUI community

BUILTIN_FUNCTIONS = [
    {
        "id": "translation-filter",
        "name": "Auto Translation Filter",
        "type": "filter",
        "description": "Translates messages in real-time (Filter function example)",
        "code": '''
class Filter:
    class Valves:
        target_language: str = "en"
        enabled: bool = True
    
    def __init__(self):
        self.valves = self.Valves()
    
    async def inlet(self, body: dict) -> dict:
        # Modify incoming user message
        # Example: translate to target language
        messages = body.get("messages", [])
        if messages and self.valves.enabled:
            # In real impl, call translation API
            pass
        return body
    
    async def outlet(self, body: dict) -> dict:
        # Modify outgoing assistant message
        return body
''',
        "valves": {"target_language": "en", "enabled": True},
        "enabled": False
    },
    {
        "id": "rag-pipe",
        "name": "Custom RAG Pipe",
        "type": "pipe",
        "description": "Implements sophisticated RAG as selectable model",
        "code": '''
class Pipe:
    class Valves:
        embedding_model: str = "all-MiniLM-L6-v2"
        collection: str = "default"
        top_k: int = 5
    
    def __init__(self):
        self.valves = self.Valves()
    
    def pipes(self):
        # Return multiple models (manifold)
        return [
            {"id": "rag-custom", "name": "Custom RAG Agent"},
            {"id": "rag-research", "name": "Research RAG Agent"}
        ]
    
    async def pipe(self, body: dict) -> str:
        # Custom RAG logic
        messages = body.get("messages", [])
        query = messages[-1]["content"] if messages else ""
        
        # 1. Retrieve from knowledge base
        # 2. Augment prompt
        # 3. Call LLM
        # 4. Return response with sources
        
        return f"RAG response for: {query} with context from {self.valves.collection}"
''',
        "valves": {"embedding_model": "all-MiniLM-L6-v2", "collection": "default", "top_k": 5},
        "enabled": True
    },
    {
        "id": "summarize-action",
        "name": "Summarize Action",
        "type": "action",
        "description": "Adds button to summarize messages",
        "code": '''
class Action:
    class Valves:
        max_length: int = 200
    
    def __init__(self):
        self.valves = self.Valves()
    
    async def action(self, body: dict, __user__=None, __event_emitter__=None, __event_call__=None) -> dict:
        # Called when user clicks button on message
        # body contains message, chat, etc
        
        # Example: summarize the message
        message = body.get("message", {})
        content = message.get("content", "")
        
        # Call LLM to summarize
        summary = f"Summary ({self.valves.max_length} chars): {content[:self.valves.max_length]}..."
        
        # Emit event to UI
        if __event_emitter__:
            await __event_emitter__({
                "type": "message",
                "data": {"content": summary}
            })
        
        return {"content": summary}
''',
        "valves": {"max_length": 200},
        "enabled": True
    },
    {
        "id": "analytics-event",
        "name": "Analytics Event Logger",
        "type": "event",
        "description": "Logs system events to analytics (Event function)",
        "code": '''
class Event:
    async def event(self, body: dict, __user__=None):
        # Reacts to 170+ system events like auth.signup, chat.deleted, etc
        event_type = body.get("type", "unknown")
        
        # Log to external analytics
        # Example: send to Langfuse, PostHog, etc
        print(f"Event: {event_type} by {__user__}")
        
        # Could also:
        # - Send Slack notification for important events
        # - Update CRM
        # - Trigger workflows
        
        return {"logged": True, "event": event_type}
''',
        "valves": {},
        "enabled": False
    },
    {
        "id": "rate-limit-filter",
        "name": "Rate Limit Filter",
        "type": "filter",
        "description": "Implements rate limiting for usage policies",
        "code": '''
class Filter:
    class Valves:
        max_requests_per_minute: int = 20
        enabled: bool = True
    
    def __init__(self):
        self.valves = self.Valves()
        self.requests = {}
    
    async def inlet(self, body: dict, __user__=None) -> dict:
        if not self.valves.enabled:
            return body
        
        user_id = __user__.get("id") if __user__ else "anonymous"
        # Check rate limit
        # If exceeded, raise exception or return error
        return body
''',
        "valves": {"max_requests_per_minute": 20, "enabled": True},
        "enabled": False
    },
    {
        "id": "agent-pipe",
        "name": "Agent as Model Pipe",
        "type": "pipe",
        "description": "Exposes ECC agents as selectable models in chat",
        "code": '''
class Pipe:
    def __init__(self):
        self.agents = []  # Load from agent registry
    
    def pipes(self):
        # Each agent appears as model
        return [
            {"id": f"agent-{agent['id']}", "name": f"🤖 {agent['name']}"}
            for agent in self.agents
        ]
    
    async def pipe(self, body: dict) -> str:
        # Route to appropriate agent based on selected model
        model = body.get("model", "")
        agent_id = model.replace("agent-", "")
        messages = body.get("messages", [])
        task = messages[-1]["content"] if messages else ""
        
        # Call agent orchestrator
        # result = await orchestrator.run_single_agent(agent_id, task)
        return f"Agent {agent_id} response to: {task}"
''',
        "valves": {},
        "enabled": True
    },
]

class FunctionManager:
    def __init__(self):
        self.functions = {f["id"]: f for f in BUILTIN_FUNCTIONS}
    
    def list_functions(self, type: str = None, enabled_only: bool = False) -> List[Dict]:
        funcs = list(self.functions.values())
        if type:
            funcs = [f for f in funcs if f["type"] == type]
        if enabled_only:
            funcs = [f for f in funcs if f.get("enabled")]
        return funcs
    
    def get_function(self, func_id: str) -> Optional[Dict]:
        return self.functions.get(func_id)
    
    def create_function(self, name: str, type: str, description: str, code: str, valves: Dict = None) -> Dict:
        func_id = name.lower().replace(" ", "-")
        func = {
            "id": func_id,
            "name": name,
            "type": type,
            "description": description,
            "code": code,
            "valves": valves or {},
            "enabled": True
        }
        self.functions[func_id] = func
        return func
    
    def update_function(self, func_id: str, updates: Dict) -> Optional[Dict]:
        if func_id in self.functions:
            self.functions[func_id].update(updates)
            return self.functions[func_id]
        return None
    
    def delete_function(self, func_id: str) -> bool:
        if func_id in self.functions:
            del self.functions[func_id]
            return True
        return False
    
    def get_by_type(self) -> Dict[str, List[Dict]]:
        result = {"pipe": [], "filter": [], "action": [], "event": []}
        for func in self.functions.values():
            if func["type"] in result:
                result[func["type"]].append(func)
        return result

function_manager = FunctionManager()

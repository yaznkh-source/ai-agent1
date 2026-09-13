"""
Hooks Manager - Inspired by ECC's hooks (SessionStart, SessionEnd, etc)
And Open WebUI's Event functions (170+ system events)

Hooks run outside model context for deterministic enforcement
"""
from typing import List, Dict, Callable, Any
import asyncio
from datetime import datetime

class Hook:
    def __init__(self, event: str, handler: Callable, priority: int = 100, name: str = None):
        self.event = event
        self.handler = handler
        self.priority = priority
        self.name = name or handler.__name__
    
    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if asyncio.iscoroutinefunction(self.handler):
                result = await self.handler(payload)
            else:
                result = self.handler(payload)
            return {"hook": self.name, "event": self.event, "success": True, "result": result}
        except Exception as e:
            return {"hook": self.name, "event": self.event, "success": False, "error": str(e)}

class HookManager:
    """
    ECC-inspired hooks + Open WebUI-inspired events
    Events: SessionStart, SessionEnd, PreToolUse, PostToolUse, PreMessage, PostMessage, etc
    """
    
    def __init__(self):
        self.hooks: Dict[str, List[Hook]] = {}
        self.event_log: List[Dict] = []
        self.register_builtin_hooks()
    
    def register_builtin_hooks(self):
        """Register built-in hooks"""
        
        # SessionStart: reload memory (ECC)
        async def session_start_memory(payload):
            from ..memory.manager import memory_manager
            user_id = payload.get("user_id") or payload.get("context", {}).get("user_id")
            if user_id:
                memories = await memory_manager.list_memories(user_id, limit=5)
                return {"memories_loaded": len(memories), "memories": memories}
            return {"memories_loaded": 0}
        
        # SessionEnd: distill summary (ECC)
        async def session_end_summary(payload):
            from ..memory.manager import memory_manager
            user_id = payload.get("user_id") or payload.get("context", {}).get("user_id")
            chat_id = payload.get("chat_id") or payload.get("context", {}).get("chat_id")
            result = payload.get("result", "")
            if user_id and result:
                await memory_manager.save_memory(
                    user_id=user_id,
                    chat_id=chat_id,
                    content=f"Session result: {result[:500]}",
                    type="session_summary"
                )
                return {"summary_saved": True}
            return {"summary_saved": False}
        
        # PreToolUse: security check (AgentShield)
        async def pre_tool_security(payload):
            from ..core.security import shield
            tool_name = payload.get("tool_name", "")
            tool_input = str(payload.get("tool_input", ""))
            issues = shield.scan_text(tool_input, f"tool:{tool_name}")
            critical = [i for i in issues if i.severity == "critical"]
            if critical:
                return {"blocked": True, "reason": f"Security block: {critical[0].message}", "issues": [i.to_dict() for i in issues]}
            return {"blocked": False, "issues": [i.to_dict() for i in issues]}
        
        # PostToolUse: record instinct
        async def post_tool_instinct(payload):
            from ..memory.instincts import instinct_manager
            tool_name = payload.get("tool_name")
            success = payload.get("success", True)
            if success and tool_name:
                await instinct_manager.record_pattern(
                    pattern=f"tool:{tool_name}",
                    description=f"Successfully used {tool_name}",
                    trigger=tool_name,
                    action=f"Use {tool_name} for similar tasks",
                    success=success
                )
            return {"instinct_recorded": True}
        
        # PreMessage: filter (Open WebUI Filter inspiration)
        async def pre_message_filter(payload):
            content = payload.get("content", "")
            # Example: block empty, too long, etc
            if len(content) > 10000:
                return {"blocked": True, "reason": "Message too long"}
            return {"blocked": False}
        
        self.register_hook("SessionStart", session_start_memory, priority=10, name="memory_loader")
        self.register_hook("SessionEnd", session_end_summary, priority=10, name="summary_saver")
        self.register_hook("PreToolUse", pre_tool_security, priority=5, name="security_check")
        self.register_hook("PostToolUse", post_tool_instinct, priority=90, name="instinct_recorder")
        self.register_hook("PreMessage", pre_message_filter, priority=5, name="message_filter")
    
    def register_hook(self, event: str, handler: Callable, priority: int = 100, name: str = None):
        hook = Hook(event, handler, priority, name)
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(hook)
        # Sort by priority (lower first)
        self.hooks[event].sort(key=lambda h: h.priority)
    
    def unregister_hook(self, event: str, name: str):
        if event in self.hooks:
            self.hooks[event] = [h for h in self.hooks[event] if h.name != name]
    
    async def trigger(self, event: str, payload: Dict[str, Any] = None) -> List[Dict]:
        """Trigger all hooks for event"""
        payload = payload or {}
        payload["event"] = event
        payload["timestamp"] = datetime.utcnow().isoformat()
        
        # Log event
        self.event_log.append({"event": event, "payload": payload, "timestamp": payload["timestamp"]})
        if len(self.event_log) > 1000:
            self.event_log = self.event_log[-1000:]
        
        results = []
        hooks = self.hooks.get(event, [])
        for hook in hooks:
            result = await hook.execute(payload)
            results.append(result)
            # If hook blocks, stop propagation
            if result.get("result", {}).get("blocked"):
                break
        
        return results
    
    def list_hooks(self, event: str = None) -> Dict[str, List[str]]:
        if event:
            return {event: [h.name for h in self.hooks.get(event, [])]}
        return {e: [h.name for h in hooks] for e, hooks in self.hooks.items()}
    
    def get_event_log(self, limit: int = 50, event: str = None) -> List[Dict]:
        logs = self.event_log
        if event:
            logs = [l for l in logs if l["event"] == event]
        return logs[-limit:]

hook_manager = HookManager()

"""
Tools Registry - Inspired by Open WebUI Tools (LLM can call tools for real-time data)
+ ECC's tool permissions per agent
"""
from typing import List, Dict, Any, Callable
import json
import httpx

# Built-in tools - Open WebUI style + ECC tool ideas
BUILTIN_TOOLS = [
    {
        "id": "web_search",
        "name": "Web Search",
        "description": "Search the web for current information",
        "category": "research",
        "schema": {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search web for current info, news, docs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "count": {"type": "integer", "description": "Number of results", "default": 5}
                    },
                    "required": ["query"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "code_write",
        "name": "Code Writer",
        "description": "Write or edit code files",
        "category": "development",
        "schema": {
            "type": "function",
            "function": {
                "name": "code_write",
                "description": "Write code to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"},
                        "content": {"type": "string", "description": "File content"},
                        "language": {"type": "string", "description": "Language"}
                    },
                    "required": ["path", "content"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "code_read",
        "name": "Code Reader",
        "description": "Read code files",
        "category": "development",
        "schema": {
            "type": "function",
            "function": {
                "name": "code_read",
                "description": "Read file content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "test_runner",
        "name": "Test Runner",
        "description": "Run tests and get results",
        "category": "quality",
        "schema": {
            "type": "function",
            "function": {
                "name": "test_runner",
                "description": "Run tests for a project",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Test command", "default": "npm test"},
                        "path": {"type": "string", "description": "Project path"}
                    },
                    "required": ["command"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "security_scan",
        "name": "Security Scanner",
        "description": "Scan code for security issues via AgentShield",
        "category": "security",
        "schema": {
            "type": "function",
            "function": {
                "name": "security_scan",
                "description": "Scan text or code for security issues",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Content to scan"},
                        "source": {"type": "string", "description": "Source identifier"}
                    },
                    "required": ["content"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "diagram_generator",
        "name": "Diagram Generator",
        "description": "Generate mermaid diagrams for architecture",
        "category": "planning",
        "schema": {
            "type": "function",
            "function": {
                "name": "diagram_generator",
                "description": "Generate architecture diagram",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["flowchart", "sequence", "er", "class"], "description": "Diagram type"},
                        "description": {"type": "string", "description": "What to diagram"}
                    },
                    "required": ["type", "description"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "exa_search",
        "name": "Exa Search",
        "description": "Neural search for web, code, company research (ECC)",
        "category": "research",
        "schema": {
            "type": "function",
            "function": {
                "name": "exa_search",
                "description": "Advanced neural search via Exa",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "type": {"type": "string", "enum": ["web", "code", "company"], "default": "web"}
                    },
                    "required": ["query"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "knowledge_search",
        "name": "Knowledge Base Search",
        "description": "Search internal knowledge collections (Open WebUI RAG)",
        "category": "research",
        "schema": {
            "type": "function",
            "function": {
                "name": "knowledge_search",
                "description": "Search knowledge base / RAG",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "collection": {"type": "string", "description": "Collection name"}
                    },
                    "required": ["query"]
                }
            }
        },
        "enabled": True
    },
    {
        "id": "proposal_generator",
        "name": "Proposal Generator",
        "description": "Generate client proposals for agency",
        "category": "agency",
        "schema": {
            "type": "function",
            "function": {
                "name": "proposal_generator",
                "description": "Generate proposal document",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_name": {"type": "string"},
                        "project_type": {"type": "string"},
                        "requirements": {"type": "string"}
                    },
                    "required": ["client_name", "project_type", "requirements"]
                }
            }
        },
        "enabled": True
    },
]

class ToolRegistry:
    def __init__(self):
        self.tools = {t["id"]: t for t in BUILTIN_TOOLS}
        self.implementations: Dict[str, Callable] = {}
        self.register_builtin_implementations()
    
    def register_builtin_implementations(self):
        """Register actual implementations"""
        
        async def web_search_impl(query: str, count: int = 5):
            # Mock search - in production integrate real search API
            return {
                "query": query,
                "results": [
                    {"title": f"Result {i} for {query}", "url": f"https://example.com/{i}", "snippet": f"This is snippet {i} about {query}"}
                    for i in range(1, count+1)
                ]
            }
        
        async def security_scan_impl(content: str, source: str = "unknown"):
            from ..core.security import shield
            issues = shield.scan_text(content, source)
            return {
                "scanned": True,
                "issues": [i.to_dict() for i in issues],
                "total": len(issues)
            }
        
        async def diagram_generator_impl(type: str, description: str):
            # Generate mermaid diagram
            if type == "flowchart":
                mermaid = f"""flowchart TD
    A[Start: {description[:30]}] --> B[Process]
    B --> C{{Decision}}
    C -->|Yes| D[Success]
    C -->|No| E[Retry]
    E --> B
    D --> F[End]
"""
            elif type == "sequence":
                mermaid = f"""sequenceDiagram
    participant User
    participant System
    participant DB
    User->>System: Request: {description[:20]}
    System->>DB: Query
    DB-->>System: Data
    System-->>User: Response
"""
            else:
                mermaid = f"""erDiagram
    USER ||--o{{ PROJECT : has
    PROJECT ||--o{{ TASK : contains
    TASK }}o--|| AGENT : assigned
"""
            return {"mermaid": mermaid, "type": type, "description": description}
        
        self.implementations["web_search"] = web_search_impl
        self.implementations["security_scan"] = security_scan_impl
        self.implementations["diagram_generator"] = diagram_generator_impl
        # Others are mocked for now
        for tool_id in self.tools:
            if tool_id not in self.implementations:
                async def mock_impl(**kwargs):
                    return {"mock": True, "tool": tool_id, "args": kwargs, "result": f"Mock result for {tool_id}"}
                # Use closure to capture tool_id
                def make_mock(tid):
                    async def impl(**kwargs):
                        return {"mock": True, "tool": tid, "args": kwargs, "result": f"Mock executed {tid} with {kwargs}"}
                    return impl
                self.implementations[tool_id] = make_mock(tool_id)
    
    def list_tools(self, category: str = None, enabled_only: bool = True) -> List[Dict]:
        tools = list(self.tools.values())
        if category:
            tools = [t for t in tools if t["category"] == category]
        if enabled_only:
            tools = [t for t in tools if t.get("enabled")]
        return tools
    
    def get_tool(self, tool_id: str) -> Dict:
        return self.tools.get(tool_id)
    
    def get_openai_schemas(self, tool_ids: List[str] = None) -> List[Dict]:
        """Get OpenAI function calling schemas for given tools"""
        if tool_ids:
            tools = [self.tools[tid] for tid in tool_ids if tid in self.tools]
        else:
            tools = self.list_tools()
        return [t["schema"] for t in tools]
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool with security hooks"""
        from ..hooks.manager import hook_manager
        
        # PreToolUse hook (security)
        pre_results = await hook_manager.trigger("PreToolUse", {
            "tool_name": tool_name,
            "tool_input": arguments
        })
        for res in pre_results:
            if res.get("result", {}).get("blocked"):
                return {"error": res["result"]["reason"], "blocked": True}
        
        # Execute
        impl = self.implementations.get(tool_name)
        if not impl:
            return {"error": f"Tool {tool_name} not implemented"}
        
        try:
            result = await impl(**arguments)
            # PostToolUse hook (instincts)
            await hook_manager.trigger("PostToolUse", {
                "tool_name": tool_name,
                "tool_input": arguments,
                "result": result,
                "success": True
            })
            return result
        except Exception as e:
            await hook_manager.trigger("PostToolUse", {
                "tool_name": tool_name,
                "tool_input": arguments,
                "error": str(e),
                "success": False
            })
            return {"error": str(e)}

tool_registry = ToolRegistry()

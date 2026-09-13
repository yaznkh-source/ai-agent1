"""
Pydantic schemas for API
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

# Chat
class ChatCreate(BaseModel):
    title: str = "New Chat"
    model: str = "gpt-4o-mini"
    agent_id: Optional[str] = None
    project_id: Optional[str] = None

class MessageCreate(BaseModel):
    role: str
    content: str
    tool_calls: Optional[List[Dict]] = None

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "gpt-4o-mini"
    messages: List[Dict[str, Any]]
    stream: bool = False
    agent_id: Optional[str] = None
    tools: Optional[List[Dict]] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None

# Agents
class AgentRunRequest(BaseModel):
    agent_id: str
    task: str
    context: Optional[Dict] = None
    chat_history: Optional[List[Dict]] = None

class WorkflowRunRequest(BaseModel):
    workflow_id: Optional[str] = None
    workflow: Optional[List[Dict]] = None
    task: str
    context: Optional[Dict] = None

# Skills
class SkillCreate(BaseModel):
    id: str
    name: str
    category: str
    description: str
    content: str

# Memory
class MemoryCreate(BaseModel):
    content: str
    type: str = "fact"
    chat_id: Optional[str] = None
    confidence: float = 1.0
    meta: Optional[Dict] = None

# Pipeline
class PipelineCreate(BaseModel):
    name: str
    description: str
    steps: List[Dict]
    valves: Optional[Dict] = None

class PipelineExecuteRequest(BaseModel):
    context: Dict[str, Any]

# Agency
class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    meta: Optional[Dict] = None

class ProjectCreate(BaseModel):
    client_id: str
    name: str
    description: Optional[str] = None
    workflow: Optional[Dict] = None
    agents: Optional[List[str]] = None
    meta: Optional[Dict] = None

class TaskCreate(BaseModel):
    project_id: str
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    assigned_agent: Optional[str] = None
    skill_used: Optional[str] = None
    meta: Optional[Dict] = None

# Tools
class ToolExecuteRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

# Functions
class FunctionCreate(BaseModel):
    name: str
    type: str  # pipe, filter, action, event
    description: str
    code: str
    valves: Optional[Dict] = None

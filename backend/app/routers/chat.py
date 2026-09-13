"""
Chat router - Open WebUI-like chat + ECC agent integration
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db, Chat, Message, SessionLocal
from ..core.llm import llm_manager
from ..models.schemas import ChatCreate, ChatCompletionRequest
from ..agents.definitions import get_agent_by_id
from ..agents.orchestrator import orchestrator
from ..tools.registry import tool_registry
from ..memory.manager import memory_manager
from ..hooks.manager import hook_manager
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/chats", tags=["chats"])

@router.get("/")
async def list_chats(user_id: str = "default-user", db: Session = Depends(get_db)):
    chats = db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.updated_at.desc()).all()
    return [{
        "id": c.id,
        "title": c.title,
        "model": c.model,
        "agent_id": c.agent_id,
        "project_id": c.project_id,
        "created_at": c.created_at.isoformat(),
        "updated_at": c.updated_at.isoformat(),
        "meta": c.meta
    } for c in chats]

@router.post("/")
async def create_chat(chat: ChatCreate, user_id: str = "default-user", db: Session = Depends(get_db)):
    new_chat = Chat(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=chat.title,
        model=chat.model,
        agent_id=chat.agent_id,
        project_id=chat.project_id,
        meta={}
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    
    # Trigger SessionStart hook
    await hook_manager.trigger("SessionStart", {
        "user_id": user_id,
        "chat_id": new_chat.id,
        "agent_id": chat.agent_id
    })
    
    return {
        "id": new_chat.id,
        "title": new_chat.title,
        "model": new_chat.model,
        "agent_id": new_chat.agent_id
    }

@router.get("/{chat_id}")
async def get_chat(chat_id: str, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(404, "Chat not found")
    
    messages = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at).all()
    
    return {
        "id": chat.id,
        "title": chat.title,
        "model": chat.model,
        "agent_id": chat.agent_id,
        "project_id": chat.project_id,
        "created_at": chat.created_at.isoformat(),
        "messages": [{
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "tool_calls": m.tool_calls,
            "created_at": m.created_at.isoformat(),
            "meta": m.meta
        } for m in messages]
    }

@router.delete("/{chat_id}")
async def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(404, "Chat not found")
    
    db.query(Message).filter(Message.chat_id == chat_id).delete()
    db.delete(chat)
    db.commit()
    
    await hook_manager.trigger("chat.deleted", {"chat_id": chat_id})
    
    return {"deleted": True}

@router.post("/{chat_id}/messages")
async def add_message(chat_id: str, msg: dict, user_id: str = "default-user", db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(404, "Chat not found")
    
    # PreMessage hook
    pre = await hook_manager.trigger("PreMessage", {"content": msg.get("content", ""), "chat_id": chat_id})
    for r in pre:
        if r.get("result", {}).get("blocked"):
            raise HTTPException(400, r["result"]["reason"])
    
    message = Message(
        id=str(uuid.uuid4()),
        chat_id=chat_id,
        role=msg.get("role", "user"),
        content=msg.get("content", ""),
        tool_calls=msg.get("tool_calls"),
        meta=msg.get("meta", {})
    )
    db.add(message)
    chat.updated_at = datetime.utcnow()
    
    # Auto-title from first user message
    if chat.title == "New Chat" and msg.get("role") == "user":
        chat.title = msg.get("content", "")[:50]
    
    db.commit()
    
    return {"id": message.id, "role": message.role, "content": message.content}

@router.post("/completions")
async def chat_completion(req: ChatCompletionRequest, user_id: str = "default-user", db: Session = Depends(get_db)):
    """
    OpenAI-compatible chat completions endpoint
    Supports agent routing, tools, memory
    """
    messages = req.messages
    
    # If agent_id specified, use agent orchestrator
    if req.agent_id:
        agent = get_agent_by_id(req.agent_id)
        if agent:
            last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
            result = await orchestrator.run_single_agent(
                agent_id=req.agent_id,
                task=last_user,
                context={"user_id": user_id},
                chat_history=messages[:-1]
            )
            return {
                "id": f"chatcmpl-{uuid.uuid4()}",
                "object": "chat.completion",
                "created": int(datetime.utcnow().timestamp()),
                "model": req.model,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": result.get("result", "")},
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300},
                "agent": {"id": req.agent_id, "name": agent["name"]}
            }
    
    # Get tools schemas if requested
    tools = req.tools
    if not tools and req.agent_id:
        agent = get_agent_by_id(req.agent_id)
        if agent and agent.get("tools"):
            tools = tool_registry.get_openai_schemas(agent["tools"])
    
    # Call LLM
    response = await llm_manager.chat_completion(
        messages=messages,
        model=req.model,
        tools=tools,
        stream=req.stream,
        temperature=req.temperature
    )
    
    # Check if LLM wants to call tools
    choice = response["choices"][0]
    message = choice.get("message", {})
    if message.get("tool_calls"):
        # Execute tools
        tool_results = []
        for tc in message["tool_calls"]:
            func_name = tc["function"]["name"]
            args = {}
            try:
                import json
                args = json.loads(tc["function"]["arguments"])
            except:
                args = {}
            
            tool_result = await tool_registry.execute_tool(func_name, args)
            tool_results.append({
                "tool_call_id": tc["id"],
                "role": "tool",
                "name": func_name,
                "content": str(tool_result)
            })
        
        # Second LLM call with tool results
        messages.append(message)
        messages.extend(tool_results)
        response = await llm_manager.chat_completion(
            messages=messages,
            model=req.model,
            stream=False,
            temperature=req.temperature
        )
    
    # Save to memory if chat context exists
    # (In real app, would save to specific chat)
    
    await hook_manager.trigger("PostMessage", {
        "user_id": user_id,
        "model": req.model,
        "messages": messages,
        "response": response
    })
    
    return response

@router.get("/models/list")
async def list_models():
    models = await llm_manager.list_all_models()
    return {"data": models}

@router.post("/models/list")
async def list_models_post():
    models = await llm_manager.list_all_models()
    return {"data": models}

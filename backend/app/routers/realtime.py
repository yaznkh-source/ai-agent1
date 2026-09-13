"""
Realtime Router - WebSocket + SSE for live updates
Task A10: WebSocket Auth - JWT verification
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from ..core.websocket import manager, broadcaster
from ..core.auth import decode_token
from typing import Dict, Optional
import asyncio
import json

router = APIRouter(prefix="/api/realtime", tags=["realtime"])

@router.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str, user_id: str = None, token: str = Query(None)):
    # Task A10: WebSocket Auth - verify JWT token if provided
    verified_user_id = None
    auth_method = "anonymous"
    
    if token:
        payload = decode_token(token)
        if payload:
            verified_user_id = payload.get("sub")
            auth_method = "jwt"
            # Use verified user_id from token, not query param
            user_id = verified_user_id
            print(f"🔒 WS Authenticated via JWT: user {verified_user_id} in room {room}")
        else:
            await websocket.close(code=1008, reason="Invalid token")
            return
    else:
        # No token - allow but as anonymous with warning
        # In production, you might want to reject anonymous
        from ..core.config import settings
        if settings.ENV == "production":
            # In prod, require token or at least log
            print(f"⚠️ WS Anonymous connection in production - room {room}, user_id {user_id} - should require JWT")
        else:
            print(f"⚠️ WS Anonymous connection in dev - room {room}, user_id {user_id}")
        auth_method = "anonymous"
    
    await manager.connect(websocket, room, user_id)
    # Send auth confirmation
    await websocket.send_text(json.dumps({"type": "auth", "user_id": user_id, "auth_method": auth_method, "room": room}))
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Echo or handle message - include verified user_id
                await manager.send_to_room({
                    "type": "message",
                    "data": message,
                    "room": room,
                    "user_id": user_id,
                    "auth_method": auth_method
                }, room)
            except:
                await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, room, user_id)

@router.websocket("/ws")
async def websocket_general(websocket: WebSocket, user_id: str = None, token: str = Query(None)):
    # Task A10: Same auth for general
    verified_user_id = None
    auth_method = "anonymous"
    
    if token:
        payload = decode_token(token)
        if payload:
            verified_user_id = payload.get("sub")
            auth_method = "jwt"
            user_id = verified_user_id
        else:
            await websocket.close(code=1008, reason="Invalid token")
            return
    
    await manager.connect(websocket, "general", user_id)
    await websocket.send_text(json.dumps({"type": "auth", "user_id": user_id, "auth_method": auth_method}))
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"General echo: {data} (user: {user_id}, auth: {auth_method})")
    except WebSocketDisconnect:
        manager.disconnect(websocket, "general", user_id)

@router.get("/rooms")
async def list_rooms():
    return {
        "rooms": list(manager.active_connections.keys()),
        "counts": {room: len(conns) for room, conns in manager.active_connections.items()},
        "total_connections": sum(len(conns) for conns in manager.active_connections.values())
    }

@router.post("/broadcast")
async def broadcast_message(payload: dict):
    room = payload.get("room", "general")
    message = payload.get("message", {})
    await manager.send_to_room(message, room)
    return {"broadcasted": True, "room": room, "message": message}

@router.post("/notify/task/{task_id}")
async def notify_task_update(task_id: str, payload: dict):
    status = payload.get("status", "updated")
    project_id = payload.get("project_id", "unknown")
    room = payload.get("room", "general")
    
    await broadcaster.broadcast_task_update(task_id, status, project_id, room)
    return {"notified": True, "task_id": task_id, "status": status}

@router.post("/notify/agent/{agent_id}")
async def notify_agent_event(agent_id: str, payload: dict):
    event_type = payload.get("type", "start")  # start, token, complete
    run_id = payload.get("run_id", "unknown")
    data = payload.get("data", "")
    room = payload.get("room", "general")
    
    if event_type == "start":
        await broadcaster.broadcast_agent_start(agent_id, data, run_id, room)
    elif event_type == "token":
        await broadcaster.broadcast_agent_token(agent_id, data, run_id, room)
    elif event_type == "complete":
        await broadcaster.broadcast_agent_complete(agent_id, data, run_id, room)
    
    return {"notified": True, "agent_id": agent_id, "type": event_type}

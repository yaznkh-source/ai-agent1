"""
WebSocket Manager - Real-time agent execution updates
Track C + D - Real-time collaboration
"""
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}  # room -> connections
        self.user_connections: Dict[str, WebSocket] = {}  # user_id -> websocket
    
    async def connect(self, websocket: WebSocket, room: str = "general", user_id: str = None):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket
        print(f"✅ WebSocket connected: room={room}, user={user_id}, total={len(self.active_connections[room])}")
    
    def disconnect(self, websocket: WebSocket, room: str = "general", user_id: str = None):
        if room in self.active_connections:
            if websocket in self.active_connections[room]:
                self.active_connections[room].remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
        print(f"❌ WebSocket disconnected: room={room}")
    
    async def send_to_room(self, message: dict, room: str = "general"):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                try:
                    await connection.send_json(message)
                except:
                    pass
    
    async def send_to_user(self, message: dict, user_id: str):
        if user_id in self.user_connections:
            try:
                await self.user_connections[user_id].send_json(message)
            except:
                pass
    
    async def broadcast(self, message: dict):
        for room_connections in self.active_connections.values():
            for connection in room_connections:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

# Real-time agent execution broadcaster
class AgentBroadcaster:
    """Broadcasts agent execution in real-time via WebSocket"""
    
    async def broadcast_agent_start(self, agent_id: str, task: str, run_id: str, room: str = "general"):
        await manager.send_to_room({
            "type": "agent_start",
            "agent_id": agent_id,
            "task": task[:100],
            "run_id": run_id,
            "timestamp": datetime.utcnow().isoformat()
        }, room)
    
    async def broadcast_agent_token(self, agent_id: str, token: str, run_id: str, room: str = "general"):
        await manager.send_to_room({
            "type": "agent_token",
            "agent_id": agent_id,
            "token": token,
            "run_id": run_id,
            "timestamp": datetime.utcnow().isoformat()
        }, room)
    
    async def broadcast_agent_complete(self, agent_id: str, result: str, run_id: str, room: str = "general"):
        await manager.send_to_room({
            "type": "agent_complete",
            "agent_id": agent_id,
            "result": result[:500],
            "run_id": run_id,
            "timestamp": datetime.utcnow().isoformat()
        }, room)
    
    async def broadcast_task_update(self, task_id: str, status: str, project_id: str, room: str = "general"):
        await manager.send_to_room({
            "type": "task_update",
            "task_id": task_id,
            "status": status,
            "project_id": project_id,
            "timestamp": datetime.utcnow().isoformat()
        }, room)
    
    async def broadcast_pipeline_step(self, pipeline_id: str, step_id: str, status: str, result: str = None, room: str = "general"):
        await manager.send_to_room({
            "type": "pipeline_step",
            "pipeline_id": pipeline_id,
            "step_id": step_id,
            "status": status,
            "result": result[:200] if result else None,
            "timestamp": datetime.utcnow().isoformat()
        }, room)

broadcaster = AgentBroadcaster()

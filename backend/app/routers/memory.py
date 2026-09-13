from fastapi import APIRouter, Depends, HTTPException
from ..memory.manager import memory_manager
from ..memory.instincts import instinct_manager
from ..models.schemas import MemoryCreate

router = APIRouter(prefix="/api/memory", tags=["memory"])

@router.get("/")
async def list_memories(user_id: str = "default-user", type: str = None, limit: int = 50):
    memories = await memory_manager.list_memories(user_id, type, limit)
    return {"memories": memories, "count": len(memories)}

@router.post("/")
async def create_memory(mem: MemoryCreate, user_id: str = "default-user"):
    result = await memory_manager.save_memory(
        user_id=user_id,
        content=mem.content,
        type=mem.type,
        chat_id=mem.chat_id,
        confidence=mem.confidence,
        meta=mem.meta
    )
    return result

@router.delete("/{memory_id}")
async def delete_memory(memory_id: str, user_id: str = "default-user"):
    deleted = await memory_manager.delete_memory(memory_id, user_id)
    if not deleted:
        raise HTTPException(404, "Memory not found")
    return {"deleted": True}

@router.get("/search")
async def search_memories(q: str, user_id: str = "default-user", limit: int = 5):
    memories = await memory_manager.get_relevant_memories(user_id, q, limit)
    return {
        "query": q,
        "memories": [{"id": m.id, "content": m.content, "type": m.type, "confidence": m.confidence} for m in memories]
    }

# Instincts endpoints (ECC continuous learning)
@router.get("/instincts/")
async def list_instincts(min_confidence: float = 0.0):
    instincts = await instinct_manager.list_instincts(min_confidence)
    return {"instincts": instincts, "count": len(instincts)}

@router.get("/instincts/search")
async def search_instincts(q: str, min_confidence: float = 0.6):
    instincts = await instinct_manager.get_relevant_instincts(q, min_confidence)
    return {"query": q, "instincts": instincts}

@router.post("/instincts/evolve")
async def evolve_instincts(payload: dict):
    instinct_ids = payload.get("instinct_ids", [])
    skill = await instinct_manager.evolve_to_skill(instinct_ids)
    if not skill:
        raise HTTPException(400, "Need at least 2 instincts to evolve")
    return {"evolved": True, "skill": skill}

@router.post("/instincts/record")
async def record_instinct(payload: dict):
    pattern = payload.get("pattern", "")
    description = payload.get("description", "")
    trigger = payload.get("trigger", "")
    action = payload.get("action", "")
    success = payload.get("success", True)
    instinct = await instinct_manager.record_pattern(pattern, description, trigger, action, success)
    return instinct

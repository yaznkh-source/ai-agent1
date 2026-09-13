"""
Memory Manager - Inspired by ECC's memory persistence + Open WebUI's chat history
SessionStart and SessionEnd hooks save/reload context, with character cap
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..core.database import Memory, SessionLocal
from datetime import datetime
import uuid

class MemoryManager:
    """
    Manages:
    - Session summaries (distilled from transcripts)
    - Facts (user preferences, project context)
    - Instincts (patterns learned)
    - Skill usage history
    """
    
    def __init__(self):
        self.max_chars = 10000  # Configurable cap so long history never blows context
    
    async def save_memory(self, user_id: str, content: str, type: str = "fact", chat_id: str = None, confidence: float = 1.0, meta: Dict = None) -> Dict:
        db = SessionLocal()
        try:
            memory = Memory(
                id=str(uuid.uuid4()),
                user_id=user_id,
                chat_id=chat_id,
                type=type,
                content=content[:5000],  # Cap individual memory
                confidence=confidence,
                meta=meta or {}
            )
            db.add(memory)
            db.commit()
            db.refresh(memory)
            return {
                "id": memory.id,
                "user_id": memory.user_id,
                "type": memory.type,
                "content": memory.content,
                "confidence": memory.confidence,
                "created_at": memory.created_at.isoformat()
            }
        finally:
            db.close()
    
    async def get_relevant_memories(self, user_id: str, query: str, limit: int = 5, type: str = None) -> List:
        """Simple keyword-based retrieval - could be upgraded to vector search with Chroma"""
        db = SessionLocal()
        try:
            q = db.query(Memory).filter(Memory.user_id == user_id)
            if type:
                q = q.filter(Memory.type == type)
            
            # Simple relevance: contains query words
            # In production, use embeddings + ChromaDB
            memories = q.order_by(Memory.created_at.desc()).limit(50).all()
            
            # Score by keyword overlap
            query_words = set(query.lower().split())
            scored = []
            for mem in memories:
                mem_words = set(mem.content.lower().split())
                overlap = len(query_words & mem_words)
                scored.append((overlap, mem))
            
            scored.sort(key=lambda x: x[0], reverse=True)
            return [m for score, m in scored[:limit] if score > 0 or len(scored) < limit]
        finally:
            db.close()
    
    async def get_session_summary(self, user_id: str, chat_id: str) -> Optional[str]:
        db = SessionLocal()
        try:
            mem = db.query(Memory).filter(
                Memory.user_id == user_id,
                Memory.chat_id == chat_id,
                Memory.type == "session_summary"
            ).order_by(Memory.created_at.desc()).first()
            return mem.content if mem else None
        finally:
            db.close()
    
    async def create_session_summary(self, user_id: str, chat_id: str, transcript: str) -> str:
        """Distill transcript into summary - ECC's session summary idea"""
        # Simple heuristic summary - in production use LLM to summarize
        lines = transcript.split("\n")[-20:]  # Last 20 lines
        summary = f"Session summary for chat {chat_id}:\n"
        summary += f"- Last interaction: {transcript[-200:]}...\n"
        summary += f"- Key topics: {', '.join(list(set(transcript.split()))[:10])}\n"
        
        await self.save_memory(
            user_id=user_id,
            chat_id=chat_id,
            content=summary,
            type="session_summary"
        )
        return summary
    
    async def list_memories(self, user_id: str, type: str = None, limit: int = 50) -> List[Dict]:
        db = SessionLocal()
        try:
            q = db.query(Memory).filter(Memory.user_id == user_id)
            if type:
                q = q.filter(Memory.type == type)
            memories = q.order_by(Memory.created_at.desc()).limit(limit).all()
            return [{
                "id": m.id,
                "type": m.type,
                "content": m.content,
                "confidence": m.confidence,
                "chat_id": m.chat_id,
                "created_at": m.created_at.isoformat(),
                "meta": m.meta
            } for m in memories]
        finally:
            db.close()
    
    async def delete_memory(self, memory_id: str, user_id: str) -> bool:
        db = SessionLocal()
        try:
            mem = db.query(Memory).filter(Memory.id == memory_id, Memory.user_id == user_id).first()
            if mem:
                db.delete(mem)
                db.commit()
                return True
            return False
        finally:
            db.close()

memory_manager = MemoryManager()

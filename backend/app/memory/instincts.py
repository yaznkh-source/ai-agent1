"""
Instincts - ECC's continuous learning v2
Extracts patterns from sessions into reusable instincts with confidence scoring,
then clusters them into full skills via /evolve
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from ..core.database import Instinct, SessionLocal
from datetime import datetime
import uuid
import re
from collections import Counter

class InstinctManager:
    """
    Continuous learning system:
    - Extracts patterns from successful sessions
    - Confidence scoring based on usage and success
    - Clustering into skills
    """
    
    def __init__(self):
        self.min_confidence = 0.6
        self.min_usage = 3
    
    async def record_pattern(self, pattern: str, description: str, trigger: str, action: str, success: bool = True) -> Dict:
        """Record a pattern observed in session"""
        db = SessionLocal()
        try:
            # Check if similar instinct exists
            existing = db.query(Instinct).filter(Instinct.pattern == pattern).first()
            if existing:
                existing.usage_count += 1
                # Update success rate
                total = existing.usage_count
                current_success = existing.success_rate * (total - 1)
                new_success = current_success + (1 if success else 0)
                existing.success_rate = new_success / total
                # Confidence increases with usage and success
                existing.confidence = min(0.95, existing.success_rate * (0.5 + 0.5 * min(total / 10, 1)))
                existing.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(existing)
                return self._to_dict(existing)
            else:
                instinct = Instinct(
                    id=str(uuid.uuid4()),
                    pattern=pattern,
                    description=description,
                    trigger=trigger,
                    action=action,
                    confidence=0.5 if success else 0.3,
                    usage_count=1,
                    success_rate=1.0 if success else 0.0
                )
                db.add(instinct)
                db.commit()
                db.refresh(instinct)
                return self._to_dict(instinct)
        finally:
            db.close()
    
    async def extract_instincts_from_session(self, session_transcript: str) -> List[Dict]:
        """Extract potential instincts from session - simplified version"""
        instincts = []
        
        # Pattern detection heuristics
        patterns = [
            (r"always (.*) before (.*)", "sequencing", "When doing {1}, always {0} first"),
            (r"remember to (.*)", "reminder", "Remember to {0}"),
            (r"prefer (.*) over (.*)", "preference", "Prefer {0} over {1}"),
            (r"check (.*) first", "verification", "Check {0} first"),
        ]
        
        for line in session_transcript.split("\n"):
            for regex, p_type, template in patterns:
                match = re.search(regex, line.lower())
                if match:
                    instinct = await self.record_pattern(
                        pattern=f"{p_type}:{match.group(0)[:50]}",
                        description=line[:200],
                        trigger=match.group(1) if match.groups() else line[:50],
                        action=template,
                        success=True
                    )
                    instincts.append(instinct)
        
        return instincts
    
    async def get_relevant_instincts(self, query: str, min_confidence: float = 0.6) -> List[Dict]:
        db = SessionLocal()
        try:
            instincts = db.query(Instinct).filter(
                Instinct.confidence >= min_confidence
            ).order_by(Instinct.confidence.desc()).limit(10).all()
            
            # Simple keyword filtering
            query_words = set(query.lower().split())
            relevant = []
            for inst in instincts:
                inst_words = set((inst.trigger + " " + inst.description).lower().split())
                if len(query_words & inst_words) > 0:
                    relevant.append(self._to_dict(inst))
            
            return relevant or [self._to_dict(i) for i in instincts[:3]]
        finally:
            db.close()
    
    async def list_instincts(self, min_confidence: float = 0.0) -> List[Dict]:
        db = SessionLocal()
        try:
            instincts = db.query(Instinct).filter(
                Instinct.confidence >= min_confidence
            ).order_by(Instinct.confidence.desc()).all()
            return [self._to_dict(i) for i in instincts]
        finally:
            db.close()
    
    async def evolve_to_skill(self, instinct_ids: List[str]) -> Optional[Dict]:
        """
        Cluster instincts into full skill via /evolve (ECC concept)
        When multiple related instincts have high confidence, create a skill
        """
        db = SessionLocal()
        try:
            instincts = db.query(Instinct).filter(Instinct.id.in_(instinct_ids)).all()
            if len(instincts) < 2:
                return None
            
            # Cluster by pattern similarity
            # Simple: if they share keywords, cluster
            all_triggers = " ".join([i.trigger for i in instincts])
            common_words = Counter(all_triggers.lower().split()).most_common(3)
            skill_name = "-".join([w for w, c in common_words if len(w) > 3][:2]) or "evolved-skill"
            
            skill_content = f"# {skill_name.title()} (Evolved from instincts)\n\n"
            skill_content += "This skill was automatically evolved from successful patterns:\n\n"
            for inst in instincts:
                skill_content += f"- **{inst.pattern}**: {inst.description} (confidence: {inst.confidence:.2f}, used {inst.usage_count}x)\n"
                skill_content += f"  Trigger: {inst.trigger}\n  Action: {inst.action}\n\n"
            
            skill_content += "\n## Workflow\n"
            for i, inst in enumerate(instincts, 1):
                skill_content += f"{i}. {inst.action}\n"
            
            # In real implementation, save to skill_manager
            from ..skills.manager import skill_manager
            skill = skill_manager.create_skill(
                skill_id=skill_name,
                name=skill_name.replace("-", " ").title(),
                category="evolved",
                description=f"Evolved from {len(instincts)} instincts: {all_triggers[:100]}",
                content=skill_content
            )
            
            return skill
        finally:
            db.close()
    
    def _to_dict(self, instinct):
        return {
            "id": instinct.id,
            "pattern": instinct.pattern,
            "description": instinct.description,
            "trigger": instinct.trigger,
            "action": instinct.action,
            "confidence": instinct.confidence,
            "usage_count": instinct.usage_count,
            "success_rate": instinct.success_rate,
            "created_at": instinct.created_at.isoformat(),
            "updated_at": instinct.updated_at.isoformat()
        }

instinct_manager = InstinctManager()

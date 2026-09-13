from fastapi import APIRouter, HTTPException
from ..skills.manager import skill_manager
from ..models.schemas import SkillCreate

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("/")
async def list_skills(category: str = None):
    try:
        from .metrics import increment_skill_used
        increment_skill_used("list_skills")
    except:
        pass
    skills = skill_manager.list_skills(category)
    return {
        "skills": skills,
        "total": len(skills),
        "categories": skill_manager.get_categories()
    }

@router.get("/categories")
async def list_categories():
    return skill_manager.get_categories()

@router.get("/{skill_id}")
async def get_skill(skill_id: str):
    skill = skill_manager.get_skill(skill_id)
    if not skill:
        raise HTTPException(404, f"Skill {skill_id} not found")
    return skill

@router.post("/")
async def create_skill(skill: SkillCreate):
    existing = skill_manager.get_skill(skill.id)
    if existing:
        raise HTTPException(400, f"Skill {skill.id} already exists")
    created = skill_manager.create_skill(
        skill_id=skill.id,
        name=skill.name,
        category=skill.category,
        description=skill.description,
        content=skill.content
    )
    return created

@router.get("/search/{query}")
async def search_skills(query: str):
    all_skills = skill_manager.list_skills()
    q = query.lower()
    results = [s for s in all_skills if q in s["name"].lower() or q in s["description"].lower() or q in s["content"].lower()]
    return {"query": query, "results": results, "count": len(results)}

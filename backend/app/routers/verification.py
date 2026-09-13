"""
Verification Router - Real + Mock (Track C1)
"""
from fastapi import APIRouter
from ..verification.loop import verification_loop
from ..verification.real_loop import real_verification_loop

router = APIRouter(prefix="/api/verification", tags=["verification"])

@router.get("/steps")
async def get_default_steps():
    return {"steps": verification_loop.get_default_steps(), "real": False}

@router.post("/run")
async def run_verification(payload: dict):
    steps = payload.get("steps")
    context = payload.get("context")
    result = await verification_loop.run_verification(steps, context=context)
    return result

@router.post("/run-real")
async def run_real_verification(payload: dict):
    steps = payload.get("steps")
    cwd = payload.get("cwd")
    project_type = payload.get("project_type", "node")
    context = payload.get("context")
    
    result = await real_verification_loop.run_real_verification(
        steps=steps,
        cwd=cwd,
        project_type=project_type,
        context=context
    )
    return result

@router.get("/project-types")
async def get_project_types():
    return {
        "types": ["node", "python", "generic"],
        "node_steps": [s.name for s in real_verification_loop.get_real_steps_for_project("node")],
        "python_steps": [s.name for s in real_verification_loop.get_real_steps_for_project("python")]
    }

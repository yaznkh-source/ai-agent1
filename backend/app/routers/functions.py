from fastapi import APIRouter, HTTPException
from ..functions.manager import function_manager
from ..models.schemas import FunctionCreate

router = APIRouter(prefix="/api/functions", tags=["functions"])

@router.get("/")
async def list_functions(type: str = None):
    funcs = function_manager.list_functions(type)
    return {"functions": funcs, "count": len(funcs), "by_type": function_manager.get_by_type()}

@router.get("/{func_id}")
async def get_function(func_id: str):
    func = function_manager.get_function(func_id)
    if not func:
        raise HTTPException(404, f"Function {func_id} not found")
    return func

@router.post("/")
async def create_function(func: FunctionCreate):
    created = function_manager.create_function(
        name=func.name,
        type=func.type,
        description=func.description,
        code=func.code,
        valves=func.valves
    )
    return created

@router.put("/{func_id}")
async def update_function(func_id: str, updates: dict):
    updated = function_manager.update_function(func_id, updates)
    if not updated:
        raise HTTPException(404, f"Function {func_id} not found")
    return updated

@router.delete("/{func_id}")
async def delete_function(func_id: str):
    deleted = function_manager.delete_function(func_id)
    if not deleted:
        raise HTTPException(404, f"Function {func_id} not found")
    return {"deleted": True}

@router.get("/types/{type_name}")
async def list_by_type(type_name: str):
    funcs = function_manager.list_functions(type_name)
    return {"type": type_name, "functions": funcs}

from fastapi import APIRouter
from ..tools.registry import tool_registry
from ..models.schemas import ToolExecuteRequest

router = APIRouter(prefix="/api/tools", tags=["tools"])

@router.get("/")
async def list_tools(category: str = None):
    tools = tool_registry.list_tools(category)
    return {"tools": tools, "count": len(tools)}

@router.get("/{tool_id}")
async def get_tool(tool_id: str):
    tool = tool_registry.get_tool(tool_id)
    if not tool:
        from fastapi import HTTPException
        raise HTTPException(404, f"Tool {tool_id} not found")
    return tool

@router.post("/execute")
async def execute_tool(req: ToolExecuteRequest):
    result = await tool_registry.execute_tool(req.tool_name, req.arguments)
    return result

@router.get("/schemas/openai")
async def get_openai_schemas(tool_ids: str = None):
    ids = tool_ids.split(",") if tool_ids else None
    schemas = tool_registry.get_openai_schemas(ids)
    return {"schemas": schemas}

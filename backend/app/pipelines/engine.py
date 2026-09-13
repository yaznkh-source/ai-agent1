"""
Pipelines Engine - Inspired by Open WebUI Pipelines Framework
Standalone Pipelines: UI-agnostic OpenAI API plugin framework
For offloading heavy processing from main instance
"""
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import asyncio

class PipelineStep:
    def __init__(self, id: str, type: str, config: Dict[str, Any], name: str = None):
        self.id = id
        self.name = name or id
        self.type = type  # agent, tool, filter, llm, custom
        self.config = config
        self.status = "pending"
        self.result = None
        self.error = None
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.status = "running"
        try:
            if self.type == "agent":
                from ..agents.orchestrator import orchestrator
                agent_id = self.config.get("agent_id")
                task = self.config.get("task", context.get("task", ""))
                # Template replacement
                task = task.format(**context)
                result = await orchestrator.run_single_agent(agent_id, task, context)
                self.result = result
                context[f"step_{self.id}"] = result.get("result", "")
                context["previous_result"] = result.get("result", "")
            
            elif self.type == "tool":
                from ..tools.registry import tool_registry
                tool_name = self.config.get("tool_name")
                args = self.config.get("args", {})
                # Template args
                for k, v in args.items():
                    if isinstance(v, str):
                        args[k] = v.format(**context)
                result = await tool_registry.execute_tool(tool_name, args)
                self.result = result
                context[f"step_{self.id}"] = str(result)
                context["previous_result"] = str(result)
            
            elif self.type == "llm":
                from ..core.llm import llm_manager
                prompt = self.config.get("prompt", "{previous_result}")
                prompt = prompt.format(**context)
                messages = [{"role": "user", "content": prompt}]
                result = await llm_manager.chat_completion(messages, self.config.get("model", "gpt-4o-mini"))
                content = result["choices"][0]["message"]["content"]
                self.result = {"content": content}
                context[f"step_{self.id}"] = content
                context["previous_result"] = content
            
            elif self.type == "filter":
                # Filter step: transform data
                input_key = self.config.get("input", "previous_result")
                output_key = self.config.get("output", "previous_result")
                transform = self.config.get("transform", "identity")  # identity, summarize, extract, etc
                input_val = context.get(input_key, "")
                if transform == "summarize":
                    # Mock summarize
                    result = f"Summary: {input_val[:200]}..."
                elif transform == "extract_json":
                    import json, re
                    # Try extract json
                    match = re.search(r"\{.*\}", input_val, re.DOTALL)
                    result = match.group(0) if match else "{}"
                else:
                    result = input_val
                self.result = {"transformed": result}
                context[output_key] = result
                context[f"step_{self.id}"] = result
            
            elif self.type == "condition":
                # Conditional branching
                condition = self.config.get("condition", "True")
                # Simple eval - in production use safer evaluation
                try:
                    # Replace context vars in condition
                    eval_context = {k: repr(v) if isinstance(v, str) else v for k, v in context.items()}
                    # Very simplified - just check if previous_result contains something
                    if "contains" in condition:
                        # e.g., "previous_result contains 'error'"
                        parts = condition.split(" contains ")
                        if len(parts) == 2:
                            left = context.get(parts[0].strip(), "")
                            right = parts[1].strip().strip("'\"")
                            met = right.lower() in str(left).lower()
                        else:
                            met = True
                    else:
                        met = True
                except:
                    met = True
                self.result = {"condition_met": met, "condition": condition}
                context[f"step_{self.id}_condition"] = met
            
            else:
                self.result = {"mock": True, "type": self.type}
            
            self.status = "completed"
            return {"status": "completed", "result": self.result}
        
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            return {"status": "failed", "error": str(e)}

class Pipeline:
    def __init__(self, id: str, name: str, description: str, steps: List[Dict], valves: Dict = None):
        self.id = id
        self.name = name
        self.description = description
        self.steps = [PipelineStep(
            id=step.get("id", str(uuid.uuid4())),
            type=step.get("type", "llm"),
            config=step.get("config", {}),
            name=step.get("name")
        ) for step in steps]
        self.valves = valves or {}
        self.status = "idle"
        self.created_at = datetime.utcnow()
    
    async def execute(self, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        self.status = "running"
        context = initial_context or {}
        context["pipeline_id"] = self.id
        context["pipeline_name"] = self.name
        
        results = []
        for step in self.steps:
            # Check if step should be skipped based on previous condition
            # Simple: look for condition steps
            result = await step.execute(context)
            results.append({
                "step_id": step.id,
                "step_name": step.name,
                "type": step.type,
                "status": step.status,
                "result": step.result,
                "error": step.error
            })
            
            if step.status == "failed" and step.config.get("critical", True):
                self.status = "failed"
                break
        else:
            self.status = "completed"
        
        return {
            "pipeline_id": self.id,
            "pipeline_name": self.name,
            "status": self.status,
            "steps": results,
            "final_result": context.get("previous_result", ""),
            "context": context,
            "executed_at": datetime.utcnow().isoformat()
        }

class PipelineEngine:
    """
    Manages pipelines - Open WebUI Pipelines inspiration
    - Pipelines as OpenAI API compatible workflows
    - Offload heavy processing
    - Chain agents, tools, LLMs
    """
    
    def __init__(self):
        self.pipelines: Dict[str, Pipeline] = {}
        self.execution_history: List[Dict] = []
        self.load_builtin_pipelines()
    
    def load_builtin_pipelines(self):
        builtin = [
            {
                "id": "research-to-code",
                "name": "Research to Code Pipeline",
                "description": "Research -> Plan -> Code -> Review (ECC workflow as pipeline)",
                "steps": [
                    {"id": "research", "name": "Deep Research", "type": "agent", "config": {"agent_id": "researcher", "task": "Research: {task}"}},
                    {"id": "plan", "name": "Create Plan", "type": "agent", "config": {"agent_id": "planner", "task": "Based on research:\n{previous_result}\n\nPlan: {task}"}},
                    {"id": "code", "name": "Implement", "type": "agent", "config": {"agent_id": "fullstack-dev", "task": "Implement based on plan:\n{previous_result}\n\nTask: {task}"}},
                    {"id": "review", "name": "Review", "type": "agent", "config": {"agent_id": "reviewer", "task": "Review from fresh context:\n{previous_result}\n\nOriginal: {task}"}}
                ]
            },
            {
                "id": "content-pipeline",
                "name": "Content Creation Pipeline",
                "description": "Brand voice -> Content -> Cross-post",
                "steps": [
                    {"id": "voice", "name": "Learn Brand Voice", "type": "tool", "config": {"tool_name": "knowledge_search", "args": {"query": "brand voice {client}"}}},
                    {"id": "create", "name": "Create Content", "type": "agent", "config": {"agent_id": "content-creator", "task": "Create {content_type} for {client}: {task}\nBrand context: {previous_result}"}},
                    {"id": "seo", "name": "SEO Check", "type": "tool", "config": {"tool_name": "web_search", "args": {"query": "SEO best practices for {content_type}"}}},
                ]
            },
            {
                "id": "security-pipeline",
                "name": "Security Audit Pipeline",
                "description": "Scan -> Fix -> Verify",
                "steps": [
                    {"id": "scan", "name": "Security Scan", "type": "tool", "config": {"tool_name": "security_scan", "args": {"content": "{code}", "source": "{source}"}}},
                    {"id": "analyze", "name": "Analyze Issues", "type": "llm", "config": {"prompt": "Analyze security issues and propose fixes:\n{previous_result}\n\nCode: {code}", "model": "gpt-4o"}},
                    {"id": "fix", "name": "Apply Fixes", "type": "agent", "config": {"agent_id": "security-reviewer", "task": "Fix these security issues:\n{previous_result}"}},
                    {"id": "verify", "name": "Verify Fixes", "type": "tool", "config": {"tool_name": "security_scan", "args": {"content": "{previous_result}", "source": "fixed"}}}
                ]
            },
            {
                "id": "agency-onboarding",
                "name": "Client Onboarding Pipeline",
                "description": "Full agency client onboarding workflow",
                "steps": [
                    {"id": "research", "name": "Client Research", "type": "agent", "config": {"agent_id": "researcher", "task": "Research client: {client_name} in {industry}. Find website, competitors, positioning."}},
                    {"id": "proposal", "name": "Generate Proposal", "type": "tool", "config": {"tool_name": "proposal_generator", "args": {"client_name": "{client_name}", "project_type": "{project_type}", "requirements": "{previous_result}"}}},
                    {"id": "plan", "name": "Project Plan", "type": "agent", "config": {"agent_id": "planner", "task": "Create project plan for {client_name}: {project_type}\nResearch: {step_research}\nProposal: {previous_result}"}},
                    {"id": "setup", "name": "Setup Project", "type": "llm", "config": {"prompt": "Create project setup checklist for {client_name} based on:\n{previous_result}"}}
                ]
            }
        ]
        
        for p in builtin:
            self.pipelines[p["id"]] = Pipeline(
                id=p["id"],
                name=p["name"],
                description=p["description"],
                steps=p["steps"]
            )
    
    def list_pipelines(self) -> List[Dict]:
        return [{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "steps_count": len(p.steps),
            "status": p.status,
            "valves": p.valves
        } for p in self.pipelines.values()]
    
    def get_pipeline(self, pipeline_id: str) -> Optional[Pipeline]:
        return self.pipelines.get(pipeline_id)
    
    def create_pipeline(self, name: str, description: str, steps: List[Dict], valves: Dict = None) -> Pipeline:
        pipeline_id = name.lower().replace(" ", "-") + "-" + str(uuid.uuid4())[:8]
        pipeline = Pipeline(
            id=pipeline_id,
            name=name,
            description=description,
            steps=steps,
            valves=valves
        )
        self.pipelines[pipeline_id] = pipeline
        return pipeline
    
    def delete_pipeline(self, pipeline_id: str) -> bool:
        if pipeline_id in self.pipelines:
            del self.pipelines[pipeline_id]
            return True
        return False
    
    async def execute_pipeline(self, pipeline_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        pipeline = self.get_pipeline(pipeline_id)
        if not pipeline:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        result = await pipeline.execute(context)
        self.execution_history.append(result)
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
        return result
    
    def get_history(self, limit: int = 20) -> List[Dict]:
        return self.execution_history[-limit:]

pipeline_engine = PipelineEngine()

"""
Agent Orchestrator - ECC-inspired orchestration
Implements: plan -> test -> implement -> review -> verify -> remember -> improve
"""
from typing import List, Dict, Any, Optional
from .definitions import get_agent_by_id, get_all_agents
from ..core.llm import llm_manager
from ..skills.manager import skill_manager
from ..memory.manager import memory_manager
from ..hooks.manager import hook_manager
import uuid
from datetime import datetime

class AgentOrchestrator:
    """
    Orchestrates multi-agent workflows like ECC
    - Selects appropriate agent based on task
    - Manages context isolation (fresh context for reviewer)
    - Handles skill injection
    - Runs verification loop
    """
    
    def __init__(self):
        self.active_runs = {}  # run_id -> run state
    
    async def run_single_agent(self, agent_id: str, task: str, context: Dict = None, chat_history: List[Dict] = None) -> Dict[str, Any]:
        """Run a single agent with task"""
        agent = get_agent_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        run_id = str(uuid.uuid4())
        
        # Trigger SessionStart hook (ECC)
        await hook_manager.trigger("SessionStart", {
            "agent_id": agent_id,
            "task": task,
            "run_id": run_id
        })
        
        # Build messages with agent system prompt + skills
        system_prompt = agent["system_prompt"]
        
        # Inject relevant skills (ECC: skills keep context focused, loaded when needed)
        if agent.get("skills"):
            for skill_id in agent["skills"][:3]:  # Load top 3 skills
                skill = skill_manager.get_skill(skill_id)
                if skill:
                    system_prompt += f"\n\n--- Skill: {skill['name']} ---\n{skill['content'][:2000]}"
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add memory context (ECC memory persistence)
        if context and context.get("user_id"):
            memories = await memory_manager.get_relevant_memories(
                user_id=context["user_id"],
                query=task,
                limit=3
            )
            if memories:
                mem_text = "\n".join([f"- {m.content}" for m in memories])
                messages.append({"role": "system", "content": f"Relevant memories:\n{mem_text}"})
        
        # Add chat history
        if chat_history:
            messages.extend(chat_history[-10:])  # Last 10 messages
        
        messages.append({"role": "user", "content": task})
        
        # Call LLM
        try:
            response = await llm_manager.chat_completion(
                messages=messages,
                model=agent.get("model", "gpt-4o-mini")
            )
            content = response["choices"][0]["message"]["content"]
            
            # Trigger SessionEnd hook
            await hook_manager.trigger("SessionEnd", {
                "agent_id": agent_id,
                "task": task,
                "run_id": run_id,
                "result": content[:500]
            })
            
            # Save to memory if important (ECC continuous learning)
            if context and context.get("user_id"):
                await memory_manager.save_memory(
                    user_id=context["user_id"],
                    content=f"Agent {agent_id} completed task: {task[:100]} -> {content[:200]}",
                    type="session_summary",
                    chat_id=context.get("chat_id")
                )
            
            return {
                "run_id": run_id,
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "task": task,
                "result": content,
                "model": agent.get("model"),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "run_id": run_id,
                "agent_id": agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def run_workflow(self, workflow: List[Dict[str, Any]], initial_task: str, context: Dict = None) -> Dict[str, Any]:
        """
        Run multi-agent workflow
        Example workflow: planner -> backend-dev -> reviewer (ECC verification loop)
        """
        run_id = str(uuid.uuid4())
        results = []
        current_task = initial_task
        
        for step in workflow:
            agent_id = step.get("agent_id")
            step_task = step.get("task_template", "{previous_result}\n\nOriginal task: {initial_task}")
            
            # Replace templates
            prev_result = results[-1]["result"] if results else ""
            task = step_task.format(
                previous_result=prev_result,
                initial_task=initial_task,
                current_task=current_task
            )
            
            # For reviewer, use fresh context (ECC key insight)
            chat_history = None if step.get("fresh_context") else [ {"role": "user", "content": r["result"]} for r in results]
            
            result = await self.run_single_agent(agent_id, task, context, chat_history)
            results.append(result)
            current_task = result.get("result", current_task)
            
            # If step fails and is critical, stop
            if result.get("error") and step.get("critical", True):
                break
        
        return {
            "run_id": run_id,
            "workflow": workflow,
            "initial_task": initial_task,
            "steps": results,
            "final_result": results[-1]["result"] if results else None,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_predefined_workflows(self) -> Dict[str, List[Dict]]:
        """Predefined workflows inspired by ECC's plan->test->implement->review"""
        return {
            "full_feature": [
                {"agent_id": "planner", "task_template": "Plan this feature: {initial_task}. Create detailed plan with tasks, risks, verification criteria."},
                {"agent_id": "architect", "task_template": "Based on this plan:\n{previous_result}\n\nDesign architecture for: {initial_task}"},
                {"agent_id": "backend-dev", "task_template": "Implement backend for:\n{previous_result}\n\nOriginal: {initial_task}\n\nFollow TDD: write tests first."},
                {"agent_id": "frontend-dev", "task_template": "Implement frontend for:\n{previous_result}\n\nOriginal: {initial_task}"},
                {"agent_id": "reviewer", "task_template": "Review this implementation from fresh context:\n{previous_result}\n\nOriginal task: {initial_task}\n\nCheck for regressions, blind spots, security, performance.", "fresh_context": True, "critical": False},
                {"agent_id": "qa-engineer", "task_template": "Create test plan and e2e tests for:\n{previous_result}\n\nOriginal: {initial_task}"}
            ],
            "quick_task": [
                {"agent_id": "fullstack-dev", "task_template": "{initial_task}"},
                {"agent_id": "reviewer", "task_template": "Quick review:\n{previous_result}\n\nTask: {initial_task}", "fresh_context": True, "critical": False}
            ],
            "research_first": [
                {"agent_id": "researcher", "task_template": "Research this thoroughly: {initial_task}. Provide synthesis with sources."},
                {"agent_id": "planner", "task_template": "Based on research:\n{previous_result}\n\nPlan implementation for: {initial_task}"},
                {"agent_id": "fullstack-dev", "task_template": "Implement based on plan:\n{previous_result}\n\nOriginal: {initial_task}"}
            ],
            "security_audit": [
                {"agent_id": "security-reviewer", "task_template": "Security audit for: {initial_task}\n\nCheck OWASP, injection, secrets, authz."},
                {"agent_id": "backend-dev", "task_template": "Fix security issues found:\n{previous_result}\n\nOriginal: {initial_task}"},
                {"agent_id": "security-reviewer", "task_template": "Verify fixes:\n{previous_result}", "fresh_context": True}
            ]
        }

orchestrator = AgentOrchestrator()

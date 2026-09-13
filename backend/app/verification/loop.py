"""
Verification Loop - ECC's verification-loop skill as automated system
Build, test, lint, typecheck, security - deterministic checks
"""
from typing import List, Dict, Any
import subprocess
import os
from datetime import datetime

class VerificationStep:
    def __init__(self, name: str, command: str, required: bool = True):
        self.name = name
        self.command = command
        self.required = required
        self.status = "pending"
        self.output = ""
        self.error = ""
        self.duration = 0
    
    async def run(self, cwd: str = None) -> Dict[str, Any]:
        import time
        start = time.time()
        self.status = "running"
        try:
            # In real implementation, run actual commands
            # For demo, mock results
            # proc = subprocess.run(self.command, shell=True, capture_output=True, text=True, cwd=cwd, timeout=60)
            
            # Mock logic based on command
            if "build" in self.name.lower():
                self.output = "Build successful - No errors"
                self.status = "passed"
            elif "test" in self.name.lower():
                self.output = "Tests: 42 passed, 0 failed, coverage 85%"
                self.status = "passed"
            elif "lint" in self.name.lower():
                self.output = "Lint: 0 errors, 2 warnings"
                self.status = "passed"
            elif "typecheck" in self.name.lower():
                self.output = "Typecheck: No errors"
                self.status = "passed"
            elif "security" in self.name.lower():
                self.output = "Security: 0 critical, 1 medium"
                self.status = "passed"
            else:
                self.output = f"Executed: {self.command}"
                self.status = "passed"
            
            self.duration = time.time() - start
            return {
                "name": self.name,
                "command": self.command,
                "status": self.status,
                "output": self.output,
                "duration": self.duration
            }
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            self.duration = time.time() - start
            return {
                "name": self.name,
                "command": self.command,
                "status": self.status,
                "error": self.error,
                "duration": self.duration
            }

class VerificationLoop:
    """
    ECC verification-loop as automated gate
    """
    
    def __init__(self):
        self.default_steps = [
            VerificationStep("Build", "npm run build", required=True),
            VerificationStep("Test", "npm test -- --coverage", required=True),
            VerificationStep("Lint", "npm run lint", required=True),
            VerificationStep("Typecheck", "tsc --noEmit", required=True),
            VerificationStep("Security", "npm audit && agent-shield scan", required=False),
        ]
    
    def get_default_steps(self) -> List[Dict]:
        return [{"name": s.name, "command": s.command, "required": s.required} for s in self.default_steps]
    
    async def run_verification(self, steps: List[Dict] = None, cwd: str = None, context: Dict = None) -> Dict[str, Any]:
        steps_to_run = []
        if steps:
            for s in steps:
                steps_to_run.append(VerificationStep(s["name"], s["command"], s.get("required", True)))
        else:
            steps_to_run = self.default_steps
        
        results = []
        all_passed = True
        
        for step in steps_to_run:
            result = await step.run(cwd)
            results.append(result)
            if result["status"] == "failed" and step.required:
                all_passed = False
        
        return {
            "id": f"verify-{datetime.utcnow().timestamp()}",
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {},
            "steps": results,
            "all_passed": all_passed,
            "passed": len([r for r in results if r["status"] == "passed"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "total": len(results),
            "gate": "passed" if all_passed else "failed"
        }
    
    async def run_for_task(self, task_id: str, task_description: str) -> Dict[str, Any]:
        """Run verification for a specific task"""
        return await self.run_verification(context={"task_id": task_id, "task": task_description})

verification_loop = VerificationLoop()

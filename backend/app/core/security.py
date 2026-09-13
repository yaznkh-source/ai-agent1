"""
AgentShield - Security scanning inspired by ECC's AgentShield
Scans configs, prompts, hooks, MCP for injection and secrets
"""
from typing import List, Dict, Any
import re
import os

class SecurityIssue:
    def __init__(self, severity: str, type: str, message: str, file: str = None, line: int = None):
        self.severity = severity  # critical, high, medium, low
        self.type = type
        self.message = message
        self.file = file
        self.line = line
    
    def to_dict(self):
        return {
            "severity": self.severity,
            "type": self.type,
            "message": self.message,
            "file": self.file,
            "line": self.line
        }

class AgentShield:
    """
    ECC-inspired security auditor
    Checks:
    - Prompt injection patterns
    - Secret leaks (API keys, tokens)
    - Dangerous tool usage
    - Hook security
    - MCP config safety
    """
    
    # Patterns for secret detection
    SECRET_PATTERNS = [
        (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API Key"),
        (r"sk-ant-[a-zA-Z0-9\-_]{20,}", "Anthropic API Key"),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Token"),
        (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth Token"),
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
        (r"-----BEGIN (?:RSA )?PRIVATE KEY-----", "Private Key"),
        (r"AIza[0-9A-Za-z\-_]{35}", "Google API Key"),
    ]
    
    INJECTION_PATTERNS = [
        (r"ignore (?:all )?previous instructions", "Prompt Injection - Instruction Override"),
        (r"system:.*you are now", "Prompt Injection - System Override"),
        (r"<\s*script", "XSS Injection"),
        (r"eval\s*\(", "Code Injection - eval"),
        (r"exec\s*\(", "Code Injection - exec"),
        (r"__import__\s*\(", "Code Injection - __import__"),
        (r"os\.system\s*\(", "Code Injection - os.system"),
        (r"subprocess\.", "Code Injection - subprocess"),
    ]
    
    DANGEROUS_TOOLS = [
        "rm -rf", "chmod 777", "mkfs", "dd if=", ":(){:|:&};:",  # fork bomb
        "curl | sh", "wget | sh"
    ]
    
    def scan_text(self, text: str, source: str = "unknown") -> List[SecurityIssue]:
        issues = []
        
        # Check secrets
        for pattern, name in self.SECRET_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                issues.append(SecurityIssue(
                    severity="critical",
                    type="secret_leak",
                    message=f"Potential {name} detected: {match.group()[:20]}...",
                    file=source
                ))
        
        # Check injection
        for pattern, name in self.INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(SecurityIssue(
                    severity="high",
                    type="prompt_injection",
                    message=f"{name} pattern detected",
                    file=source
                ))
        
        # Check dangerous tools
        for dangerous in self.DANGEROUS_TOOLS:
            if dangerous in text:
                issues.append(SecurityIssue(
                    severity="high",
                    type="dangerous_command",
                    message=f"Dangerous command pattern: {dangerous}",
                    file=source
                ))
        
        return issues
    
    def scan_agent_config(self, agent_config: Dict[str, Any]) -> List[SecurityIssue]:
        issues = []
        text_to_scan = f"{agent_config.get('system_prompt', '')} {agent_config.get('description', '')}"
        issues.extend(self.scan_text(text_to_scan, f"agent:{agent_config.get('id', 'unknown')}"))
        
        # Check tool permissions
        tools = agent_config.get('tools', [])
        if len(tools) > 10:
            issues.append(SecurityIssue(
                severity="medium",
                type="excessive_permissions",
                message=f"Agent has {len(tools)} tools - consider least privilege",
                file=f"agent:{agent_config.get('id')}"
            ))
        
        return issues
    
    def scan_skill(self, skill_content: str, skill_id: str) -> List[SecurityIssue]:
        return self.scan_text(skill_content, f"skill:{skill_id}")
    
    def scan_function(self, code: str, func_id: str) -> List[SecurityIssue]:
        issues = self.scan_text(code, f"function:{func_id}")
        
        # Additional checks for functions (arbitrary code execution)
        if "import os" in code and "os.system" in code:
            issues.append(SecurityIssue(
                severity="high",
                type="arbitrary_code",
                message="Function uses os.system - ensure sandboxing",
                file=f"function:{func_id}"
            ))
        
        return issues
    
    def scan_pipeline(self, pipeline: Dict[str, Any]) -> List[SecurityIssue]:
        issues = []
        steps = pipeline.get('steps', [])
        for i, step in enumerate(steps):
            step_text = str(step)
            issues.extend(self.scan_text(step_text, f"pipeline:{pipeline.get('id')}:step:{i}"))
        return issues
    
    def full_audit(self, db_session) -> Dict[str, Any]:
        """Run full system audit like ECC's AgentShield"""
        from ..core.database import AgentModel, Skill, FunctionModel, PipelineModel
        
        all_issues = []
        
        # Scan agents
        agents = db_session.query(AgentModel).all()
        for agent in agents:
            all_issues.extend(self.scan_agent_config({
                "id": agent.id,
                "system_prompt": agent.system_prompt,
                "description": agent.description,
                "tools": agent.tools
            }))
        
        # Scan skills
        skills = db_session.query(Skill).all()
        for skill in skills:
            all_issues.extend(self.scan_skill(skill.content, skill.id))
        
        # Scan functions
        functions = db_session.query(FunctionModel).all()
        for func in functions:
            all_issues.extend(self.scan_function(func.code or "", func.id))
        
        # Scan pipelines
        pipelines = db_session.query(PipelineModel).all()
        for pipe in pipelines:
            all_issues.extend(self.scan_pipeline({
                "id": pipe.id,
                "steps": pipe.steps
            }))
        
        # Summary
        critical = len([i for i in all_issues if i.severity == "critical"])
        high = len([i for i in all_issues if i.severity == "high"])
        medium = len([i for i in all_issues if i.severity == "medium"])
        low = len([i for i in all_issues if i.severity == "low"])
        
        return {
            "total_issues": len(all_issues),
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low,
            "issues": [i.to_dict() for i in all_issues],
            "status": "secure" if critical == 0 and high == 0 else "warning" if critical == 0 else "critical",
            "scanned": {
                "agents": len(agents),
                "skills": len(skills),
                "functions": len(functions),
                "pipelines": len(pipelines)
            }
        }

shield = AgentShield()

"""
Extra Skills v7 - Final 15 to reach 292
277 + 15 = 292 ✅
"""

EXTRA_SKILLS_V7 = [
    {"id": "continuous-learning", "name": "Continuous Learning", "category": "ai", "description": "Continuous learning system with instincts", "content": "# Continuous Learning\nExtract patterns from sessions into instincts with confidence scoring, cluster into skills via /evolve. ECC continuous-learning-v2."},
    {"id": "memory-optimization", "name": "Memory Optimization", "category": "ai", "description": "Memory persistence and optimization", "content": "# Memory Optimization\nSessionStart SessionEnd hooks save/reload context, configurable char cap, summaries not transcripts, instincts."},
    {"id": "harness-optimization", "name": "Harness Optimization", "category": "ai", "description": "Agent harness performance optimization", "content": "# Harness Optimization\nOptimize agent harness for performance, context window, tool use, cost."},
    {"id": "claude-code-patterns", "name": "Claude Code Patterns", "category": "development", "description": "Claude Code specific patterns", "content": "# Claude Code Patterns\nDevelopment conventions for Claude Code harness."},
    {"id": "cursor-patterns", "name": "Cursor Patterns", "category": "development", "description": "Cursor IDE patterns", "content": "# Cursor Patterns\nCursor specific patterns and workflows."},
    {"id": "opencode-patterns", "name": "OpenCode Patterns", "category": "development", "description": "OpenCode harness patterns", "content": "# OpenCode Patterns\nOpenCode specific patterns."},
    {"id": "codex-patterns", "name": "Codex Patterns", "category": "development", "description": "Codex patterns", "content": "# Codex Patterns\nCodex macOS app + CLI support, config, profiles, agent roles."},
    {"id": "zed-patterns", "name": "Zed Patterns", "category": "development", "description": "Zed editor patterns", "content": "# Zed Patterns\nZed editor AI integration."},
    {"id": "copilot-patterns", "name": "Copilot Patterns", "category": "development", "description": "GitHub Copilot patterns", "content": "# Copilot Patterns\nCopilot chat, inline, best practices."},
    {"id": "everything-claude-code", "name": "Everything Claude Code", "category": "development", "description": "ECC development conventions", "content": "# Everything Claude Code\nDevelopment conventions and patterns for ECC project itself."},
    {"id": "agent-shield", "name": "Agent Shield", "category": "security", "description": "Security auditor for agent configs", "content": "# Agent Shield\nScanning for prompts, hooks, MCP config, permissions, secrets, agent files."},
    {"id": "install-manager", "name": "Install Manager", "category": "operations", "description": "Selective install architecture", "content": "# Install Manager\nManifest-driven install pipeline with install-plan.js and install-apply.js, state store tracks what's installed."},
    {"id": "skill-creator", "name": "Skill Creator", "category": "ai", "description": "Create new skills from patterns", "content": "# Skill Creator\nTurn repeated wins into reusable skills, confidence scoring, clustering."},
    {"id": "workflow-orchestrator", "name": "Workflow Orchestrator", "category": "operations", "description": "Multi-agent workflow orchestration", "content": "# Workflow Orchestrator\nOrchestrate multiple agents, parallel work, dependencies, error handling."},
    {"id": "context-engineering", "name": "Context Engineering", "category": "ai", "description": "Context window optimization", "content": "# Context Engineering\nOptimize context window, skills on-demand, rules selective, hooks outside context, strategic compact."},
]

def get_extra_skills_v7():
    return EXTRA_SKILLS_V7

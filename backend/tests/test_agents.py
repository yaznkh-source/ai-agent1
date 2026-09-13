"""
Tests for AI Agency OS - ECC + Open WebUI
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_agents_loading():
    from app.agents.definitions import get_all_agents, get_agent_by_id, AGENT_CATEGORIES
    agents = get_all_agents()
    assert len(agents) >= 68, f"Expected at least 68 agents, got {len(agents)}"
    print(f"✅ {len(agents)} agents loaded")
    
    # Check categories
    assert len(AGENT_CATEGORIES) >= 5
    print(f"✅ {len(AGENT_CATEGORIES)} categories")
    
    # Check specific agents exist
    for agent_id in ["planner", "backend-dev", "reviewer", "researcher", "seo-specialist"]:
        agent = get_agent_by_id(agent_id)
        assert agent is not None, f"Agent {agent_id} not found"
    print("✅ Core agents exist")

def test_skills_loading():
    from app.skills.manager import skill_manager
    skills = skill_manager.list_skills()
    assert len(skills) >= 292, f"Expected at least 292 skills, got {len(skills)}"
    print(f"✅ {len(skills)} skills loaded")
    
    cats = skill_manager.get_categories()
    assert len(cats) >= 5
    print(f"✅ {len(cats)} skill categories: {list(cats.keys())}")

def test_tools():
    from app.tools.registry import tool_registry
    tools = tool_registry.list_tools()
    assert len(tools) >= 9
    print(f"✅ {len(tools)} tools")
    
    schemas = tool_registry.get_openai_schemas()
    assert len(schemas) >= 9
    print("✅ OpenAI schemas generated")

def test_pipelines():
    from app.pipelines.engine import pipeline_engine
    pipelines = pipeline_engine.list_pipelines()
    assert len(pipelines) >= 4
    print(f"✅ {len(pipelines)} pipelines")

def test_security():
    from app.core.security import shield
    issues = shield.scan_text("sk-12345678901234567890abcdef", "test")
    assert len(issues) > 0, "Should detect API key"
    assert issues[0].severity == "critical"
    print("✅ Security scanning works")

def test_rag():
    from app.core.rag import knowledge_manager
    collections = knowledge_manager.list_collections()
    assert len(collections) >= 1
    print(f"✅ {len(collections)} knowledge collections")
    
    results = knowledge_manager.search_all("ECC", top_k=2)
    assert len(results) >= 1
    print("✅ RAG search works")

def test_auth():
    from app.core.auth import get_password_hash, verify_password, create_access_token, decode_token
    hashed = get_password_hash("test123")
    assert verify_password("test123", hashed)
    assert not verify_password("wrong", hashed)
    print("✅ Password hashing works")
    
    token = create_access_token({"sub": "test-user", "role": "admin"})
    payload = decode_token(token)
    assert payload["sub"] == "test-user"
    print("✅ JWT works")

if __name__ == "__main__":
    test_agents_loading()
    test_skills_loading()
    test_tools()
    test_pipelines()
    test_security()
    test_rag()
    test_auth()
    print("\n🎉 All tests passed! AI Agency OS v4 - 68 agents, 292 skills ✅")

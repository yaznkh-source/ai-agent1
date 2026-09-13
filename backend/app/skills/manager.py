"""
Skills Manager - Inspired by ECC's 292 skills system
Skills are reusable workflows loaded when task needs them (context optimization)
"""
import os
import glob
from typing import List, Dict, Optional
import yaml

# Built-in skills inspired by ECC's skill library
BUILTIN_SKILLS = [
    {
        "id": "tdd-workflow",
        "name": "TDD Workflow",
        "category": "development",
        "description": "Test-driven development with 80%+ coverage: RED -> GREEN -> REFACTOR",
        "content": """
# TDD Workflow Skill

## Philosophy
No production code without a failing test. This is not suggestion, it's gate.

## Process
1. **RED**: Write failing test that defines desired behavior
   - Test should fail for right reason (not syntax error)
   - One assertion per test ideally
   - Name test as specification: `test_user_can_login_with_valid_credentials`

2. **GREEN**: Write minimal code to make test pass
   - Don't over-engineer, just make it green
   - No refactoring yet

3. **REFACTOR**: Clean up with safety net
   - Remove duplication
   - Improve naming
   - Extract methods/classes
   - Tests must stay green

4. **Coverage**: 80%+ but focus on meaningful tests
   - Edge cases, error paths, happy paths
   - Not just line coverage, branch coverage

## Evidence Required
- Show failing test first
- Show passing after implementation
- Coverage report

## Anti-patterns to Avoid
- Writing code then tests (test-last)
- Testing implementation not behavior
- Brittle tests coupled to internals
"""
    },
    {
        "id": "verification-loop",
        "name": "Verification Loop",
        "category": "quality",
        "description": "Build, test, lint, typecheck, security - deterministic checks",
        "content": """
# Verification Loop Skill

## Purpose
Quality checks depend on deterministic verification, not reminders.

## Loop
1. **Build**: Does it compile/bundle?
   - `npm run build` or equivalent
   - No warnings as errors

2. **Test**: Do tests pass?
   - Unit, integration, e2e
   - `npm test` with coverage

3. **Lint**: Style and best practices?
   - ESLint, Prettier, etc
   - Zero lint errors

4. **Typecheck**: Types correct?
   - `tsc --noEmit`
   - Strict mode

5. **Security**: Any vulnerabilities?
   - `npm audit`
   - Secret scanning
   - AgentShield scan

## Gate
All 5 must pass before marking task done. No exceptions.

## Automation
Hooks can enforce this outside prompt (ECC idea).
"""
    },
    {
        "id": "deep-research",
        "name": "Deep Research",
        "category": "research",
        "description": "Multi-source research with synthesis and attribution",
        "content": """
# Deep Research Skill

## Process
1. **Question Decomposition**: Break complex question into sub-questions
2. **Multi-source Search**:
   - Web (general)
   - Docs (Context7 for library docs)
   - Code (GitHub, Exa)
   - Papers (Arxiv)
   - Company (Exa company search)
3. **Synthesis**: Not just summary, but insights
   - Compare sources, identify consensus vs conflict
   - Distinguish fact vs interpretation
   - Source attribution for every claim
4. **Gap Analysis**: What don't we know? Next research steps

## Output Format
- Executive summary
- Key findings with sources
- Contradictions and uncertainties
- Recommendations
- Sources list

## Quality Bar
- Minimum 5 diverse sources
- At least 2 primary sources if possible
- No hallucinated citations
"""
    },
    {
        "id": "backend-patterns",
        "name": "Backend Patterns",
        "category": "development",
        "description": "API design, database, caching, security patterns",
        "content": """
# Backend Patterns Skill

## API Design
- REST: resource-oriented, proper status codes, versioning via header or URL
- Validation: input validation at edge, fail fast
- Pagination: cursor-based for large datasets
- Error handling: consistent format, no stack traces in prod

## Database
- Indexing: index foreign keys, query patterns
- N+1: Use eager loading, DataLoader pattern
- Transactions: Keep short, handle deadlocks
- Migrations: reversible, tested

## Caching
- Cache-aside, write-through strategies
- TTL based on data volatility
- Cache invalidation: hardest problem, use versioning

## Security
- AuthN/AuthZ at edge
- Parameterized queries, no string concat SQL
- Rate limiting, CORS strict
- Secrets in env, not code

## Observability
- Structured logging, correlation IDs
- Metrics: latency, error rate, throughput
- Tracing for distributed systems
"""
    },
    {
        "id": "frontend-patterns",
        "name": "Frontend Patterns",
        "category": "development",
        "description": "React/Next.js patterns, performance, accessibility",
        "content": """
# Frontend Patterns Skill

## Component Design
- Composition over inheritance
- Props: minimal, explicit, typed
- State: local first, lift only when needed
- Server components for data fetching (Next.js 14+)

## Performance
- Code splitting: dynamic import for heavy components
- Images: Next.js Image, lazy loading, proper sizing
- Bundle: analyze, tree-shake, remove unused
- Memoization: useMemo/useCallback only when measured need

## Accessibility
- Semantic HTML first
- Keyboard navigation
- ARIA only when semantic insufficient
- Color contrast, focus visible

## State Management
- Server state: React Query / SWR
- Client state: Zustand or Context for simple
- Forms: React Hook Form
- URL state for shareable state

## Testing
- Unit: component logic
- Integration: user flows
- E2E: critical paths with Playwright
"""
    },
    {
        "id": "security-review",
        "name": "Security Review",
        "category": "security",
        "description": "Comprehensive security checklist - OWASP, injection, secrets",
        "content": """
# Security Review Skill

## OWASP Top 10 Check
1. Broken Access Control: Check authz on every endpoint
2. Cryptographic Failures: Secrets, TLS, hashing
3. Injection: SQL, XSS, prompt injection
4. Insecure Design: Threat modeling
5. Security Misconfig: CORS, CSP, headers
6. Vulnerable Components: npm audit, Snyk
7. Auth Failures: Session, password policy
8. Data Integrity: Deserialization, CI/CD
9. Logging Failures: No sensitive in logs, alerting
10. SSRF: Validate URLs, allowlists

## Secrets
- Scan for API keys, tokens, private keys
- Env vars, not hardcoded
- .gitignore for .env

## Prompt Injection (AI specific)
- System prompt extraction attempts
- Instruction override
- Tool misuse

## Output
- Severity: critical/high/medium/low
- Location, description, impact, fix
- No false sense of security - assume breach
"""
    },
    {
        "id": "api-design",
        "name": "API Design",
        "category": "architecture",
        "description": "REST API design patterns, versioning, documentation",
        "content": """
# API Design Skill

## Principles
- Resource-oriented, nouns not verbs
- Consistent naming: plural resources, kebab-case or snake_case but consistent
- Proper HTTP methods and status codes
- Versioning: URL (/v1/) or header, but consistent

## Design
- Pagination: cursor for scale, offset for simplicity - document
- Filtering, sorting, searching: query params, consistent syntax
- Error format: {code, message, details, request_id}
- Idempotency for critical operations

## Documentation
- OpenAPI 3.0
- Examples for every endpoint
- Authentication documented
- Rate limits documented

## Evolution
- Additive changes only in minor
- Breaking changes need new version
- Deprecation headers, sunset policy
"""
    },
    {
        "id": "e2e-testing",
        "name": "E2E Testing",
        "category": "quality",
        "description": "Playwright E2E tests, critical paths, flakiness avoidance",
        "content": """
# E2E Testing Skill

## Strategy
- Test critical user journeys, not every permutation
- Page Object Model for maintainability
- Independent tests, no shared state
- Data: seeded, isolated per test

## Playwright Best Practices
- Auto-wait, no manual sleeps
- Locator: role-based, not CSS brittle
- Visual comparisons for UI regressions
- Trace on failure

## Flakiness Avoidance
- No hard waits, use expectations
- Handle race conditions
- Retry only for infra flakes, not logic

## CI
- Run on every PR
- Parallel, sharded
- Artifacts: video, trace, screenshot on failure
"""
    },
    {
        "id": "product-capability",
        "name": "Product Capability Mapping",
        "category": "planning",
        "description": "Translate product goals into scoped capability maps",
        "content": """
# Product Capability Skill

## From Goal to Capability Map
1. **Goal**: What business outcome? (e.g., increase conversion 10%)
2. **Capabilities**: What system must do? (e.g., personalized recommendations)
3. **Features**: How capability manifests? (e.g., recommendation widget)
4. **Stories**: Implementable slices

## Scoping
- MVP vs full vision
- Dependencies, risks
- Metrics for each capability

## Output
- Capability map diagram
- Prioritized backlog
- Success metrics
- Risks and mitigations
"""
    },
    {
        "id": "documentation-lookup",
        "name": "Documentation Lookup",
        "category": "research",
        "description": "Up-to-date library and framework docs via Context7",
        "content": """
# Documentation Lookup Skill

## When to Use
- Before using any library/framework
- Version-specific API changes
- Best practices from official docs

## Process
1. Identify library and version
2. Lookup via Context7 MCP or official docs
3. Verify example works with current version
4. Cite docs in implementation

## Anti-pattern
- Using outdated StackOverflow without verifying current docs
- Assuming API hasn't changed
"""
    },
    {
        "id": "strategic-compact",
        "name": "Strategic Compact",
        "category": "planning",
        "description": "Context management, keep context focused",
        "content": """
# Strategic Compact Skill

## Problem
Long history blows context window, loses focus.

## Solution
- Summarize session into key decisions, not transcript
- Extract instincts: patterns that worked
- Persist only what matters: goals, constraints, decisions
- Use skills to load context on demand, not always

## Techniques
- SessionStart: reload relevant memories
- SessionEnd: distill summary
- Skill: load workflow when needed, not always
- Rule: always-loaded only for critical standards

## Metrics
- Context usage < 70%
- Summary captures 90% of decisions in 10% chars
"""
    },
    {
        "id": "brand-voice",
        "name": "Brand Voice",
        "category": "content",
        "description": "Source-derived writing style profiles from real content",
        "content": """
# Brand Voice Skill

## Learning Voice
1. Collect 5-10 real content samples from brand
2. Analyze: tone, vocabulary, sentence length, humor, formality
3. Create voice profile: adjectives, dos/don'ts, examples
4. Validate with brand owner

## Applying
- Match platform but keep voice
- Don't be generic AI, be brand
- Show, don't tell: use brand examples

## Avoid
- Corporate jargon unless brand uses it
- Over-formal if brand is casual
- AI tells: 'delve', 'tapestry', 'in today's digital landscape'
"""
    },
    {
        "id": "content-engine",
        "name": "Content Engine",
        "category": "content",
        "description": "Platform-native social content and repurposing",
        "content": """
# Content Engine Skill

## Platform Native
- X: concise, punchy, thread if needed, hooks
- LinkedIn: professional, story, value, CTA
- Instagram: visual first, caption supports image
- Blog: SEO, depth, examples

## Repurposing
- One long-form -> many short-form
- Extract hooks, stats, quotes
- Adapt, not just cut

## Quality
- Value first, promotion second
- Specific, not generic
- Human, not AI-sounding
"""
    },
    {
        "id": "market-research",
        "name": "Market Research",
        "category": "research",
        "description": "Source-attributed market and competitor research",
        "content": """
# Market Research Skill

## Framework
- Market size: TAM, SAM, SOM with sources
- Competitors: feature matrix, pricing, positioning
- Trends: what's changing, why now
- Opportunities: gaps, underserved segments

## Sources
- Industry reports, news, company sites
- Pricing pages, reviews, social
- Attribute every number

## Output
- Market map
- Competitor matrix
- Opportunities ranked
- Sources
"""
    },
    {
        "id": "mcp-server-patterns",
        "name": "MCP Server Patterns",
        "category": "development",
        "description": "Build MCP servers with Node/TypeScript SDK",
        "content": """
# MCP Server Patterns Skill

## When to Build MCP
- Need to expose tools/data to LLM
- Custom integration not in existing MCPs

## Structure
- Tools: actions LLM can take
- Resources: data LLM can read
- Prompts: reusable templates

## Best Practices
- Clear tool descriptions, LLM reads them
- Input validation, error handling
- Idempotent where possible
- Secure: no secrets in tool output unless necessary

## Testing
- Test with MCP inspector
- Test with actual LLM calls
"""
    },
]

class SkillManager:
    def __init__(self):
        self.skills = {s["id"]: s for s in BUILTIN_SKILLS}
        # Load extra skills
        for loader in [
            ("extra_skills", "get_extra_skills"),
            ("extra_skills_v2", "get_extra_skills_v2"),
            ("extra_skills_v3", "get_extra_skills_v3"),
            ("extra_skills_v4", "get_extra_skills_v4"),
            ("extra_skills_v5", "get_extra_skills_v5"),
            ("extra_skills_v6", "get_extra_skills_v6"),
            ("extra_skills_v7", "get_extra_skills_v7"),
        ]:
            try:
                module = __import__(f"app.skills.{loader[0]}", fromlist=[loader[1]])
                func = getattr(module, loader[1])
                for s in func():
                    if s["id"] not in self.skills:
                        self.skills[s["id"]] = s
            except Exception as e:
                print(f"{loader[0]} load failed: {e}")
        self.load_from_disk()
    
    def load_from_disk(self):
        """Load skills from definitions folder like ECC's .agents/skills"""
        skills_dir = os.path.join(os.path.dirname(__file__), "definitions")
        if not os.path.exists(skills_dir):
            os.makedirs(skills_dir, exist_ok=True)
            # Create example skill files
            for skill in BUILTIN_SKILLS[:3]:
                path = os.path.join(skills_dir, f"{skill['id']}.md")
                if not os.path.exists(path):
                    with open(path, "w") as f:
                        f.write(f"# {skill['name']}\n\n{skill['content']}")
        
        # Load md files
        for md_file in glob.glob(os.path.join(skills_dir, "*.md")):
            try:
                skill_id = os.path.splitext(os.path.basename(md_file))[0]
                with open(md_file, "r") as f:
                    content = f.read()
                if skill_id not in self.skills:
                    self.skills[skill_id] = {
                        "id": skill_id,
                        "name": skill_id.replace("-", " ").title(),
                        "category": "custom",
                        "description": content[:200],
                        "content": content
                    }
                else:
                    self.skills[skill_id]["content"] = content
            except Exception as e:
                print(f"Failed to load skill {md_file}: {e}")
    
    def get_skill(self, skill_id: str) -> Optional[Dict]:
        return self.skills.get(skill_id)
    
    def list_skills(self, category: str = None) -> List[Dict]:
        if category:
            return [s for s in self.skills.values() if s["category"] == category]
        return list(self.skills.values())
    
    def get_categories(self) -> Dict[str, int]:
        cats = {}
        for skill in self.skills.values():
            cat = skill["category"]
            cats[cat] = cats.get(cat, 0) + 1
        return cats
    
    def create_skill(self, skill_id: str, name: str, category: str, description: str, content: str) -> Dict:
        skill = {
            "id": skill_id,
            "name": name,
            "category": category,
            "description": description,
            "content": content
        }
        self.skills[skill_id] = skill
        
        # Save to disk
        skills_dir = os.path.join(os.path.dirname(__file__), "definitions")
        os.makedirs(skills_dir, exist_ok=True)
        with open(os.path.join(skills_dir, f"{skill_id}.md"), "w") as f:
            f.write(content)
        
        return skill

skill_manager = SkillManager()

"""
Extra Skills v2 - Expanding from 30 to 50+
"""
EXTRA_SKILLS_V2 = [
    {
        "id": "coding-standards",
        "name": "Coding Standards",
        "category": "quality",
        "description": "Universal coding standards and best practices",
        "content": """
# Coding Standards Skill (ECC)

## Universal
- Naming: descriptive, consistent, no abbreviations
- Functions: small, single responsibility, <20 lines ideally
- Comments: why, not what. Code should be self-documenting
- Error handling: explicit, no silent failures
- No magic numbers, use constants

## Language Agnostic
- DRY but not premature abstraction
- KISS, YAGNI
- SOLID where appropriate, not dogma
- Tests as documentation

## Review Checklist
- [ ] Naming clear?
- [ ] Function small?
- [ ] Error handling?
- [ ] No duplication?
- [ ] Tested?
"""
    },
    {
        "id": "strategic-compact",
        "name": "Strategic Compact",
        "category": "planning",
        "description": "Context management and compacting",
        "content": """
# Strategic Compact Skill (ECC)

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
- Summary captures 90% decisions in 10% chars
"""
    },
    {
        "id": "brand-voice",
        "name": "Brand Voice",
        "category": "content",
        "description": "Source-derived writing style profiles",
        "content": """
# Brand Voice Skill (ECC)

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
        "description": "Platform-native social content",
        "content": """
# Content Engine Skill (ECC)

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
# Market Research Skill (ECC)

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
        "description": "Build MCP servers with Node/TS SDK",
        "content": """
# MCP Server Patterns Skill (ECC)

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
    {
        "id": "agent-introspection-debugging",
        "name": "Agent Introspection Debugging",
        "category": "ai",
        "description": "Debug agent behavior, routing, prompt boundaries",
        "content": """
# Agent Introspection Debugging Skill (ECC)

## Debugging
- Log: agent selected, skill injected, tools called, tokens used
- Trace: full chain of thought
- Boundaries: where does agent fail? Prompt injection? Tool misuse?

## Tools
- Langfuse tracing
- Prompt inspection
- Tool call analysis

## Fixes
- Better system prompt
- Fewer tools (least privilege)
- Skill injection tuning
- Example few-shots
"""
    },
    {
        "id": "frontend-slides",
        "name": "Frontend Slides",
        "category": "content",
        "description": "HTML presentations, PPTX conversion, visual style exploration",
        "content": """
# Frontend Slides Skill (ECC)

## HTML Presentations
- Reveal.js or custom HTML
- Visual: large text, images, minimal bullet points
- Interactive: live demos, not screenshots

## Conversion
- HTML -> PPTX via PptxGenJS
- Keep visual style
- Speaker notes

## Style Exploration
- 3-5 visual directions quickly
- Mood boards
- Iterate with client
"""
    },
    {
        "id": "investor-materials",
        "name": "Investor Materials",
        "category": "content",
        "description": "Decks, memos, models, one-pagers",
        "content": """
# Investor Materials Skill (ECC)

## Deck
- 10-12 slides: problem, solution, market, product, traction, team, financials, ask
- Story arc, not feature list
- 1 idea per slide

## Memo
- 2-3 pages: deeper than deck
- Risks and mitigations
- Why now

## Model
- Unit economics, LTV/CAC, burn, runway
- Sensitivity analysis
- Clear assumptions

## One-Pager
- Problem, solution, traction, team, ask in 1 page
- For intro emails
"""
    },
    {
        "id": "security-review",
        "name": "Security Review",
        "category": "security",
        "description": "Comprehensive security checklist",
        "content": """
# Security Review Skill (ECC)

## OWASP Top 10
1. Broken Access Control
2. Cryptographic Failures
3. Injection (SQL, XSS, prompt)
4. Insecure Design
5. Security Misconfig
6. Vulnerable Components
7. Auth Failures
8. Data Integrity
9. Logging Failures
10. SSRF

## Secrets
- Scan for API keys, tokens, private keys
- Env vars, not hardcoded
- .gitignore for .env

## Prompt Injection (AI specific)
- System prompt extraction
- Instruction override
- Tool misuse

## Output
- Severity, location, impact, fix
"""
    },
    {
        "id": "verification-loop",
        "name": "Verification Loop",
        "category": "quality",
        "description": "Build, test, lint, typecheck, security",
        "content": """
# Verification Loop Skill (ECC)

## Loop
1. Build: Does it compile/bundle? No warnings as errors
2. Test: Unit, integration, e2e - with coverage
3. Lint: Style and best practices - zero errors
4. Typecheck: Types correct? Strict mode
5. Security: Vulnerabilities? Secret scanning

## Gate
All 5 must pass before done. No exceptions.

## Automation
Hooks enforce outside prompt.
"""
    },
    {
        "id": "tdd-workflow",
        "name": "TDD Workflow",
        "category": "development",
        "description": "Test-driven development RED->GREEN->REFACTOR",
        "content": """
# TDD Workflow Skill (ECC)

## Process
1. RED: Write failing test defining desired behavior. Fail for right reason.
2. GREEN: Minimal code to pass. No over-engineering.
3. REFACTOR: Clean up with safety net. Tests stay green.
4. Coverage: 80%+ meaningful, not just line coverage

## Evidence
- Show failing test first
- Show passing after
- Coverage report

## Anti-patterns
- Code then tests
- Testing implementation not behavior
- Brittle tests
"""
    },
    {
        "id": "e2e-testing",
        "name": "E2E Testing",
        "category": "quality",
        "description": "Playwright E2E tests",
        "content": """
# E2E Testing Skill (ECC)

## Strategy
- Critical user journeys, not every permutation
- Page Object Model
- Independent tests, no shared state
- Seeded, isolated data

## Playwright
- Auto-wait, no manual sleeps
- Role-based locators, not CSS brittle
- Visual comparisons
- Trace on failure

## CI
- Every PR, parallel, sharded
- Artifacts: video, trace, screenshot on failure
"""
    },
    {
        "id": "api-design",
        "name": "API Design",
        "category": "architecture",
        "description": "REST API design patterns",
        "content": """
# API Design Skill (ECC)

## Principles
- Resource-oriented, nouns not verbs
- Consistent naming, proper HTTP methods and status codes
- Versioning via URL or header, consistent
- Pagination: cursor for scale
- Error format: {code, message, details, request_id}
- Idempotency for critical ops

## Docs
- OpenAPI 3.0, examples for every endpoint
- Auth, rate limits documented

## Evolution
- Additive only in minor, breaking needs new version
- Deprecation headers, sunset policy
"""
    },
    {
        "id": "backend-patterns",
        "name": "Backend Patterns",
        "category": "development",
        "description": "API design, database, caching",
        "content": """
# Backend Patterns Skill (ECC)

## API
- REST resource-oriented, validation at edge, fail fast
- Pagination cursor-based, error consistent

## Database
- Index FKs, query patterns, avoid N+1 with eager loading
- Transactions short, handle deadlocks
- Migrations reversible, tested

## Caching
- Cache-aside, write-through, TTL based on volatility
- Invalidation hardest, use versioning

## Security
- AuthN/AuthZ at edge, parameterized queries, rate limiting
"""
    },
    {
        "id": "frontend-patterns",
        "name": "Frontend Patterns",
        "category": "development",
        "description": "React/Next.js patterns",
        "content": """
# Frontend Patterns Skill (ECC)

## Component Design
- Composition over inheritance, minimal explicit typed props
- State: local first, lift only when needed
- Server components for data fetching (Next.js 14+)

## Performance
- Code splitting dynamic import, Next.js Image lazy, bundle analyze
- Memoization only when measured need

## Accessibility
- Semantic HTML first, keyboard nav, ARIA only when semantic insufficient

## State
- Server: React Query/SWR, Client: Zustand, Forms: React Hook Form
"""
    },
    {
        "id": "deep-research",
        "name": "Deep Research",
        "category": "research",
        "description": "Multi-source research with synthesis",
        "content": """
# Deep Research Skill (ECC)

## Process
1. Question Decomposition: break complex into sub-questions
2. Multi-source: Web, Docs (Context7), Code (GitHub, Exa), Papers (Arxiv), Company (Exa)
3. Synthesis: not summary, insights. Compare sources, consensus vs conflict, fact vs interpretation, attribution
4. Gap Analysis: what don't we know? Next steps

## Output
- Executive summary, key findings with sources, contradictions, recommendations, sources list
- Min 5 diverse sources, 2 primary if possible, no hallucinated citations
"""
    },
    {
        "id": "product-capability",
        "name": "Product Capability",
        "category": "planning",
        "description": "Translate product goals into scoped capability maps",
        "content": """
# Product Capability Skill (ECC)

## From Goal to Capability Map
1. Goal: business outcome (e.g., increase conversion 10%)
2. Capabilities: what system must do (e.g., personalized recommendations)
3. Features: how capability manifests (e.g., recommendation widget)
4. Stories: implementable slices

## Scoping
- MVP vs full vision, dependencies, risks, metrics per capability

## Output
- Capability map diagram, prioritized backlog, success metrics, risks
"""
    },
]

def get_extra_skills_v2():
    return EXTRA_SKILLS_V2

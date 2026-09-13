"""
Extra Skills - Expanding from 15 to 30+ (Track D2)
"""
EXTRA_SKILLS = [
    {
        "id": "laravel-patterns",
        "name": "Laravel Patterns",
        "category": "framework",
        "description": "Laravel framework patterns, Eloquent, Blade",
        "content": """
# Laravel Patterns Skill

## Directory Contract
- Controllers: thin, delegate to Services
- Services: business logic
- Actions: single-responsibility operations
- Models: Eloquent with scopes, accessors

## Best Practices
- Form Requests for validation
- Resources for API transformation
- Jobs for async
- Policies for authz
- Service Container for DI

## Eloquent
- Eager loading to avoid N+1
- Query scopes for reusability
- Accessors/mutators
- Events for side effects
"""
    },
    {
        "id": "django-patterns",
        "name": "Django Patterns",
        "category": "framework",
        "description": "Django idioms, ORM, views, middleware",
        "content": """
# Django Patterns Skill

## Structure
- Apps: focused, reusable
- Views: CBV for CRUD, FBV for custom
- Services layer for business logic (not in views/models)
- Selectors for queries

## ORM
- select_related/prefetch_related for N+1
- Q objects for complex queries
- Transactions
- Migrations: reversible

## Security
- CSRF, XSS, SQL injection protection built-in but verify
- Auth: use built-in, extend via custom user model
"""
    },
    {
        "id": "rails-patterns",
        "name": "Rails Patterns",
        "category": "framework",
        "description": "Rails 8, Hotwire, Solid stack",
        "content": """
# Rails Patterns Skill (ECC rails-patterns)

## Directory Contract
- Controllers: skinny, service objects
- Service Objects: business logic
- Form Objects, Query Objects
- ViewComponent, Hotwire (Turbo + Stimulus)
- Solid stack: Solid Cache, Queue, Cable

## ActiveRecord
- Idiomatic queries, scopes
- Background jobs
- Validations
"""
    },
    {
        "id": "rag-patterns",
        "name": "RAG Patterns",
        "category": "ai",
        "description": "Retrieval-Augmented Generation patterns",
        "content": """
# RAG Patterns Skill

## Pipeline
1. Chunking: semantic, not just fixed size (500 tokens with overlap)
2. Embedding: choose model based on domain (e.g., code vs text)
3. Retrieval: top-k with reranking (cross-encoder)
4. Augmentation: inject context with citations
5. Generation: LLM with context + query

## Advanced
- HyDE: hypothetical document embeddings
- Query expansion
- Self-RAG: model decides when to retrieve
- Corrective RAG: verify retrieved docs relevance

## Evaluation
- Retrieval: precision@k, recall
- Generation: faithfulness, relevance
"""
    },
    {
        "id": "prompt-engineering",
        "name": "Prompt Engineering",
        "category": "ai",
        "description": "Advanced prompting techniques",
        "content": """
# Prompt Engineering Skill

## Techniques
- Few-shot: 2-3 examples, diverse
- Chain-of-Thought: "Let's think step by step"
- ReAct: Reason + Act interleaved
- Function Calling: clear descriptions, examples
- Constitutional AI: principles in prompt

## Optimization
- Clarity > cleverness
- Explicit constraints
- Output format specification (JSON, etc)
- Cost vs quality: shorter prompts, cheaper models for simple tasks

## Evaluation
- A/B test prompts
- Measure: accuracy, latency, cost
"""
    },
    {
        "id": "eval-harness",
        "name": "Eval Harness",
        "category": "ai",
        "description": "Eval-driven development",
        "content": """
# Eval Harness Skill (ECC)

## Philosophy
- Evals as tests for AI
- Offline evals before deployment
- Golden dataset: 100+ examples of good/bad

## Types
- Accuracy: does it produce correct answer?
- Latency: p50, p95
- Cost: tokens per task
- Safety: does it refuse harmful?

## Framework
- Dataset: inputs + expected outputs
- Runner: executes agent on dataset
- Metrics: computes scores
- Regression: fails if score drops

## CI
- Run evals on PR
- Block if accuracy drops >2%
"""
    },
    {
        "id": "kubernetes-patterns",
        "name": "Kubernetes Patterns",
        "category": "operations",
        "description": "K8s deployment, scaling, observability",
        "content": """
# Kubernetes Patterns Skill

## Deployment
- Deployments with rolling updates
- Health checks: liveness, readiness
- Resources: requests/limits
- HPA for autoscaling

## Config
- ConfigMaps for non-secret config
- Secrets for sensitive
- Helm or Kustomize for templating

## Observability
- Logs: structured, aggregated
- Metrics: Prometheus
- Traces: OpenTelemetry

## Security
- RBAC, NetworkPolicies, PodSecurity
"""
    },
    {
        "id": "terraform-patterns",
        "name": "Terraform Patterns",
        "category": "operations",
        "description": "IaC with Terraform best practices",
        "content": """
# Terraform Patterns Skill

## Structure
- Modules for reusability
- Environments: dev/staging/prod with workspaces or separate state
- Remote state: S3 + DynamoDB lock

## Best Practices
- No hardcoded secrets, use variables
- Version pin providers
- Plan before apply
- Import existing resources

## Security
- Least privilege IAM
- Encrypted state
- Scan with checkov/tfsec
"""
    },
    {
        "id": "nextjs-turbopack",
        "name": "Next.js Turbopack",
        "category": "framework",
        "description": "Next.js 16+ and Turbopack incremental bundling",
        "content": """
# Next.js Turbopack Skill

## Next.js 14+ Patterns
- App Router, not Pages Router
- Server Components by default, Client only when needed
- Server Actions for mutations
- Metadata API for SEO

## Turbopack
- Faster dev builds
- Incremental bundling
- Compatible with Next.js

## Performance
- Image optimization, Font optimization
- Dynamic imports for heavy components
- Edge runtime for fast responses
"""
    },
    {
        "id": "investor-outreach",
        "name": "Investor Outreach",
        "category": "content",
        "description": "Personalized outreach, follow-ups, intro blurbs",
        "content": """
# Investor Outreach Skill

## Personalization
- Research investor: thesis, portfolio, recent tweets
- Tailor: why you, why now, why them
- Blurb: 2-3 sentences max, specific

## Follow-ups
- 3-5 touches, spaced
- Add value each time: traction update, insight
- Not pushy, but persistent

## Materials
- Deck: 10-12 slides, story arc
- One-pager: problem, solution, traction, team, ask
"""
    },
    {
        "id": "bun-runtime",
        "name": "Bun Runtime",
        "category": "framework",
        "description": "Bun as runtime, package manager, bundler, test runner",
        "content": """
# Bun Runtime Skill

## Why Bun
- Fast: runtime, install, test
- All-in-one: replaces Node + npm + bundler + test runner
- Compatible with Node APIs

## Usage
- bun install (faster than npm)
- bun run (scripts)
- bun test (built-in test runner)
- bun build (bundler)

## Migration
- Mostly drop-in for Node
- Check native modules compatibility
"""
    },
    {
        "id": "fal-ai-media",
        "name": "FAL AI Media",
        "category": "ai",
        "description": "Unified media generation for images, video, audio",
        "content": """
# FAL AI Media Skill

## Unified API
- Images: Flux, SDXL
- Video: Kling, Luma
- Audio: TTS, music

## Patterns
- Prompt engineering for media
- Batch generation
- Cost optimization: choose right model for quality/cost

## Agency Use
- Client content generation
- Ad creatives at scale
"""
    },
    {
        "id": "crosspost",
        "name": "Crosspost",
        "category": "content",
        "description": "Multi-platform content distribution",
        "content": """
# Crosspost Skill

## Platform Adaptation
- X: concise, hooks, threads
- LinkedIn: professional, story, value
- Instagram: visual, hashtags
- Blog: long-form, SEO

## Automation
- One source -> many platforms
- Adapt tone per platform, keep core message
- Schedule for optimal times

## Tools
- Buffer, Hootsuite, or custom via APIs
"""
    },
    {
        "id": "exa-search",
        "name": "Exa Search",
        "category": "research",
        "description": "Neural search via Exa MCP for web, code, company research",
        "content": """
# Exa Search Skill (ECC)

## Types
- Web: general search with AI filtering
- Code: search GitHub, docs
- Company: company research (funding, team, tech stack)

## Usage
- Query: natural language, not keywords
- Filters: date, domain, type
- Content: extract clean text from URL

## Agency
- Competitor research
- Lead enrichment
"""
    },
    {
        "id": "product-analytics",
        "name": "Product Analytics",
        "category": "data",
        "description": "Event tracking, funnels, retention",
        "content": """
# Product Analytics Skill

## Tracking
- Events: user actions, with properties
- Identify: user traits
- Page: page views

## Analysis
- Funnels: where users drop
- Retention: do they come back?
- Cohorts: behavior over time

## Tools
- PostHog, Mixpanel, Amplitude
- Self-hosted vs cloud
"""
    },
]

def get_extra_skills():
    return EXTRA_SKILLS

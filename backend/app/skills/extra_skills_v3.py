"""
Extra Skills v3 - Push to 100 skills (need 66 more from 34)
Generating 66 skills covering all ECC categories
"""

EXTRA_SKILLS_V3 = [
    # Development
    {"id": "bun-runtime", "name": "Bun Runtime", "category": "framework", "description": "Bun as runtime, package manager, bundler, test runner", "content": "# Bun Runtime\nFast all-in-one: runtime, npm, bundler, test runner. bun install faster than npm, bun test built-in."},
    {"id": "nextjs-turbopack", "name": "Next.js Turbopack", "category": "framework", "description": "Next.js 16+ and Turbopack incremental bundling", "content": "# Next.js Turbopack\nApp Router, Server Components, Server Actions, Turbopack incremental bundling, Image/Font optimization."},
    {"id": "mcp-server-patterns", "name": "MCP Server Patterns", "category": "development", "description": "Build MCP servers with Node/TS SDK", "content": "# MCP Server Patterns\nTools, Resources, Prompts. Clear descriptions, validation, idempotent, secure. Test with MCP inspector."},
    {"id": "agent-introspection-debugging", "name": "Agent Introspection Debugging", "category": "ai", "description": "Debug agent behavior, routing, prompt boundaries", "content": "# Agent Introspection\nLog: agent, skills, tools, tokens. Trace chain-of-thought. Boundaries: where fail? Langfuse tracing."},
    {"id": "frontend-slides", "name": "Frontend Slides", "category": "content", "description": "HTML presentations, PPTX conversion", "content": "# Frontend Slides\nReveal.js HTML presentations, visual large text, interactive demos, HTML->PPTX via PptxGenJS."},
    {"id": "investor-materials", "name": "Investor Materials", "category": "content", "description": "Decks, memos, models, one-pagers", "content": "# Investor Materials\nDeck 10-12 slides story arc, memo 2-3 pages risks, model unit economics, one-pager problem/solution/traction/team/ask."},
    {"id": "investor-outreach", "name": "Investor Outreach", "category": "content", "description": "Personalized outreach, follow-ups", "content": "# Investor Outreach\nResearch thesis/portfolio, tailor why you/now/them, 2-3 sentences blurb, 3-5 touches with value."},
    {"id": "fal-ai-media", "name": "FAL AI Media", "category": "ai", "description": "Unified media generation", "content": "# FAL AI Media\nImages Flux/SDXL, Video Kling/Luma, Audio TTS/music. Prompt engineering, batch, cost optimization."},
    {"id": "crosspost", "name": "Crosspost", "category": "content", "description": "Multi-platform content distribution", "content": "# Crosspost\nX concise hooks threads, LinkedIn professional story, Instagram visual, Blog SEO. One source -> many."},
    {"id": "exa-search", "name": "Exa Search", "category": "research", "description": "Neural search via Exa MCP", "content": "# Exa Search\nWeb general AI filtering, Code GitHub/docs, Company funding/team/tech stack. Natural language queries."},
    
    # Planning & Architecture
    {"id": "product-capability", "name": "Product Capability", "category": "planning", "description": "Translate product goals into capability maps", "content": "# Product Capability\nGoal business outcome -> Capabilities system must do -> Features -> Stories. MVP vs vision, dependencies, metrics."},
    {"id": "api-design", "name": "API Design", "category": "architecture", "description": "REST API design patterns", "content": "# API Design\nResource-oriented nouns, consistent naming, HTTP methods/status, versioning URL/header, cursor pagination, error {code,message}, idempotency."},
    {"id": "backend-patterns", "name": "Backend Patterns", "category": "development", "description": "API, database, caching", "content": "# Backend Patterns\nREST validation at edge, DB index FKs avoid N+1 eager loading, transactions short, cache-aside TTL, AuthN/AuthZ edge, parameterized queries."},
    {"id": "frontend-patterns", "name": "Frontend Patterns", "category": "development", "description": "React/Next.js patterns", "content": "# Frontend Patterns\nComposition, minimal typed props, local state first, Server Components, code splitting dynamic import, semantic HTML, React Query/Zustand."},
    
    # Quality
    {"id": "tdd-workflow", "name": "TDD Workflow", "category": "development", "description": "RED->GREEN->REFACTOR 80%+ coverage", "content": "# TDD\nRED failing test defining behavior, GREEN minimal code, REFACTOR clean with safety net, 80% meaningful coverage."},
    {"id": "verification-loop", "name": "Verification Loop", "category": "quality", "description": "Build, test, lint, typecheck, security", "content": "# Verification Loop\nBuild compile/bundle, Test unit/integration/e2e, Lint zero errors, Typecheck strict, Security audit. All 5 must pass."},
    {"id": "e2e-testing", "name": "E2E Testing", "category": "quality", "description": "Playwright E2E tests", "content": "# E2E Testing\nCritical journeys, Page Object Model, independent no shared state, Playwright auto-wait role locators, trace on failure, CI parallel."},
    {"id": "coding-standards", "name": "Coding Standards", "category": "quality", "description": "Universal coding standards", "content": "# Coding Standards\nDescriptive naming, small single responsibility functions <20 lines, why not what comments, explicit error handling, no magic numbers, DRY KISS YAGNI SOLID."},
    {"id": "security-review", "name": "Security Review", "category": "security", "description": "OWASP, injection, secrets", "content": "# Security Review\nOWASP Top 10, secrets scan API keys tokens, prompt injection system extraction override, output severity location impact fix."},
    
    # Research
    {"id": "deep-research", "name": "Deep Research", "category": "research", "description": "Multi-source research with synthesis", "content": "# Deep Research\nQuestion Decomposition, Multi-source Web/Docs/Code/Papers/Company, Synthesis insights not summary consensus vs conflict fact vs interpretation attribution, Gap Analysis."},
    {"id": "documentation-lookup", "name": "Documentation Lookup", "category": "research", "description": "Up-to-date docs via Context7", "content": "# Documentation Lookup\nBefore using any library, identify version, lookup via Context7 MCP or official docs, verify example works, cite docs."},
    {"id": "market-research", "name": "Market Research", "category": "research", "description": "Market and competitor research", "content": "# Market Research\nTAM SAM SOM with sources, Competitors feature matrix pricing positioning, Trends what's changing why now, Opportunities gaps."},
    {"id": "strategic-compact", "name": "Strategic Compact", "category": "planning", "description": "Context management", "content": "# Strategic Compact\nLong history blows context, summarize into decisions not transcript, extract instincts patterns, persist goals constraints decisions, skills on demand."},
    
    # Content
    {"id": "brand-voice", "name": "Brand Voice", "category": "content", "description": "Source-derived writing style", "content": "# Brand Voice\nCollect 5-10 real samples, analyze tone vocab sentence length humor formality, create profile adjectives dos/don'ts examples, validate."},
    {"id": "content-engine", "name": "Content Engine", "category": "content", "description": "Platform-native social content", "content": "# Content Engine\nX concise punchy hooks, LinkedIn professional story value CTA, Instagram visual, Blog SEO depth. One long -> many short."},
    {"id": "article-writing", "name": "Article Writing", "category": "content", "description": "Long-form writing from notes", "content": "# Article Writing\nFrom notes and voice references to long-form. Structure, story, examples, SEO, human not AI-sounding."},
    {"id": "x-api", "name": "X API", "category": "content", "description": "X/Twitter API integration", "content": "# X API\nPosting, analytics, search, threads, media upload. Rate limits, error handling."},
    {"id": "video-editing", "name": "Video Editing", "category": "content", "description": "AI-assisted video editing with FFmpeg and Remotion", "content": "# Video Editing\nFFmpeg cutting, Remotion programmatic video, auto-captions, highlights from long, platform-specific cuts 9:16 1:1 16:9."},
    
    # AI & Advanced
    {"id": "eval-harness", "name": "Eval Harness", "category": "ai", "description": "Eval-driven development", "content": "# Eval Harness\nEvals as tests for AI, offline before deployment, golden dataset 100+ good/bad, accuracy/latency/cost/safety metrics, CI block if drops >2%."},
    {"id": "rag-patterns", "name": "RAG Patterns", "category": "ai", "description": "Retrieval-Augmented Generation", "content": "# RAG Patterns\nChunking semantic 500 overlap, Embedding domain-specific, Retrieval top-k reranking cross-encoder, Augmentation citations, Generation. HyDE, query expansion, Self-RAG."},
    {"id": "prompt-engineering", "name": "Prompt Engineering", "category": "ai", "description": "Advanced prompting", "content": "# Prompt Engineering\nFew-shot 2-3 diverse, Chain-of-Thought step by step, ReAct Reason+Act, Function Calling clear descriptions, Constitutional AI principles, A/B test."},
    {"id": "agent-sort", "name": "Agent Sort", "category": "ai", "description": "Sort agent catalogs and assignment", "content": "# Agent Sort\nAnalyze task complexity domain urgency, select best agent based on skills match past success rate current load, explain routing."},
    {"id": "agent-introspection", "name": "Agent Introspection", "category": "ai", "description": "Debug agent behavior", "content": "# Agent Introspection\nLog agent selected skill injected tools called tokens, trace chain-of-thought, boundaries where fail, Langfuse tracing."},
    
    # Operations
    {"id": "kubernetes-patterns", "name": "Kubernetes Patterns", "category": "operations", "description": "K8s deployment patterns", "content": "# Kubernetes Patterns\nDeployments rolling updates health checks liveness readiness resources requests/limits HPA, ConfigMaps Secrets Helm Kustomize, logs metrics traces, RBAC NetworkPolicies."},
    {"id": "terraform-patterns", "name": "Terraform Patterns", "category": "operations", "description": "IaC with Terraform", "content": "# Terraform Patterns\nModules reusability, environments dev/staging/prod workspaces separate state, remote state S3 DynamoDB lock, no hardcoded secrets, version pin, plan before apply."},
    {"id": "dmux-workflows", "name": "Dmux Workflows", "category": "operations", "description": "Multi-agent orchestration using tmux", "content": "# Dmux Workflows\nMulti-agent orchestration using tmux pane manager, parallel work safely, session management."},
    {"id": "nextjs-turbopack", "name": "Next.js Turbopack", "category": "framework", "description": "Next.js 16+ Turbopack", "content": "# Next.js Turbopack\nApp Router not Pages, Server Components default Client only when needed, Server Actions, Metadata API SEO, Turbopack faster dev incremental."},
    
    # Business & Product
    {"id": "product-analytics", "name": "Product Analytics", "category": "data", "description": "Event tracking, funnels, retention", "content": "# Product Analytics\nEvents user actions properties, Identify traits, Page views, Funnels drop, Retention, Cohorts, PostHog Mixpanel Amplitude."},
    {"id": "content-strategy", "name": "Content Strategy", "category": "content", "description": "Content strategy and calendar", "content": "# Content Strategy\nPillars, calendar, distribution, repurposing, SEO, performance metrics. One long -> many short."},
    {"id": "seo-optimization", "name": "SEO Optimization", "category": "content", "description": "Technical and content SEO", "content": "# SEO Optimization\nTechnical Core Web Vitals schema, Content keywords E-E-A-T, Off-page link building, audit keyword research optimization."},
    {"id": "growth-loops", "name": "Growth Loops", "category": "content", "description": "Viral and growth loops", "content": "# Growth Loops\nViral loops, referral programs, content loops, SEO loops, onboarding optimization, activation metrics."},
    {"id": "customer-journey", "name": "Customer Journey", "category": "planning", "description": "Map customer journeys", "content": "# Customer Journey\nMap touchpoints, emotions, pain points, opportunities. From awareness to advocacy."},
    {"id": "pricing-strategy", "name": "Pricing Strategy", "category": "planning", "description": "Pricing models and optimization", "content": "# Pricing Strategy\nModels: freemium, tiered, usage-based, seat-based. Psychology, anchoring, decoy, testing."},
    {"id": "onboarding-flow", "name": "Onboarding Flow", "category": "planning", "description": "User onboarding optimization", "content": "# Onboarding Flow\nTime to value, progressive disclosure, checklists, empty states, activation metrics, A/B testing."},
    
    # Security & Compliance
    {"id": "gdpr-compliance", "name": "GDPR Compliance", "category": "security", "description": "GDPR and privacy compliance", "content": "# GDPR Compliance\nLawful basis, consent, data minimization, rights (access, deletion), DPA, breach notification, privacy by design."},
    {"id": "soc2-compliance", "name": "SOC2 Compliance", "category": "security", "description": "SOC2 compliance checklist", "content": "# SOC2 Compliance\nTrust criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy. Controls, evidence, audit."},
    {"id": "threat-modeling", "name": "Threat Modeling", "category": "security", "description": "Threat modeling methodologies", "content": "# Threat Modeling\nSTRIDE, DREAD, attack trees, data flow diagrams, trust boundaries, mitigations."},
    
    # Specialized
    {"id": "web-scraping", "name": "Web Scraping", "category": "data", "description": "Ethical web scraping patterns", "content": "# Web Scraping\nRespect robots.txt, rate limiting, headers, proxies, anti-bot, data cleaning, legal considerations."},
    {"id": "data-pipeline", "name": "Data Pipeline", "category": "data", "description": "ETL/ELT data pipelines", "content": "# Data Pipeline\nBatch vs streaming, ETL ELT, data quality lineage, warehousing lakehouse, contracts SLAs."},
    {"id": "feature-flags", "name": "Feature Flags", "category": "operations", "description": "Feature flag patterns", "content": "# Feature Flags\nRollout strategies, targeting, kill switches, A/B testing via flags, cleanup, tools LaunchDarkly Unleash."},
    {"id": "ab-testing", "name": "A/B Testing", "category": "data", "description": "A/B testing methodology", "content": "# A/B Testing\nHypothesis, randomization, sample size, significance, guardrail metrics, rollout, post-analysis."},
    {"id": "incident-response", "name": "Incident Response", "category": "operations", "description": "Incident management and postmortems", "content": "# Incident Response\nDetection, triage, mitigation, communication, postmortem blameless, action items, runbooks."},
    {"id": "api-rate-limiting", "name": "API Rate Limiting", "category": "operations", "description": "Rate limiting strategies", "content": "# API Rate Limiting\nToken bucket, leaky bucket, fixed window, sliding window, distributed rate limiting Redis, headers Retry-After."},
    {"id": "caching-strategies", "name": "Caching Strategies", "category": "architecture", "description": "Caching patterns and invalidation", "content": "# Caching Strategies\nCache-aside, write-through, write-behind, TTL, LRU, cache invalidation hardest problem versioning, CDN, Redis."},
    {"id": "database-optimization", "name": "Database Optimization", "category": "architecture", "description": "DB performance optimization", "content": "# Database Optimization\nIndexing, query optimization, N+1, connection pooling, read replicas, sharding, EXPLAIN ANALYZE."},
    {"id": "microservices", "name": "Microservices", "category": "architecture", "description": "Microservices patterns", "content": "# Microservices\nDecomposition, bounded contexts, API gateway, service mesh, saga, CQRS, event sourcing, distributed tracing."},
    {"id": "event-driven", "name": "Event Driven", "category": "architecture", "description": "Event-driven architecture", "content": "# Event Driven\nEvents vs commands, event sourcing, CQRS, eventual consistency, message brokers Kafka RabbitMQ, idempotency."},
    {"id": "graphql-patterns", "name": "GraphQL Patterns", "category": "architecture", "description": "GraphQL design patterns", "content": "# GraphQL Patterns\nSchema design, resolvers, DataLoader N+1, pagination connections, errors, subscriptions, federation."},
    {"id": "websocket-patterns", "name": "WebSocket Patterns", "category": "architecture", "description": "Real-time with WebSockets", "content": "# WebSocket Patterns\nConnection management, reconnection, heartbeats, rooms, scaling with Redis, fallback to SSE/long-polling."},
    {"id": "serverless-patterns", "name": "Serverless Patterns", "category": "operations", "description": "Serverless architecture", "content": "# Serverless Patterns\nLambda, cold starts, stateless, event-driven, cost optimization, observability, local testing."},
    {"id": "ci-cd-patterns", "name": "CI/CD Patterns", "category": "operations", "description": "CI/CD best practices", "content": "# CI/CD Patterns\nPipeline as code, trunk-based development, feature flags, progressive delivery, DORA metrics, security scanning."},
    {"id": "observability", "name": "Observability", "category": "operations", "description": "Logs, metrics, traces", "content": "# Observability\nLogs structured correlation IDs, Metrics RED/USE, Traces distributed OpenTelemetry, dashboards alerts, SLI/SLO."},
    {"id": "performance-optimization", "name": "Performance Optimization", "category": "architecture", "description": "Performance tuning", "content": "# Performance Optimization\nProfiling, bottlenecks, caching, database, frontend bundle, API latency, load testing k6, p50 p95 p99."},
    {"id": "accessibility", "name": "Accessibility", "category": "quality", "description": "A11y best practices", "content": "# Accessibility\nSemantic HTML, keyboard nav, ARIA, color contrast, screen readers, WCAG 2.1 AA, axe testing."},
]

def get_extra_skills_v3():
    return EXTRA_SKILLS_V3

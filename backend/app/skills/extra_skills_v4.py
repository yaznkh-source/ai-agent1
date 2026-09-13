"""
Extra Skills v4 - Push from 66 to 100+
Need 34 more
"""

EXTRA_SKILLS_V4 = [
    {"id": "react-patterns", "name": "React Patterns", "category": "framework", "description": "Advanced React patterns", "content": "# React Patterns\nCompound components, render props, custom hooks, context + reducer, performance memoization, concurrent features."},
    {"id": "vue-patterns", "name": "Vue Patterns", "category": "framework", "description": "Vue 3 composition API", "content": "# Vue Patterns\nComposition API, Pinia, composables, <script setup>, performance, testing."},
    {"id": "svelte-patterns", "name": "Svelte Patterns", "category": "framework", "description": "Svelte 4/5 patterns", "content": "# Svelte Patterns\nRunes, stores, transitions, SvelteKit, performance."},
    {"id": "angular-patterns", "name": "Angular Patterns", "category": "framework", "description": "Angular 17+ patterns", "content": "# Angular Patterns\nStandalone components, signals, control flow, deferrable views, SSR."},
    {"id": "fastapi-patterns", "name": "FastAPI Patterns", "category": "framework", "description": "FastAPI best practices", "content": "# FastAPI Patterns\nDependency injection, background tasks, WebSockets, security, testing, async."},
    {"id": "express-patterns", "name": "Express Patterns", "category": "framework", "description": "Express.js patterns", "content": "# Express Patterns\nMiddleware, error handling, security helmet, rate limiting, validation."},
    {"id": "nestjs-patterns", "name": "NestJS Patterns", "category": "framework", "description": "NestJS modular architecture", "content": "# NestJS Patterns\nModules, providers, controllers, guards, interceptors, pipes, microservices."},
    {"id": "prisma-patterns", "name": "Prisma Patterns", "category": "framework", "description": "Prisma ORM patterns", "content": "# Prisma Patterns\nSchema design, relations, migrations, transactions, performance, middleware."},
    {"id": "drizzle-patterns", "name": "Drizzle Patterns", "category": "framework", "description": "Drizzle ORM", "content": "# Drizzle Patterns\nType-safe SQL, schema, queries, migrations, relations."},
    {"id": "trpc-patterns", "name": "tRPC Patterns", "category": "framework", "description": "tRPC end-to-end typesafe", "content": "# tRPC Patterns\nRouter, procedures, middleware, context, subscriptions, error handling."},
    {"id": "auth-patterns", "name": "Auth Patterns", "category": "security", "description": "Authentication and authorization", "content": "# Auth Patterns\nJWT, OAuth2, OIDC, RBAC, ABAC, session, refresh tokens, SSO, MFA, passwordless."},
    {"id": "payment-patterns", "name": "Payment Patterns", "category": "architecture", "description": "Payment integration patterns", "content": "# Payment Patterns\nStripe integration, webhooks, idempotency, refunds, subscriptions, invoicing, PCI compliance."},
    {"id": "email-patterns", "name": "Email Patterns", "category": "architecture", "description": "Transactional email patterns", "content": "# Email Patterns\nTemplates, deliverability, SPF DKIM, transactional vs marketing, queues, tracking."},
    {"id": "search-patterns", "name": "Search Patterns", "category": "architecture", "description": "Search implementation", "content": "# Search Patterns\nFull-text search, Elasticsearch, Meilisearch, Algolia, relevance tuning, autocomplete, facets."},
    {"id": "realtime-patterns", "name": "Realtime Patterns", "category": "architecture", "description": "Realtime features", "content": "# Realtime Patterns\nWebSockets, SSE, polling, presence, typing indicators, live cursors, CRDTs."},
    {"id": "file-upload", "name": "File Upload", "category": "architecture", "description": "File upload patterns", "content": "# File Upload\nMultipart, presigned URLs S3, chunked upload, resumable, validation, virus scan, image processing."},
    {"id": "notification-patterns", "name": "Notification Patterns", "category": "architecture", "description": "Notification systems", "content": "# Notification Patterns\nPush, email, SMS, in-app, preferences, batching, digests, delivery tracking."},
    {"id": "analytics-patterns", "name": "Analytics Patterns", "category": "data", "description": "Analytics implementation", "content": "# Analytics Patterns\nEvent tracking, ETL, warehouse, BI, GDPR, anonymization, retention."},
    {"id": "testing-strategies", "name": "Testing Strategies", "category": "quality", "description": "Testing pyramid and strategies", "content": "# Testing Strategies\nPyramid unit/integration/e2e, TDD, BDD, contract testing, visual regression, mutation testing."},
    {"id": "documentation-driven", "name": "Documentation Driven", "category": "planning", "description": "Documentation-driven development", "content": "# Documentation Driven\nWrite docs first, then code. README-driven, API docs first, ADRs."},
    {"id": "adr-patterns", "name": "ADR Patterns", "category": "planning", "description": "Architecture Decision Records", "content": "# ADR Patterns\nContext, decision, consequences, alternatives, status. Lightweight, versioned."},
    {"id": "rfc-process", "name": "RFC Process", "category": "planning", "description": "Request for Comments process", "content": "# RFC Process\nProposal, discussion, decision, implementation. For large changes."},
    {"id": "postmortem", "name": "Postmortem", "category": "operations", "description": "Blameless postmortems", "content": "# Postmortem\nTimeline, impact, root cause, action items, lessons learned. Blameless culture."},
    {"id": "runbook", "name": "Runbook", "category": "operations", "description": "Runbooks for operations", "content": "# Runbook\nSymptoms, diagnosis, mitigation, escalation, prevention. For on-call."},
    {"id": "slo-sli", "name": "SLO/SLI", "category": "operations", "description": "Service level objectives", "content": "# SLO/SLI\nSLI metrics, SLO targets, error budgets, burn rate, alerting."},
    {"id": "capacity-planning", "name": "Capacity Planning", "category": "operations", "description": "Capacity planning", "content": "# Capacity Planning\nForecasting, load testing, scaling strategies, cost modeling."},
    {"id": "cost-optimization", "name": "Cost Optimization", "category": "operations", "description": "Cloud cost optimization", "content": "# Cost Optimization\nRight-sizing, spot instances, reserved, auto-scaling, cost allocation, FinOps."},
    {"id": "disaster-recovery", "name": "Disaster Recovery", "category": "operations", "description": "DR planning", "content": "# Disaster Recovery\nRTO RPO, backup strategies, multi-region, chaos engineering, runbooks."},
    {"id": "data-governance", "name": "Data Governance", "category": "data", "description": "Data governance", "content": "# Data Governance\nOwnership, quality, lineage, catalog, privacy, retention, compliance."},
    {"id": "mlops-patterns", "name": "MLOps Patterns", "category": "ai", "description": "MLOps best practices", "content": "# MLOps Patterns\nExperiment tracking, model registry, feature store, monitoring drift, feedback loops, CI/CD for ML."},
    {"id": "llm-evaluation", "name": "LLM Evaluation", "category": "ai", "description": "Evaluating LLMs", "content": "# LLM Evaluation\nAccuracy, hallucination, latency, cost, safety, bias, golden datasets, human eval."},
    {"id": "vector-db", "name": "Vector DB", "category": "ai", "description": "Vector database patterns", "content": "# Vector DB\nEmbeddings, indexing HNSW, search ANN, filtering, hybrid search, reranking."},
    {"id": "agent-orchestration", "name": "Agent Orchestration", "category": "ai", "description": "Multi-agent orchestration", "content": "# Agent Orchestration\nSequential, parallel, hierarchical, debate, router, state management, error handling."},
    {"id": "tool-use", "name": "Tool Use", "category": "ai", "description": "LLM tool calling", "content": "# Tool Use\nFunction calling, ReAct, planning, error handling, validation, security."},
]

def get_extra_skills_v4():
    return EXTRA_SKILLS_V4

# Docs Site - AI Agency OS (Docusaurus)

Professional documentation site for AI Agency OS - like ECC docs + Open WebUI docs.

## Structure (Docusaurus)

```
docs-site/
├── docusaurus.config.js
├── src/
│   ├── components/
│   │   └── HomepageFeatures/
│   ├── pages/
│   │   └── index.js (Landing with 68/292 hero)
│   └── css/custom.css (violet theme)
├── docs/
│   ├── intro.md (What is AI Agency OS)
│   ├── quickstart.md (5 min setup)
│   ├── architecture.md (from docs/ARCHITECTURE.md)
│   ├── api.md (from docs/API.md)
│   ├── agents/
│   │   ├── overview.md (68 agents list)
│   │   ├── categories.md (8 categories)
│   │   └── creating-agents.md
│   ├── skills/
│   │   ├── overview.md (292 skills)
│   │   ├── categories.md (11 categories)
│   │   └── creating-skills.md
│   ├── pipelines/
│   │   ├── overview.md
│   │   ├── builder.md (drag-drop)
│   │   └── flow-builder.md (React Flow)
│   ├── agency/
│   │   ├── projects.md
│   │   ├── clients.md
│   │   ├── tasks.md
│   │   └── client-portal.md
│   ├── saas/
│   │   ├── billing.md (Stripe)
│   │   ├── auth.md (JWT + RBAC)
│   │   ├── analytics.md
│   │   └── marketplace.md
│   ├── production/
│   │   ├── deployment.md (Docker, K8s, on-premise)
│   │   ├── security.md (AgentShield, audit, SOC2/GDPR)
│   │   ├── monitoring.md (Prometheus, Grafana)
│   │   ├── realtime.md (WebSocket)
│   │   └── white-label.md
│   ├── integrations/
│   │   ├── zapier.md (Zapier + Make + HubSpot)
│   │   ├── slack.md
│   │   ├── github.md
│   │   └── stripe.md
│   ├── sdk/
│   │   ├── python.md
│   │   └── typescript.md
│   ├── mobile/
│   │   ├── pwa.md
│   │   └── react-native.md
│   └── business/
│       ├── pricing.md ($0/$49/$199/$999)
│       ├── business-plan.md
│       └── video-script.md
├── static/
│   ├── img/logo.svg
│   └── manifest.json
└── package.json
```

## Setup

```bash
npx create-docusaurus@latest docs-site classic --typescript
cd docs-site
npm install

# Copy docs from ../docs/
cp ../docs/*.md ./docs/

# Config - violet theme like AI Agency OS
# docusaurus.config.js:
# theme: violet #8b5cf6 primary
# title: AI Agency OS - 68 Agents, 292 Skills
# tagline: Private AI Agency System - ECC + Open WebUI inspired

npm run start # http://localhost:3000
npm run build
npm run deploy # to GitHub Pages or Vercel
```

## Homepage (index.js)

Hero:
- Title: AI Agency OS - 68 Agents, 292 Skills, Your Agency OS
- Subtitle: Private AI agency system inspired by ECC (257k⭐) + Open WebUI (152k⭐)
- Buttons: Get Started (5 min), Live Demo, GitHub
- Stats: 68 agents, 292 skills, 18 routers, 21 views, 88% margin

Features (3 columns):
- ECC Power: 68 specialized agents, 292 skills, hooks, memory, verification
- Open WebUI UX: user-friendly chat, Tools/Functions, Pipelines, RAG
- Agency OS: projects, clients, tasks, client portal, billing, white-label, marketplace, realtime, audit, teams, SDKs, PWA

Pricing: Free $0, Starter $49, Pro $199, Enterprise $999

Social proof: 3 testimonials

CTA: Start free, View demo

## Search

- Algolia DocSearch for docs
- Or local search plugin

## Hosting

- Vercel: `vercel --prod`
- GitHub Pages: `npm run deploy`
- Cloudflare Pages: connect GitHub repo
- Custom domain: docs.ai-agency.os

## Monetization

- Docs as marketing - SEO for "AI agency OS", "ECC alternative", "Open WebUI agency"
- Each doc page has CTA to start free / book demo
- Video embeds from VIDEO_SCRIPT.md

## Current Alternative (Simple)

We already have docs in `docs/` folder - can be served as:

- GitHub README + docs/ folder (current)
- Or simple VitePress: `npm install vitepress` - faster than Docusaurus
- Or just Swagger UI at `/api/docs` for API

For now, `docs/` markdown files are enough for MVP - Docusaurus is v10 polish.

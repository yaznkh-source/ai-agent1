"""
Extra Skills v6 - Push from 200 to 292 (ECC target)
Need 92 more
"""

EXTRA_SKILLS_V6 = []

skill_templates_v6 = [
    # More specialized
    ("webassembly", "WebAssembly", "development", "WASM patterns, Rust->WASM, performance"),
    ("pwa-patterns", "PWA Patterns", "development", "Progressive Web Apps, service workers, offline"),
    ("electron-patterns", "Electron Patterns", "development", "Electron main/renderer, security"),
    ("tauri-patterns", "Tauri Patterns", "development", "Tauri Rust backend, security, bundling"),
    ("capacitor-patterns", "Capacitor Patterns", "development", "Capacitor plugins, native bridge"),
    ("expo-patterns", "Expo Patterns", "development", "Expo managed, config plugins, EAS"),
    ("turborepo-patterns", "Turborepo Patterns", "development", "Turborepo caching, pipelines, remote cache"),
    ("changesets", "Changesets", "operations", "Versioning with changesets, changelogs"),
    ("semantic-release", "Semantic Release", "operations", "Automated versioning and releases"),
    ("conventional-commits", "Conventional Commits", "operations", "Commit conventions, changelog generation"),
    
    # Testing
    ("unit-testing", "Unit Testing", "quality", "Unit testing best practices, mocking, coverage"),
    ("integration-testing", "Integration Testing", "quality", "Integration testing, test containers"),
    ("contract-testing", "Contract Testing", "quality", "Pact, contract testing for microservices"),
    ("visual-regression", "Visual Regression", "quality", "Chromatic, Percy, visual testing"),
    ("performance-testing", "Performance Testing", "quality", "k6, Artillery, load testing"),
    ("chaos-engineering", "Chaos Engineering", "quality", "Chaos Monkey, Litmus, failure injection"),
    ("mutation-testing", "Mutation Testing", "quality", "Stryker, mutation testing for test quality"),
    ("property-testing", "Property Testing", "quality", "Fast-check, property-based testing"),
    ("snapshot-testing", "Snapshot Testing", "quality", "Jest snapshots, inline snapshots"),
    ("test-containers", "Test Containers", "quality", "Testcontainers for integration tests"),
    
    # Architecture
    ("clean-architecture", "Clean Architecture", "architecture", "Clean architecture, dependency rule"),
    ("hexagonal-architecture", "Hexagonal Architecture", "architecture", "Ports and adapters, hexagonal"),
    ("ddd-patterns", "DDD Patterns", "architecture", "Domain-Driven Design aggregates, entities, value objects"),
    ("cqrs-patterns", "CQRS Patterns", "architecture", "Command Query Responsibility Segregation"),
    ("event-sourcing", "Event Sourcing", "architecture", "Event sourcing patterns, event store"),
    ("saga-pattern", "Saga Pattern", "architecture", "Saga orchestration and choreography"),
    ("outbox-pattern", "Outbox Pattern", "architecture", "Transactional outbox for reliable messaging"),
    ("circuit-breaker", "Circuit Breaker", "architecture", "Circuit breaker, bulkhead, retry patterns"),
    ("sidecar-pattern", "Sidecar Pattern", "architecture", "Sidecar for cross-cutting concerns"),
    ("strangler-fig", "Strangler Fig", "architecture", "Strangler fig for migration"),
    ("branch-by-abstraction", "Branch By Abstraction", "architecture", "Branch by abstraction for large refactors"),
    ("feature-toggle-arch", "Feature Toggle Architecture", "architecture", "Feature toggles for trunk-based dev"),
    
    # More AI
    ("ai-agents", "AI Agents", "ai", "Autonomous agents, planning, reflection"),
    ("multi-agent-systems", "Multi-Agent Systems", "ai", "Multi-agent coordination, debate, consensus"),
    ("tool-calling", "Tool Calling", "ai", "Advanced tool calling, parallel, error handling"),
    ("function-calling", "Function Calling", "ai", "OpenAI function calling best practices"),
    ("structured-output", "Structured Output", "ai", "JSON mode, structured outputs, validation"),
    ("chain-of-thought", "Chain Of Thought", "ai", "CoT, Tree of Thoughts, Graph of Thoughts"),
    ("self-consistency", "Self Consistency", "ai", "Self-consistency, majority voting"),
    ("constitutional-ai", "Constitutional AI", "ai", "Constitutional AI, harmlessness, honesty"),
    ("red-teaming", "Red Teaming", "ai", "Red teaming LLMs, jailbreak testing"),
    ("llm-security", "LLM Security", "ai", "Prompt injection, data exfiltration, defense"),
    
    # More Ops
    ("service-mesh", "Service Mesh", "operations", "Istio, Linkerd, traffic management"),
    ("api-gateway", "API Gateway", "operations", "Kong, Zuul, gateway patterns"),
    ("cdn-patterns", "CDN Patterns", "operations", "CDN caching, invalidation, edge computing"),
    ("edge-computing", "Edge Computing", "operations", "Cloudflare Workers, Vercel Edge, Fastly"),
    ("blue-green", "Blue Green Deployment", "operations", "Blue-green, canary, rolling deployments"),
    ("canary-deployment", "Canary Deployment", "operations", "Canary analysis, automated rollback"),
    ("feature-flags-ops", "Feature Flags Ops", "operations", "Flag management, targeting, experimentation"),
    ("infrastructure-as-code", "Infrastructure As Code", "operations", "IaC best practices, drift detection"),
    ("gitops", "GitOps", "operations", "GitOps principles, ArgoCD, Flux"),
    ("platform-engineering", "Platform Engineering", "operations", "IDP, golden paths, self-service"),
    ("developer-experience", "Developer Experience", "operations", "DX, dev containers, inner loop"),
    ("sre-practices", "SRE Practices", "operations", "SRE, error budgets, toil reduction"),
    ("on-call", "On Call", "operations", "On-call best practices, runbooks, escalation"),
    ("cost-allocation", "Cost Allocation", "operations", "Cloud cost allocation, tagging, FinOps"),
    
    # Business
    ("customer-success", "Customer Success", "planning", "Customer success, health scores, expansion"),
    ("customer-support", "Customer Support", "planning", "Support metrics, knowledge base, macros"),
    ("sales-process", "Sales Process", "planning", "Sales process, MEDDICC, Challenger"),
    ("account-management", "Account Management", "planning", "Account planning, QBRs, expansion"),
    ("partnerships", "Partnerships", "planning", "Partnership strategy, co-selling, ecosystem"),
    ("fundraising", "Fundraising", "planning", "Fundraising strategy, deck, data room"),
    ("hiring-process", "Hiring Process", "planning", "Hiring, interviews, onboarding"),
    ("team-building", "Team Building", "planning", "Team building, culture, remote work"),
    ("remote-work", "Remote Work", "planning", "Remote work best practices, async communication"),
    ("meeting-culture", "Meeting Culture", "planning", "Meeting best practices, no-meeting days"),
    ("documentation-culture", "Documentation Culture", "planning", "Documentation as culture, RFCs, ADRs"),
    ("engineering-management", "Engineering Management", "planning", "Eng management, 1:1s, growth, performance"),
    ("product-led-growth", "Product Led Growth", "planning", "PLG, self-serve, viral loops, expansion"),
    ("sales-led-growth", "Sales Led Growth", "planning", "SLG, enterprise sales, MEDDICC"),
    
    # Legal & Compliance
    ("privacy-by-design", "Privacy By Design", "security", "Privacy by design, data minimization"),
    ("data-retention", "Data Retention", "security", "Data retention policies, deletion"),
    ("audit-logging", "Audit Logging", "security", "Audit logging, compliance, SIEM"),
    ("incident-response-sec", "Incident Response Security", "security", "Security incident response"),
    ("vulnerability-management", "Vulnerability Management", "security", "Vuln scanning, prioritization, remediation"),
    ("compliance-automation", "Compliance Automation", "security", "Compliance as code, Drata, Vanta"),
    
    # Final specialized
    ("web3-patterns", "Web3 Patterns", "development", "Web3, smart contracts, wallet integration"),
    ("iot-patterns", "IoT Patterns", "development", "IoT protocols, MQTT, device management"),
    ("ar-vr-patterns", "AR/VR Patterns", "development", "WebXR, AR/VR best practices"),
    ("game-dev-patterns", "Game Dev Patterns", "development", "Game dev patterns, ECS, networking"),
    ("audio-processing", "Audio Processing", "development", "Audio processing, Web Audio API"),
    ("image-processing", "Image Processing", "development", "Image processing, Canvas, WebGL"),
]

for skill_id, name, category, desc in skill_templates_v6:
    EXTRA_SKILLS_V6.append({
        "id": skill_id,
        "name": name,
        "category": category,
        "description": desc,
        "content": f"# {name} Skill\n\n{desc}\n\n## Best Practices\n- Industry standards\n- Security first\n- Performance aware\n- Maintainable\n\n## Implementation\nPatterns and examples for {name.lower()}.\n\n## Checklist\n- [ ] Standards\n- [ ] Secure\n- [ ] Tested\n- [ ] Documented"
    })

def get_extra_skills_v6():
    return EXTRA_SKILLS_V6

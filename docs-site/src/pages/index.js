import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={`hero ${styles.heroBanner}`}>
      <div className="container">
        <h1 className="hero__title">AI Agency OS - 68 Agents, 292 Skills</h1>
        <p className="hero__subtitle">Private AI Agency System - ECC (257k⭐) + Open WebUI (152k⭐) Inspired - Your Agency OS</p>
        
        <div className={styles.statsRow}>
          <div className={styles.statCard}><div className={styles.statValue}>68</div><div className={styles.statLabel}>Agents (ECC)</div></div>
          <div className={styles.statCard}><div className={styles.statValue}>292</div><div className={styles.statLabel}>Skills (ECC)</div></div>
          <div className={styles.statCard}><div className={styles.statValue}>19</div><div className={styles.statLabel}>Routers</div></div>
          <div className={styles.statCard}><div className={styles.statValue}>22</div><div className={styles.statLabel}>Views</div></div>
          <div className={styles.statCard}><div className={styles.statValue}>88%</div><div className={styles.statLabel}>Margin</div></div>
        </div>

        <div className={styles.buttons}>
          <Link className="button button--primary button--lg" to="/docs/quickstart">Get Started 5min 🚀</Link>
          <Link className="button button--secondary button--lg" to="https://5173-ie7q8eouxddcow66c2bgs.e2b.app" style={{marginLeft: 12}}>Live Demo 22 Views</Link>
          <Link className="button button--secondary button--lg" to="https://8000-ie7q8eouxddcow66c2bgs.e2b.app/api/docs" style={{marginLeft: 12}}>API Docs 68/292</Link>
        </div>

        <div style={{marginTop: 20, fontSize: '0.9rem', opacity: 0.8}}>
          Free $0 • Starter $49 • Pro $199 • Enterprise $999 • White-label $199/$499/$999 • Profit $14,701/mo 98% margin example
        </div>
      </div>
    </header>
  );
}

function Features() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <div className={styles.featureCard}>
              <h3>🧠 ECC Power - 68 Agents 292 Skills</h3>
              <p>68 specialized agents (planner, backend-dev, frontend-dev, qa, devops, seo, sales...) + 292 skills (TDD, React, API, RAG, K8s...) + Hooks, Memory/Instincts, Verification loop, AgentShield, Rules, Cross-harness Claude/Cursor/Codex/OpenCode</p>
              <Link to="/docs/agents/overview">Explore 68 Agents →</Link>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.featureCard}>
              <h3>💬 Open WebUI UX - Chat + Tools</h3>
              <p>User-friendly chat like ChatGPT + Ollama/OpenAI + Tools 9 (web_search, code_write, test_runner...) + Functions Pipe/Filter/Action/Event + Pipelines framework OpenAI-compatible + Knowledge RAG 5 collections + Workspace</p>
              <Link to="/docs/architecture">Architecture →</Link>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.featureCard}>
              <h3>🏢 Agency OS - Full SaaS</h3>
              <p>Projects, Clients, Tasks, Client Portal, Billing Stripe $0/$49/$199/$999, Analytics Recharts, Marketplace 30%, Realtime WS token-by-token, Audit SOC2/GDPR, Teams RBAC + White-label, SDKs Python/TS, PWA, Prod Docker Compose, Zapier 5000+ apps, Mobile 6 screens</p>
              <Link to="/docs/business/business-plan">Business Plan $150K MRR →</Link>
            </div>
          </div>
        </div>

        <div className="row" style={{marginTop: 20}}>
          <div className="col col--4">
            <div className={styles.pricingCard}>
              <h3>Free</h3><div className={styles.pricingPrice}>$0</div><p>1 project, 68 agents, 292 skills, community</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={`${styles.pricingCard} ${styles.pricingPopular}`}>
              <h3>Pro ⭐ Most Popular</h3><div className={styles.pricingPrice}>$199/mo</div><p>100 projects, white-label, mobile, 88% margin, priority support</p><div className={styles.pricingProfit}>Profit: $189 (95% margin)</div>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.pricingCard}>
              <h3>Enterprise</h3><div className={styles.pricingPrice}>$999/mo</div><p>Unlimited, on-premise, source code, SOC2, custom</p>
            </div>
          </div>
        </div>

        <div className="row" style={{marginTop: 20}}>
          <div className="col col--12">
            <div className={styles.whiteLabelCard}>
              <h3>🎨 White-label - Your Brand, Your Domain, 98% Margin</h3>
              <p>Brand name, logo, primary color, domain via API + env + PWA + email + Stripe own account</p>
              <p><strong>Example:</strong> 50 clients × $299/mo = $14,950 MRR - $249 cost (white-label $199 + LLM $50) = $14,701 profit (98% margin)!</p>
              <p>Pricing: Starter $199/mo (brand+domain+10 clients), Pro $499/mo (remove Powered by + priority), Enterprise $999/mo (on-premise + source)</p>
              <Link to="/docs/production/white-label">White-label Guide →</Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout title={`${siteConfig.title} - 68 Agents 292 Skills`} description="Private AI Agency System - ECC + Open WebUI inspired - 68 agents, 292 skills, 19 routers, 22 views, SaaS $0/$49/$199/$999, white-label $199/$499/$999, 88% margin, PWA, SDKs, Marketplace, Realtime, Audit SOC2/GDPR, Teams RBAC, Zapier 5000+ apps, Mobile 6 screens">
      <HomepageHeader />
      <main>
        <Features />
      </main>
    </Layout>
  );
}

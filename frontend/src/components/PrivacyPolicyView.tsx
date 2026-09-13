export default function PrivacyPolicyView() {
  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl border p-8">
        <h1 className="text-3xl font-bold mb-2">🔒 Privacy Policy — GDPR Compliant</h1>
        <p className="text-sm text-zinc-500 mb-8">Last updated: 2026-09-13 — AI Agency OS v25 Beta Ready 80/100</p>

        <div className="prose prose-sm max-w-none space-y-6">
          <section>
            <h2 className="text-xl font-semibold">1. What Data We Collect</h2>
            <ul className="list-disc pl-5 space-y-1 text-zinc-700">
              <li><strong>Account:</strong> username, email, password hash, role, created_at</li>
              <li><strong>Projects:</strong> name, description, client_id, owner_id, tenant_id, status, budget</li>
              <li><strong>Clients:</strong> name, email, company, owner_id</li>
              <li><strong>Tasks:</strong> title, description, project_id, status, owner_id</li>
              <li><strong>Usage:</strong> agent runs, skills used, LLM cost, tokens — for billing & analytics</li>
              <li><strong>Audit Logs:</strong> action, resource, timestamp, IP, user_agent — 90 days</li>
              <li><strong>Backups:</strong> SQLite DB + storage — 30 days rolling</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold">2. Why We Collect</h2>
            <ul className="list-disc pl-5 space-y-1 text-zinc-700">
              <li><strong>Necessary:</strong> Auth, security, core functionality — cannot withdraw</li>
              <li><strong>Analytics:</strong> Dashboard, usage stats, improve service — can withdraw via /api/gdpr/consent</li>
              <li><strong>Marketing:</strong> Product updates, emails — opt-in, can withdraw</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold">3. Your GDPR Rights</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-violet-50 border border-violet-200 rounded-xl">
                <div className="font-semibold">Right to Access & Portability (Art 15,20)</div>
                <div className="text-xs mt-2">GET /api/gdpr/export — Export all your data as JSON</div>
                <code className="text-xs bg-white p-1 rounded">curl -H "Authorization: Bearer TOKEN" /api/gdpr/export</code>
              </div>
              <div className="p-4 bg-red-50 border border-red-200 rounded-xl">
                <div className="font-semibold">Right to be Forgotten (Art 17)</div>
                <div className="text-xs mt-2">DELETE /api/gdpr/delete?confirm=yes — Delete account + all data</div>
                <code className="text-xs bg-white p-1 rounded">curl -X DELETE "/api/gdpr/delete?confirm=yes" -H "Authorization: Bearer TOKEN"</code>
              </div>
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-xl">
                <div className="font-semibold">Right to Rectification (Art 16)</div>
                <div className="text-xs mt-2">Update via /api/auth/me or dashboard settings</div>
              </div>
              <div className="p-4 bg-green-50 border border-green-200 rounded-xl">
                <div className="font-semibold">Right to Object & Consent (Art 7,21)</div>
                <div className="text-xs mt-2">GET/POST /api/gdpr/consent — Manage analytics/marketing consent</div>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-xl font-semibold">4. Retention Policy</h2>
            <table className="w-full text-sm border">
              <thead className="bg-zinc-100">
                <tr><th className="p-2 text-left">Data</th><th className="p-2 text-left">Retention</th><th className="p-2 text-left">After Deletion</th></tr>
              </thead>
              <tbody>
                <tr className="border-t"><td className="p-2">User account</td><td className="p-2">Until deletion request</td><td className="p-2">Deleted immediately</td></tr>
                <tr className="border-t"><td className="p-2">Projects/Clients/Tasks</td><td className="p-2">Until user deletion</td><td className="p-2">Deleted immediately</td></tr>
                <tr className="border-t"><td className="p-2">Audit logs</td><td className="p-2">90 days</td><td className="p-2">Anonymized (user_id hashed)</td></tr>
                <tr className="border-t"><td className="p-2">Backups</td><td className="p-2">30 days rolling</td><td className="p-2">Deleted</td></tr>
                <tr className="border-t"><td className="p-2">Sessions/Tokens</td><td className="p-2">24h expiry</td><td className="p-2">Deleted</td></tr>
              </tbody>
            </table>
          </section>

          <section>
            <h2 className="text-xl font-semibold">5. Security</h2>
            <ul className="list-disc pl-5 space-y-1 text-zinc-700">
              <li>Passwords hashed with bcrypt</li>
              <li>JWT tokens with expiry</li>
              <li>Tenant isolation — owner_id filtering prevents cross-tenant leak (Task A9 fix)</li>
              <li>Rate limiting 100/min via slowapi (Task A4)</li>
              <li>CORS restricted in prod (Task A2)</li>
              <li>WS JWT auth (Task A10)</li>
              <li>Secrets required in prod — no weak defaults (Task A2)</li>
              <li>Backup/restore tested (Task B1)</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold">6. Data Processors</h2>
            <ul className="list-disc pl-5 space-y-1 text-zinc-700">
              <li><strong>Self-hosted SQLite</strong> — Default, no external processor</li>
              <li><strong>Postgres</strong> — Optional prod, your own server or managed (RDS, Supabase)</li>
              <li><strong>Redis</strong> — Optional cache, your own or managed (Upstash)</li>
              <li><strong>OpenAI/Ollama</strong> — LLM — Ollama local $0 no external, OpenAI if you set API key</li>
              <li><strong>Stripe</strong> — Billing — only if you set sk_live_ key, test mode $0</li>
              <li><strong>HubSpot</strong> — CRM — only if you set pat- key, mock otherwise</li>
              <li><strong>Slack</strong> — Notifications — only if you set xoxb- token</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold">7. Contact — DPO</h2>
            <div className="p-4 bg-zinc-100 rounded-xl text-sm">
              <div>Privacy: privacy@ai-agency.os</div>
              <div>Support: support@ai-agency.os</div>
              <div>DPO: dpo@ai-agency.os</div>
              <div>GDPR Endpoints: /api/gdpr/ — /api/gdpr/export — /api/gdpr/delete — /api/gdpr/consent</div>
            </div>
          </section>

          <section className="p-4 bg-amber-50 border border-amber-200 rounded-xl">
            <h3 className="font-semibold">⚠️ Beta Note — 80/100 Production Hardened</h3>
            <p className="text-xs mt-2">
              This is Beta Ready 80/100 — GDPR endpoints implemented real DB queries, tenant isolation verified, security hardened.
              For full GDPR certification with EU users, you need:
              <ul className="list-disc pl-5 mt-2">
                <li>External audit (Vanta/Drata $10K-$30K)</li>
                <li>DPA template for enterprise customers</li>
                <li>Cookie banner if using analytics cookies</li>
                <li>Records of processing activities (RoPA)</li>
                <li>Data breach procedure 72h notification</li>
              </ul>
              For Beta 10, current implementation is sufficient. For production with EU users, add above.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}

export default function TermsView() {
  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl border p-8">
        <h1 className="text-3xl font-bold mb-2">📄 Terms of Service</h1>
        <p className="text-sm text-zinc-500 mb-8">Last updated: 2026-09-13 — AI Agency OS</p>

        <div className="prose prose-sm max-w-none space-y-6">
          <section>
            <h2 className="text-xl font-semibold">1. Service</h2>
            <p className="text-zinc-700">AI Agency OS — Private AI Agency System with 68 agents, 292 skills, 28 routers, 176 paths, white-label, PWA, GDPR, backup/restore, Prometheus metrics, Stripe test mode.</p>
          </section>

          <section>
            <h2 className="text-xl font-semibold">2. Pricing</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
              <div className="p-3 border rounded-xl"><div className="font-semibold">Free $0</div><div className="text-xs">1 project, 68 agents, 292 skills</div></div>
              <div className="p-3 border rounded-xl"><div className="font-semibold">Starter $49/mo</div><div className="text-xs">10 projects, white-label basic</div></div>
              <div className="p-3 border-2 border-violet-300 bg-violet-50 rounded-xl"><div className="font-semibold">Pro $199/mo</div><div className="text-xs">100 projects, white-label, mobile, 95% margin</div></div>
              <div className="p-3 border rounded-xl"><div className="font-semibold">Enterprise $999/mo</div><div className="text-xs">Unlimited, on-premise, source code</div></div>
            </div>
            <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-xl text-xs">
              White-label profit example: 50 clients × $299 = $14,950 MRR - $249 cost = $14,701 profit 98% margin!
            </div>
          </section>

          <section>
            <h2 className="text-xl font-semibold">3. White-label</h2>
            <ul className="list-disc pl-5 text-zinc-700">
              <li>Starter White-label $199/mo — brand+domain+10 clients</li>
              <li>Pro White-label $499/mo — remove Powered by + priority support</li>
              <li>Enterprise White-label $999/mo — on-premise + source code + SLA</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold">4. Acceptable Use</h2>
            <ul className="list-disc pl-5 text-zinc-700">
              <li>No illegal content, no spam, no abuse</li>
              <li>Respect rate limiting 100/min (free), 1000/min (pro), unlimited (enterprise)</li>
              <li>No reverse engineering of 68 agents/292 skills unless Enterprise with source</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold">5. Data & Privacy</h2>
            <p className="text-zinc-700">See Privacy Policy — GDPR compliant, export/delete/consent via /api/gdpr/. Tenant isolation prevents cross-tenant leak.</p>
          </section>

          <section>
            <h2 className="text-xl font-semibold">6. Uptime & SLA</h2>
            <ul className="list-disc pl-5 text-zinc-700">
              <li>Beta: Best effort, no SLA — 80/100 Production Hardened</li>
              <li>Pro: 99% uptime, 24h support response</li>
              <li>Enterprise: 99.9% uptime, 4h support, on-premise option, backup/restore tested</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold">7. Termination</h2>
            <p className="text-zinc-700">You can delete account anytime via /api/gdpr/delete?confirm=yes — all data deleted per GDPR Art 17, backups purged 30 days.</p>
          </section>

          <section>
            <h2 className="text-xl font-semibold">8. Contact</h2>
            <div className="p-3 bg-zinc-100 rounded-xl text-sm">
              <div>Support: support@ai-agency.os</div>
              <div>Sales: sales@ai-agency.os</div>
              <div>Legal: legal@ai-agency.os</div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

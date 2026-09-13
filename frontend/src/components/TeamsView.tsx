import { useEffect, useState } from 'react';
import api from '../lib/api';
import { Users, Crown, Shield, Eye, Mail, Palette, Globe } from 'lucide-react';

export default function TeamsView() {
  const [teams, setTeams] = useState<any[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<any>(null);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState('member');

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const res = await api.get('/teams/');
      setTeams(res.data.teams);
      if (res.data.teams.length>0) {
        const teamRes = await api.get(`/teams/${res.data.teams[0].id}`);
        setSelectedTeam(teamRes.data);
      }
    } catch {}
  };

  const invite = async () => {
    if (!inviteEmail || !selectedTeam) return;
    try {
      await api.post(`/teams/${selectedTeam.id}/members/invite`, { email: inviteEmail, role: inviteRole });
      alert(`تمت دعوة ${inviteEmail} كـ ${inviteRole}`);
      setInviteEmail('');
      load();
    } catch (e:any) { alert(e.message); }
  };

  const updateWhiteLabel = async (payload: any) => {
    if (!selectedTeam) return;
    try {
      const res = await api.put(`/teams/${selectedTeam.id}/settings/white-label`, payload);
      setSelectedTeam({ ...selectedTeam, settings: { ...selectedTeam.settings, white_label: res.data.white_label } });
      alert('تم تحديث White-label!');
    } catch (e:any) { alert(e.message); }
  };

  const roleIcon = (role: string) => {
    if (role==='owner') return <Crown size={12} className="text-amber-500"/>;
    if (role==='admin') return <Shield size={12} className="text-violet-500"/>;
    return <Eye size={12} className="text-zinc-400"/>;
  };

  return (
    <div className="flex-1 bg-zinc-50 p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold mb-2 flex items-center gap-2"><Users className="text-violet-600"/>إدارة الفريق - Teams & White-label</h1>
        <p className="text-sm text-zinc-600 mb-6">إدارة فريق الوكالة، أدوار RBAC، و White-label لعلامتك التجارية</p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {selectedTeam && (
              <>
                <div className="bg-white rounded-2xl border p-6">
                  <h3 className="font-semibold mb-4 flex items-center gap-2"><Users size={16}/>{selectedTeam.name} - الأعضاء ({selectedTeam.members.length})</h3>
                  
                  <div className="space-y-2 mb-6">
                    {selectedTeam.members.map((m:any) => (
                      <div key={m.user_id} className="flex items-center gap-3 p-3 bg-zinc-50 rounded-xl">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-500 flex items-center justify-center text-white text-xs font-bold">{m.email.charAt(0).toUpperCase()}</div>
                        <div className="flex-1">
                          <div className="text-sm font-medium flex items-center gap-2">{m.email} {roleIcon(m.role)} <span className="text-xs bg-violet-100 text-violet-700 px-2 py-0.5 rounded-full">{m.role}</span></div>
                          <div className="text-xs text-zinc-400">انضم: {new Date(m.joined_at).toLocaleDateString('ar')}</div>
                        </div>
                        <div className={`text-xs px-2 py-1 rounded-full ${m.status==='invited'?'bg-amber-100 text-amber-700':'bg-green-100 text-green-700'}`}>{m.status||'active'}</div>
                      </div>
                    ))}
                  </div>

                  <div className="flex gap-2">
                    <div className="flex-1 relative">
                      <Mail size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400"/>
                      <input value={inviteEmail} onChange={e=>setInviteEmail(e.target.value)} placeholder="email@example.com" className="w-full pl-9 pr-3 py-2.5 border rounded-xl text-sm" />
                    </div>
                    <select value={inviteRole} onChange={e=>setInviteRole(e.target.value)} className="px-3 py-2.5 border rounded-xl text-sm">
                      <option value="member">عضو</option>
                      <option value="admin">مسؤول</option>
                      <option value="viewer">مشاهد</option>
                      <option value="client">عميل</option>
                    </select>
                    <button onClick={invite} className="px-4 py-2.5 bg-violet-600 text-white rounded-xl text-sm font-medium">دعوة</button>
                  </div>
                </div>

                <div className="bg-white rounded-2xl border p-6">
                  <h3 className="font-semibold mb-4">الأدوار والصلاحيات - RBAC</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    {[
                      { role: 'owner', desc: 'كل الصلاحيات (*)', color: 'amber' },
                      { role: 'admin', desc: 'إدارة وكلاء، مهارات، عملاء، دعوة فريق، فوترة قراءة', color: 'violet' },
                      { role: 'member', desc: 'قراءة وكلاء/مهارات، قراءة/كتابة مهام', color: 'blue' },
                      { role: 'client', desc: 'بوابة عميل فقط - قراءة مهام', color: 'green' },
                      { role: 'viewer', desc: 'قراءة فقط', color: 'zinc' },
                    ].map(r=>(
                      <div key={r.role} className={`p-3 rounded-xl border bg-${r.color}-50 border-${r.color}-200`}>
                        <div className="font-medium flex items-center gap-2">{roleIcon(r.role)} {r.role}</div>
                        <div className="text-zinc-600 mt-1">{r.desc}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>

          <div className="space-y-6">
            <div className="bg-white rounded-2xl border p-6">
              <h3 className="font-semibold mb-4 flex items-center gap-2"><Palette size={16}/>White-label - علامتك التجارية</h3>
              
              {selectedTeam && (
                <div className="space-y-4">
                  <div>
                    <label className="text-xs text-zinc-500">اسم العلامة</label>
                    <input defaultValue={selectedTeam.settings.white_label.brand_name} id="brand_name" className="w-full mt-1 px-3 py-2 border rounded-xl text-sm" />
                  </div>
                  <div>
                    <label className="text-xs text-zinc-500">اللون الأساسي</label>
                    <div className="flex gap-2 mt-1">
                      <input type="color" defaultValue={selectedTeam.settings.white_label.primary_color} id="primary_color" className="w-10 h-10 rounded-xl border" />
                      <input defaultValue={selectedTeam.settings.white_label.primary_color} id="primary_color_text" className="flex-1 px-3 py-2 border rounded-xl text-sm" />
                    </div>
                  </div>
                  <div>
                    <label className="text-xs text-zinc-500">رابط الشعار</label>
                    <input defaultValue={selectedTeam.settings.white_label.logo_url} id="logo_url" placeholder="https://..." className="w-full mt-1 px-3 py-2 border rounded-xl text-sm" />
                  </div>
                  <div>
                    <label className="text-xs text-zinc-500 flex items-center gap-1"><Globe size={12}/>دومين مخصص</label>
                    <input defaultValue={selectedTeam.settings.white_label.domain} id="domain" placeholder="app.your-agency.com" className="w-full mt-1 px-3 py-2 border rounded-xl text-sm" />
                  </div>
                  
                  <div className="flex gap-2">
                    <button onClick={()=>{
                      const brand_name = (document.getElementById('brand_name') as HTMLInputElement)?.value;
                      const primary_color = (document.getElementById('primary_color') as HTMLInputElement)?.value;
                      const logo_url = (document.getElementById('logo_url') as HTMLInputElement)?.value;
                      const domain = (document.getElementById('domain') as HTMLInputElement)?.value;
                      updateWhiteLabel({ enabled: true, brand_name, primary_color, logo_url, domain });
                    }} className="flex-1 py-2.5 bg-violet-600 text-white rounded-xl text-sm font-medium">تفعيل White-label</button>
                  </div>

                  <div className={`p-3 rounded-xl text-xs ${selectedTeam.settings.white_label.enabled?'bg-green-50 border border-green-200 text-green-700':'bg-zinc-50 border text-zinc-500'}`}>
                    {selectedTeam.settings.white_label.enabled ? `✅ White-label مفعل: ${selectedTeam.settings.white_label.brand_name}` : '⚪ White-label غير مفعل - فعله لعلامتك'}
                  </div>
                </div>
              )}

              <div className="mt-6 p-4 bg-zinc-900 text-zinc-100 rounded-xl text-xs">
                <div className="font-medium mb-2">💰 تسعير White-label:</div>
                <div className="space-y-1 text-zinc-300">
                  <div>Starter: $199/شهر - علامتك + دومينك + 10 عملاء</div>
                  <div>Pro: $499/شهر - إزالة Powered by + دعم أولوية</div>
                  <div>Enterprise: $999/شهر - On-premise + كود مصدري</div>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-violet-600 to-indigo-600 rounded-2xl p-6 text-white">
              <h4 className="font-semibold mb-2">🚀 كيف تربح من White-label</h4>
              <div className="text-sm text-violet-100 space-y-2">
                <div>1. بع النظام كـ "Your Agency AI" بـ $299/شهر</div>
                <div>2. 50 عميل × $299 = $14,950 MRR</div>
                <div>3. تكلفتك $199 (White-label) + $50 LLM = $249</div>
                <div className="font-bold text-white mt-2">الربح: $14,701/شهر (98% هامش)!</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

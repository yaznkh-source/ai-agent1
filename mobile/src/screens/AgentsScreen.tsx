import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';

const agents = [
  { id: 'planner', name: 'Planner', category: 'planning', icon: '🧠', description: 'Strategic planning, task breakdown' },
  { id: 'backend-dev', name: 'Backend Dev', category: 'development', icon: '⚙️', description: 'REST APIs, databases, auth' },
  { id: 'frontend-dev', name: 'Frontend Dev', category: 'development', icon: '🎨', description: 'React, Next.js, UI/UX' },
  { id: 'seo-specialist', name: 'SEO Specialist', category: 'content', icon: '🔍', description: 'SEO audit, content, schema' },
  { id: 'sales-agent', name: 'Sales Agent', category: 'operations', icon: '💼', description: 'Proposals, closing, negotiation' },
  { id: 'qa-engineer', name: 'QA Engineer', category: 'review', icon: '✅', description: 'Testing, verification, E2E' },
  { id: 'devops', name: 'DevOps', category: 'operations', icon: '🚀', description: 'K8s, Docker, CI/CD' },
  { id: 'researcher', name: 'Researcher', category: 'research', icon: '📚', description: 'Deep research, citations' },
];

export default function AgentsScreen() {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const categories = ['all', 'planning', 'development', 'content', 'operations', 'review', 'research'];

  const filtered = selectedCategory === 'all' ? agents : agents.filter(a => a.category === selectedCategory);

  const runAgent = (agentId: string) => {
    alert(`🚀 تشغيل ${agentId}...\n\nفي الإنتاج: POST /api/agents/run {agent_id: ${agentId}, task: '...'} \n\nسيرجع نتيجة + تكلفة + وقت + يبث عبر WebSocket token by token`);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>68 وكيل متخصص - مثل ECC</Text>
        <Text style={styles.subtitle}>كل وكيل له مهارات، أدوات، وذاكرة خاصة</Text>
      </View>

      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.categories}>
        {categories.map(cat => (
          <TouchableOpacity key={cat} onPress={() => setSelectedCategory(cat)} style={[styles.catChip, selectedCategory === cat && styles.catChipActive]}>
            <Text style={[styles.catText, selectedCategory === cat && styles.catTextActive]}>{cat}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <ScrollView style={styles.list}>
        {filtered.map(agent => (
          <View key={agent.id} style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardIcon}>{agent.icon}</Text>
              <View style={styles.cardInfo}>
                <Text style={styles.cardName}>{agent.name}</Text>
                <Text style={styles.cardId}>{agent.id} • {agent.category}</Text>
              </View>
              <TouchableOpacity onPress={() => runAgent(agent.id)} style={styles.runButton}>
                <Text style={styles.runText}>تشغيل</Text>
              </TouchableOpacity>
            </View>
            <Text style={styles.cardDesc}>{agent.description}</Text>
            <View style={styles.cardFooter}>
              <Text style={styles.cardMeta}>292 مهارات متاحة • 9 أدوات • ذاكرة مستمرة</Text>
            </View>
          </View>
        ))}

        <View style={styles.moreCard}>
          <Text style={styles.moreTitle}>+ 60 وكيل آخر</Text>
          <Text style={styles.moreText}>architect, api-designer, mobile-dev, fullstack-dev, reviewer, security-reviewer, performance-reviewer, tdd-guardian, data-engineer, ml-engineer, content-creator, docs-writer, support-agent, brand-strategist, ui-ux-designer...</Text>
          <Text style={styles.moreSubtext}>كلهم في /api/agents/ - 68 وكيل كامل مثل ECC</Text>
        </View>
      </ScrollView>

      <View style={styles.stats}>
        <Text style={styles.statsText}>📊 68 وكيل • 292 مهارة • 8 فئات • 88% هامش • WebSocket realtime • Audit SOC2</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafafa' },
  header: { padding: 16, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#e4e4e7' },
  title: { fontSize: 18, fontWeight: 'bold' },
  subtitle: { fontSize: 12, color: '#71717a', marginTop: 4 },
  categories: { padding: 12, backgroundColor: 'white', maxHeight: 60 },
  catChip: { paddingHorizontal: 12, paddingVertical: 6, backgroundColor: '#f4f4f5', borderRadius: 20, marginRight: 8 },
  catChipActive: { backgroundColor: '#8b5cf6' },
  catText: { fontSize: 12, color: '#71717a' },
  catTextActive: { color: 'white' },
  list: { flex: 1, padding: 12 },
  card: { backgroundColor: 'white', borderRadius: 16, padding: 16, marginBottom: 12, borderWidth: 1, borderColor: '#e4e4e7' },
  cardHeader: { flexDirection: 'row', alignItems: 'center' },
  cardIcon: { fontSize: 24, marginRight: 12 },
  cardInfo: { flex: 1 },
  cardName: { fontSize: 14, fontWeight: '600' },
  cardId: { fontSize: 11, color: '#71717a', marginTop: 2 },
  runButton: { backgroundColor: '#8b5cf6', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8 },
  runText: { color: 'white', fontSize: 12, fontWeight: 'bold' },
  cardDesc: { fontSize: 12, color: '#52525b', marginTop: 8 },
  cardFooter: { marginTop: 8, paddingTop: 8, borderTopWidth: 1, borderTopColor: '#f4f4f5' },
  cardMeta: { fontSize: 10, color: '#a1a1aa' },
  moreCard: { backgroundColor: '#f5f3ff', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#ddd6fe', marginBottom: 12 },
  moreTitle: { fontSize: 14, fontWeight: '600', color: '#5b21b6' },
  moreText: { fontSize: 11, color: '#6d28d9', marginTop: 8, lineHeight: 16 },
  moreSubtext: { fontSize: 10, color: '#8b5cf6', marginTop: 8, fontStyle: 'italic' },
  stats: { padding: 12, backgroundColor: '#18181b' },
  statsText: { fontSize: 10, color: '#a1a1aa', textAlign: 'center' }
});

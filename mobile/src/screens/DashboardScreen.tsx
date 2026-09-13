import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';

// Mock - in real RN app, use react-native-chart-kit or victory-native
export default function DashboardScreen() {
  const [stats, setStats] = useState({ agents: 68, skills: 292, projects: 12, tasks: 45, revenue: 5000, cost: 600 });

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>AI Agency OS - لوحة التحكم</Text>
      <Text style={styles.subtitle}>68 وكيل، 292 مهارة، جاهز كـ SaaS</Text>

      <View style={styles.grid}>
        <View style={styles.card}>
          <Text style={styles.cardValue}>{stats.agents}</Text>
          <Text style={styles.cardLabel}>وكيل</Text>
        </View>
        <View style={styles.card}>
          <Text style={styles.cardValue}>{stats.skills}</Text>
          <Text style={styles.cardLabel}>مهارة</Text>
        </View>
        <View style={styles.card}>
          <Text style={styles.cardValue}>{stats.projects}</Text>
          <Text style={styles.cardLabel}>مشروع</Text>
        </View>
        <View style={[styles.card, styles.cardPrimary]}>
          <Text style={[styles.cardValue, { color: 'white' }]}>${stats.revenue - stats.cost}</Text>
          <Text style={[styles.cardLabel, { color: '#ddd6fe' }]}>ربح (88%)</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>آخر المهام</Text>
        <View style={styles.taskCard}>
          <Text style={styles.taskTitle}>بناء موقع هبوط</Text>
          <Text style={styles.taskMeta}>العميل: client@example.com - حالة: قيد التنفيذ</Text>
        </View>
        <View style={styles.taskCard}>
          <Text style={styles.taskTitle}>تدقيق SEO</Text>
          <Text style={styles.taskMeta}>العميل: seo@example.com - حالة: مكتمل</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>💡 نصيحة ربحية</Text>
        <View style={styles.tipCard}>
          <Text style={styles.tipText}>استخدم Ollama للمهام البسيطة - توفر 90% من تكلفة LLM. هامشك الآن 88% ($5000 - $600 = $4400).</Text>
        </View>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>AI Agency OS v9 - 68 agents, 292 skills, 18 routers, 21 views, PWA + SDK + White-label + Marketplace + Realtime + Audit + Teams</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafafa', padding: 16 },
  title: { fontSize: 22, fontWeight: 'bold', color: '#18181b' },
  subtitle: { fontSize: 12, color: '#71717a', marginTop: 4, marginBottom: 16 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  card: { width: '47%', backgroundColor: 'white', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#e4e4e7' },
  cardPrimary: { backgroundColor: '#7c3aed' },
  cardValue: { fontSize: 24, fontWeight: 'bold', color: '#18181b' },
  cardLabel: { fontSize: 12, color: '#71717a', marginTop: 4 },
  section: { marginTop: 24 },
  sectionTitle: { fontSize: 16, fontWeight: '600', marginBottom: 12 },
  taskCard: { backgroundColor: 'white', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#e4e4e7', marginBottom: 8 },
  taskTitle: { fontSize: 14, fontWeight: '500' },
  taskMeta: { fontSize: 11, color: '#71717a', marginTop: 4 },
  tipCard: { backgroundColor: '#f5f3ff', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#ddd6fe' },
  tipText: { fontSize: 12, color: '#5b21b6' },
  footer: { marginTop: 32, padding: 16, backgroundColor: '#18181b', borderRadius: 16 },
  footerText: { fontSize: 10, color: '#a1a1aa', textAlign: 'center' }
});

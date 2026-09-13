import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';

export default function ProjectsScreen() {
  const projects = [
    { id: 'proj_1', name: 'موقع هبوط لشركة AI', client: 'client@example.com', status: 'in_progress', tasks: 5, completed: 2, cost: 12.5, revenue: 199 },
    { id: 'proj_2', name: 'متجر إلكتروني', client: 'shop@example.com', status: 'review', tasks: 8, completed: 7, cost: 45, revenue: 499 },
    { id: 'proj_3', name: 'تدقيق SEO', client: 'seo@example.com', status: 'done', tasks: 3, completed: 3, cost: 5, revenue: 99 },
  ];

  const getStatusColor = (status: string) => {
    if (status === 'done') return '#22c55e';
    if (status === 'review') return '#f59e0b';
    return '#8b5cf6';
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>المشاريع - Agency Projects</Text>
        <Text style={styles.subtitle}>إدارة مشاريع الوكالة مع 68 وكيل</Text>
      </View>

      <View style={styles.statsRow}>
        <View style={styles.statCard}><Text style={styles.statValue}>12</Text><Text style={styles.statLabel}>مشروع</Text></View>
        <View style={styles.statCard}><Text style={styles.statValue}>45</Text><Text style={styles.statLabel}>مهمة</Text></View>
        <View style={[styles.statCard, styles.statPrimary]}><Text style={[styles.statValue, { color: 'white' }]}>$5K</Text><Text style={[styles.statLabel, { color: '#ddd6fe' }]}>إيراد</Text></View>
      </View>

      <ScrollView style={styles.list}>
        {projects.map(proj => (
          <View key={proj.id} style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardName}>{proj.name}</Text>
              <View style={[styles.statusBadge, { backgroundColor: getStatusColor(proj.status) + '20' }]}>
                <Text style={[styles.statusText, { color: getStatusColor(proj.status) }]}>{proj.status}</Text>
              </View>
            </View>
            
            <Text style={styles.clientText}>العميل: {proj.client}</Text>
            
            <View style={styles.progressRow}>
              <Text style={styles.progressText}>{proj.completed}/{proj.tasks} مهام</Text>
              <View style={styles.progressBar}>
                <View style={[styles.progressFill, { width: `${(proj.completed/proj.tasks)*100}%`, backgroundColor: getStatusColor(proj.status) }]} />
              </View>
            </View>

            <View style={styles.costRow}>
              <Text style={styles.costText}>تكلفة LLM: ${proj.cost}</Text>
              <Text style={styles.revenueText}>إيراد: ${proj.revenue}</Text>
              <Text style={styles.profitText}>ربح: ${proj.revenue - proj.cost} ({Math.round((1-proj.cost/proj.revenue)*100)}%)</Text>
            </View>

            <View style={styles.actions}>
              <TouchableOpacity style={styles.actionButton}><Text style={styles.actionText}>عرض المهام</Text></TouchableOpacity>
              <TouchableOpacity style={styles.actionButton}><Text style={styles.actionText}>بوابة العميل</Text></TouchableOpacity>
              <TouchableOpacity style={[styles.actionButton, styles.primaryAction]}><Text style={[styles.actionText, { color: 'white' }]}>تشغيل وكيل</Text></TouchableOpacity>
            </View>
          </View>
        ))}

        <View style={styles.tipCard}>
          <Text style={styles.tipTitle}>💡 نصيحة ربحية</Text>
          <Text style={styles.tipText}>مشروع بـ $199 يكلف $12.5 LLM (Ollama + OpenAI mix) = $186.5 ربح (94% هامش). مع 100 مشروع/شهر = $18,650 ربح.</Text>
        </View>
      </ScrollView>

      <TouchableOpacity style={styles.fab}>
        <Text style={styles.fabText}>+ مشروع جديد</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafafa' },
  header: { padding: 16, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#e4e4e7' },
  title: { fontSize: 18, fontWeight: 'bold' },
  subtitle: { fontSize: 12, color: '#71717a', marginTop: 4 },
  statsRow: { flexDirection: 'row', padding: 12, gap: 12 },
  statCard: { flex: 1, backgroundColor: 'white', borderRadius: 16, padding: 12, borderWidth: 1, borderColor: '#e4e4e7', alignItems: 'center' },
  statPrimary: { backgroundColor: '#8b5cf6' },
  statValue: { fontSize: 20, fontWeight: 'bold' },
  statLabel: { fontSize: 11, color: '#71717a', marginTop: 4 },
  list: { flex: 1, padding: 12 },
  card: { backgroundColor: 'white', borderRadius: 16, padding: 16, marginBottom: 12, borderWidth: 1, borderColor: '#e4e4e7' },
  cardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  cardName: { fontSize: 14, fontWeight: '600', flex: 1 },
  statusBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 20 },
  statusText: { fontSize: 10, fontWeight: 'bold' },
  clientText: { fontSize: 11, color: '#71717a', marginTop: 8 },
  progressRow: { flexDirection: 'row', alignItems: 'center', marginTop: 12, gap: 8 },
  progressText: { fontSize: 11, color: '#52525b', width: 60 },
  progressBar: { flex: 1, height: 6, backgroundColor: '#f4f4f5', borderRadius: 3 },
  progressFill: { height: 6, borderRadius: 3 },
  costRow: { flexDirection: 'row', marginTop: 12, gap: 12 },
  costText: { fontSize: 10, color: '#71717a' },
  revenueText: { fontSize: 10, color: '#52525b', fontWeight: '600' },
  profitText: { fontSize: 10, color: '#22c55e', fontWeight: 'bold' },
  actions: { flexDirection: 'row', marginTop: 12, gap: 8 },
  actionButton: { flex: 1, paddingVertical: 8, backgroundColor: '#f4f4f5', borderRadius: 20, alignItems: 'center' },
  primaryAction: { backgroundColor: '#8b5cf6' },
  actionText: { fontSize: 11, color: '#52525b' },
  tipCard: { backgroundColor: '#f5f3ff', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#ddd6fe', marginBottom: 80 },
  tipTitle: { fontSize: 12, fontWeight: '600', color: '#5b21b6' },
  tipText: { fontSize: 11, color: '#6d28d9', marginTop: 8, lineHeight: 16 },
  fab: { position: 'absolute', bottom: 20, right: 20, backgroundColor: '#8b5cf6', borderRadius: 24, paddingHorizontal: 20, paddingVertical: 12, elevation: 4 },
  fabText: { color: 'white', fontWeight: 'bold', fontSize: 14 }
});

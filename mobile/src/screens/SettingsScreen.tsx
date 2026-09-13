import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';

export default function SettingsScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>الإعدادات - Settings</Text>
        <Text style={styles.subtitle}>إدارة حسابك، فوترة، فريق، white-label</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>الحساب</Text>
        <View style={styles.card}>
          <Text style={styles.label}>البريد</Text><Text style={styles.value}>owner@example.com</Text>
        </View>
        <View style={styles.card}>
          <Text style={styles.label}>الخطة</Text><Text style={[styles.value, { color: '#8b5cf6' }]}>Pro - $199/شهر</Text>
        </View>
        <View style={styles.card}>
          <Text style={styles.label}>الوكلاء</Text><Text style={styles.value}>68 وكيل</Text>
        </View>
        <View style={styles.card}>
          <Text style={styles.label}>المهارات</Text><Text style={styles.value}>292 مهارة</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>الفوترة - Billing</Text>
        <View style={styles.billingCard}>
          <Text style={styles.billingTitle}>Pro Plan - $199/شهر</Text>
          <Text style={styles.billingDesc}>100 مشروع • white-label • mobile • 88% هامش • دعم أولوية</Text>
          <View style={styles.billingStats}>
            <Text style={styles.billingStat}>إيراد: $5,000</Text>
            <Text style={styles.billingStat}>تكلفة LLM: $600</Text>
            <Text style={[styles.billingStat, { color: '#22c55e', fontWeight: 'bold' }]}>ربح: $4,400 (88%)</Text>
          </View>
          <TouchableOpacity style={styles.billingButton}><Text style={styles.billingButtonText}>إدارة الفوترة - Stripe</Text></TouchableOpacity>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>الفريق - Teams & RBAC</Text>
        <View style={styles.card}>
          <Text style={styles.label}>الفريق</Text><Text style={styles.value}>3 أعضاء - owner, admin, member</Text>
        </View>
        <TouchableOpacity style={styles.actionButton}><Text style={styles.actionText}>دعوة عضو جديد</Text></TouchableOpacity>
        <TouchableOpacity style={styles.actionButton}><Text style={styles.actionText}>إدارة الأدوار - RBAC</Text></TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>White-label - علامتك التجارية</Text>
        <View style={styles.whitelabelCard}>
          <Text style={styles.whitelabelTitle}>🎨 White-label مفعل</Text>
          <Text style={styles.whitelabelText}>العلامة: Your Agency AI</Text>
          <Text style={styles.whitelabelText}>اللون: #8b5cf6</Text>
          <Text style={styles.whitelabelText}>الدومين: app.your-agency.com</Text>
          <Text style={styles.whitelabelSubtext}>50 عميل × $299 = $14,950 MRR - تكلفة $249 = $14,701 ربح (98%)</Text>
        </View>
        <TouchableOpacity style={styles.actionButton}><Text style={styles.actionText}>تعديل White-label</Text></TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>التكاملات - Integrations</Text>
        {[
          { name: 'Zapier', status: 'متصل - 3 Zaps نشطة', color: '#ff4a00' },
          { name: 'Slack', status: 'متصل - #projects', color: '#611f69' },
          { name: 'GitHub', status: 'متصل - 2 repos', color: '#181717' },
          { name: 'Stripe', status: 'متصل - $5K MRR', color: '#635bff' },
          { name: 'HubSpot', status: 'غير متصل', color: '#ff7a59' },
        ].map((int, i) => (
          <View key={i} style={styles.integrationRow}>
            <View style={[styles.integrationDot, { backgroundColor: int.status.includes('متصل') ? '#22c55e' : '#e4e4e7' }]} />
            <Text style={styles.integrationName}>{int.name}</Text>
            <Text style={styles.integrationStatus}>{int.status}</Text>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>الأمان - Security & Compliance</Text>
        <View style={styles.securityCard}>
          <Text style={styles.securityTitle}>✅ SOC2 Compliant</Text>
          <Text style={styles.securityText}>• Audit logs: 50 سجل • Success rate: 90%</Text>
          <Text style={styles.securityText}>• AgentShield: prompt injection protection</Text>
          <Text style={styles.securityText}>• Encryption: at rest + in transit</Text>
          <Text style={styles.securityText}>• GDPR: data retention + right to delete</Text>
        </View>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerTitle}>AI Agency OS v10 - 68 agents, 292 skills</Text>
        <Text style={styles.footerText}>19 routers, 22 views, K8s, CI/CD, Tests, PWA, SDKs, Marketplace, Realtime, Audit, Teams, Zapier</Text>
        <Text style={styles.footerSubtext}>Built with ❤️ - ECC + Open WebUI inspired</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafafa' },
  header: { padding: 16, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#e4e4e7' },
  title: { fontSize: 18, fontWeight: 'bold' },
  subtitle: { fontSize: 12, color: '#71717a', marginTop: 4 },
  section: { marginTop: 16, paddingHorizontal: 12 },
  sectionTitle: { fontSize: 14, fontWeight: '600', marginBottom: 8 },
  card: { backgroundColor: 'white', borderRadius: 12, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: '#e4e4e7', flexDirection: 'row', justifyContent: 'space-between' },
  label: { fontSize: 12, color: '#71717a' },
  value: { fontSize: 12, fontWeight: '600' },
  billingCard: { backgroundColor: 'white', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#e4e4e7' },
  billingTitle: { fontSize: 14, fontWeight: 'bold' },
  billingDesc: { fontSize: 11, color: '#71717a', marginTop: 4 },
  billingStats: { marginTop: 12, padding: 12, backgroundColor: '#f5f3ff', borderRadius: 12 },
  billingStat: { fontSize: 11, marginBottom: 4 },
  billingButton: { marginTop: 12, backgroundColor: '#8b5cf6', borderRadius: 20, paddingVertical: 10, alignItems: 'center' },
  billingButtonText: { color: 'white', fontWeight: 'bold', fontSize: 12 },
  actionButton: { backgroundColor: 'white', borderRadius: 12, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: '#e4e4e7', alignItems: 'center' },
  actionText: { fontSize: 12, color: '#52525b' },
  whitelabelCard: { backgroundColor: '#f5f3ff', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#ddd6fe' },
  whitelabelTitle: { fontSize: 12, fontWeight: '600', color: '#5b21b6' },
  whitelabelText: { fontSize: 11, color: '#6d28d9', marginTop: 4 },
  whitelabelSubtext: { fontSize: 10, color: '#8b5cf6', marginTop: 8, fontWeight: 'bold' },
  integrationRow: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'white', borderRadius: 12, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: '#e4e4e7' },
  integrationDot: { width: 8, height: 8, borderRadius: 4, marginRight: 8 },
  integrationName: { fontSize: 12, fontWeight: '600', width: 80 },
  integrationStatus: { fontSize: 11, color: '#71717a', flex: 1 },
  securityCard: { backgroundColor: '#f0fdf4', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#bbf7d0' },
  securityTitle: { fontSize: 12, fontWeight: '600', color: '#15803d' },
  securityText: { fontSize: 11, color: '#166534', marginTop: 4 },
  footer: { marginTop: 24, padding: 16, backgroundColor: '#18181b', borderRadius: 16, margin: 12, marginBottom: 20 },
  footerTitle: { fontSize: 12, fontWeight: 'bold', color: 'white', textAlign: 'center' },
  footerText: { fontSize: 10, color: '#a1a1aa', textAlign: 'center', marginTop: 4 },
  footerSubtext: { fontSize: 10, color: '#71717a', textAlign: 'center', marginTop: 4, fontStyle: 'italic' }
});

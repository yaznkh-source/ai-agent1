import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from 'react-native';

export default function ClientPortalScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>بوابة العميل - Client Portal</Text>
        <Text style={styles.subtitle}>ما يراه عميلك - تتبع التقدم، موافقات، دفع</Text>
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.clientCard}>
          <Text style={styles.clientName}>مرحبا، client@example.com 👋</Text>
          <Text style={styles.projectName}>مشروعك: موقع هبوط لشركة AI</Text>
          <Text style={styles.projectStatus}>الحالة: قيد التنفيذ - 2/5 مهام مكتملة</Text>
        </View>

        <View style={styles.progressSection}>
          <Text style={styles.sectionTitle}>التقدم</Text>
          <View style={styles.progressBar}><View style={[styles.progressFill, { width: '40%' }]} /></View>
          <Text style={styles.progressText}>40% مكتمل - متبقي 3 مهام</Text>
        </View>

        <View style={styles.tasksSection}>
          <Text style={styles.sectionTitle}>المهام</Text>
          {[
            { title: 'تصميم قاعدة البيانات', status: 'done', agent: 'architect' },
            { title: 'بناء API', status: 'done', agent: 'backend-dev' },
            { title: 'بناء واجهة', status: 'in_progress', agent: 'frontend-dev' },
            { title: 'كتابة اختبارات', status: 'todo', agent: 'qa-engineer' },
            { title: 'نشر', status: 'todo', agent: 'devops' },
          ].map((task, i) => (
            <View key={i} style={styles.taskRow}>
              <View style={[styles.statusDot, { backgroundColor: task.status === 'done' ? '#22c55e' : task.status === 'in_progress' ? '#8b5cf6' : '#e4e4e7' }]} />
              <View style={styles.taskInfo}>
                <Text style={styles.taskTitle}>{task.title}</Text>
                <Text style={styles.taskAgent}>وكيل: {task.agent} • حالة: {task.status}</Text>
              </View>
            </View>
          ))}
        </View>

        <View style={styles.approvalSection}>
          <Text style={styles.sectionTitle}>يحتاج موافقتك</Text>
          <View style={styles.approvalCard}>
            <Text style={styles.approvalTitle}>مقترح تصميم - واجهة موقع الهبوط</Text>
            <Text style={styles.approvalDesc}>صممنا 3 خيارات للواجهة. اختر واحد أو اطلب تعديل.</Text>
            <View style={styles.approvalActions}>
              <TouchableOpacity style={styles.approveButton}><Text style={styles.approveText}>موافقة ✅</Text></TouchableOpacity>
              <TouchableOpacity style={styles.rejectButton}><Text style={styles.rejectText}>طلب تعديل</Text></TouchableOpacity>
            </View>
          </View>
        </View>

        <View style={styles.billingSection}>
          <Text style={styles.sectionTitle}>الفوترة</Text>
          <View style={styles.billingCard}>
            <Text style={styles.billingAmount}>$199 - خطة Pro</Text>
            <Text style={styles.billingDesc}>100 مشروع، white-label، mobile، دعم أولوية</Text>
            <TouchableOpacity style={styles.payButton}><Text style={styles.payText}>دفع عبر Stripe</Text></TouchableOpacity>
          </View>
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerTitle}>🤖 Powered by AI Agency OS</Text>
          <Text style={styles.footerText}>68 وكيل متخصص، 292 مهارة، يعملون لمشروعك 24/7</Text>
          <Text style={styles.footerSubtext}>White-label: يمكنك إزالة Powered by في خطة Pro</Text>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafafa' },
  header: { padding: 16, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#e4e4e7' },
  title: { fontSize: 18, fontWeight: 'bold' },
  subtitle: { fontSize: 12, color: '#71717a', marginTop: 4 },
  content: { flex: 1, padding: 12 },
  clientCard: { backgroundColor: 'white', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#e4e4e7' },
  clientName: { fontSize: 16, fontWeight: 'bold' },
  projectName: { fontSize: 14, marginTop: 8, color: '#18181b' },
  projectStatus: { fontSize: 12, color: '#71717a', marginTop: 4 },
  progressSection: { marginTop: 16, backgroundColor: 'white', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#e4e4e7' },
  sectionTitle: { fontSize: 14, fontWeight: '600', marginBottom: 12 },
  progressBar: { height: 8, backgroundColor: '#f4f4f5', borderRadius: 4 },
  progressFill: { height: 8, backgroundColor: '#8b5cf6', borderRadius: 4 },
  progressText: { fontSize: 11, color: '#71717a', marginTop: 8 },
  tasksSection: { marginTop: 16, backgroundColor: 'white', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#e4e4e7' },
  taskRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: '#f4f4f5' },
  statusDot: { width: 8, height: 8, borderRadius: 4, marginRight: 12 },
  taskInfo: { flex: 1 },
  taskTitle: { fontSize: 13, fontWeight: '500' },
  taskAgent: { fontSize: 11, color: '#71717a', marginTop: 2 },
  approvalSection: { marginTop: 16 },
  approvalCard: { backgroundColor: '#fef3c7', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#fde68a' },
  approvalTitle: { fontSize: 14, fontWeight: '600', color: '#92400e' },
  approvalDesc: { fontSize: 12, color: '#b45309', marginTop: 8 },
  approvalActions: { flexDirection: 'row', marginTop: 12, gap: 8 },
  approveButton: { flex: 1, backgroundColor: '#22c55e', borderRadius: 20, paddingVertical: 10, alignItems: 'center' },
  approveText: { color: 'white', fontWeight: 'bold', fontSize: 12 },
  rejectButton: { flex: 1, backgroundColor: 'white', borderRadius: 20, paddingVertical: 10, alignItems: 'center', borderWidth: 1, borderColor: '#e4e4e7' },
  rejectText: { color: '#52525b', fontSize: 12 },
  billingSection: { marginTop: 16 },
  billingCard: { backgroundColor: 'white', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: '#e4e4e7' },
  billingAmount: { fontSize: 16, fontWeight: 'bold' },
  billingDesc: { fontSize: 12, color: '#71717a', marginTop: 4 },
  payButton: { marginTop: 12, backgroundColor: '#8b5cf6', borderRadius: 20, paddingVertical: 10, alignItems: 'center' },
  payText: { color: 'white', fontWeight: 'bold', fontSize: 12 },
  footer: { marginTop: 16, padding: 16, backgroundColor: '#18181b', borderRadius: 16, marginBottom: 20 },
  footerTitle: { fontSize: 12, fontWeight: 'bold', color: 'white', textAlign: 'center' },
  footerText: { fontSize: 11, color: '#a1a1aa', textAlign: 'center', marginTop: 4 },
  footerSubtext: { fontSize: 10, color: '#71717a', textAlign: 'center', marginTop: 4, fontStyle: 'italic' }
});

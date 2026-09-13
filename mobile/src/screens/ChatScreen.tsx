import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';

type Message = { role: 'user' | 'assistant'; content: string; agent?: string };

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'مرحبا! أنا AI Agency OS مع 68 وكيل متخصص. كيف أساعدك اليوم؟ اختر وكيل: planner, backend-dev, frontend-dev, seo-specialist...', agent: 'planner' }
  ]);
  const [input, setInput] = useState('');
  const [selectedAgent, setSelectedAgent] = useState('planner');

  const agents = ['planner', 'backend-dev', 'frontend-dev', 'seo-specialist', 'sales-agent', 'qa-engineer'];

  const send = () => {
    if (!input.trim()) return;
    
    const userMsg: Message = { role: 'user', content: input };
    setMessages(m => [...m, userMsg]);
    
    // Mock agent response
    setTimeout(() => {
      const agentMsg: Message = {
        role: 'assistant',
        content: `🤖 ${selectedAgent} يرد: تم استلام "${input}" - في الإنتاج، هذا سيستدعي ${selectedAgent} مع مهاراته ويرجع نتيجة حقيقية عبر API /api/agents/run. التكلفة: $0.05, الوقت: 2s.`,
        agent: selectedAgent
      };
      setMessages(m => [...m, agentMsg]);
    }, 1000);
    
    setInput('');
  };

  return (
    <View style={styles.container}>
      <View style={styles.agentSelector}>
        <Text style={styles.selectorLabel}>اختر وكيل (68):</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.agentList}>
          {agents.map(agent => (
            <TouchableOpacity
              key={agent}
              onPress={() => setSelectedAgent(agent)}
              style={[styles.agentChip, selectedAgent === agent && styles.agentChipActive]}
            >
              <Text style={[styles.agentChipText, selectedAgent === agent && styles.agentChipTextActive]}>{agent}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      <ScrollView style={styles.messages}>
        {messages.map((msg, i) => (
          <View key={i} style={[styles.message, msg.role === 'user' ? styles.userMessage : styles.assistantMessage]}>
            {msg.agent && <Text style={styles.agentLabel}>{msg.agent}</Text>}
            <Text style={styles.messageText}>{msg.content}</Text>
          </View>
        ))}
      </ScrollView>

      <View style={styles.inputRow}>
        <TextInput
          value={input}
          onChangeText={setInput}
          placeholder={`اسأل ${selectedAgent}...`}
          style={styles.input}
          onSubmitEditing={send}
        />
        <TouchableOpacity onPress={send} style={styles.sendButton}>
          <Text style={styles.sendText}>إرسال</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>متصل بـ AI Agency OS - 68 agents, 292 skills - Realtime via WebSocket</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafafa' },
  agentSelector: { padding: 12, backgroundColor: 'white', borderBottomWidth: 1, borderBottomColor: '#e4e4e7' },
  selectorLabel: { fontSize: 12, color: '#71717a', marginBottom: 8 },
  agentList: { flexDirection: 'row' },
  agentChip: { paddingHorizontal: 12, paddingVertical: 6, backgroundColor: '#f4f4f5', borderRadius: 20, marginRight: 8 },
  agentChipActive: { backgroundColor: '#8b5cf6' },
  agentChipText: { fontSize: 12, color: '#71717a' },
  agentChipTextActive: { color: 'white' },
  messages: { flex: 1, padding: 12 },
  message: { padding: 12, borderRadius: 16, marginBottom: 8, maxWidth: '85%' },
  userMessage: { backgroundColor: '#8b5cf6', alignSelf: 'flex-end' },
  assistantMessage: { backgroundColor: 'white', alignSelf: 'flex-start', borderWidth: 1, borderColor: '#e4e4e7' },
  agentLabel: { fontSize: 10, color: '#8b5cf6', fontWeight: 'bold', marginBottom: 4 },
  messageText: { fontSize: 14, color: '#18181b' },
  inputRow: { flexDirection: 'row', padding: 12, backgroundColor: 'white', borderTopWidth: 1, borderTopColor: '#e4e4e7' },
  input: { flex: 1, borderWidth: 1, borderColor: '#e4e4e7', borderRadius: 24, paddingHorizontal: 16, paddingVertical: 10, fontSize: 14 },
  sendButton: { marginLeft: 8, backgroundColor: '#8b5cf6', borderRadius: 24, paddingHorizontal: 20, paddingVertical: 10, justifyContent: 'center' },
  sendText: { color: 'white', fontWeight: 'bold', fontSize: 14 },
  footer: { padding: 8, backgroundColor: '#18181b' },
  footerText: { fontSize: 10, color: '#a1a1aa', textAlign: 'center' }
});

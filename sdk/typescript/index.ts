/**
 * AI Agency OS TypeScript SDK
 * npm install ai-agency-sdk (mock - in production publish to NPM)
 */

type Agent = {
  id: string;
  name: string;
  description: string;
  category: string;
  icon: string;
};

type Skill = {
  id: string;
  name: string;
  description: string;
  category: string;
};

type ChatResponse = {
  response: string;
  conversation_id: string;
  agent_id?: string;
};

export class AIAgencyClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(config: { baseUrl?: string; apiKey?: string } = {}) {
    this.baseUrl = (config.baseUrl || 'http://localhost:8000').replace(/\/$/, '');
    this.apiKey = config.apiKey;
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> || {}),
    };
    
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const res = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`API Error ${res.status}: ${text}`);
    }

    return res.json();
  }

  // Agents
  async listAgents(category?: string): Promise<Agent[]> {
    const params = category ? `?category=${category}` : '';
    const data = await this.request<{ agents: Agent[] }>(`/api/agents/${params}`);
    return data.agents;
  }

  async getAgent(agentId: string): Promise<Agent> {
    return this.request<Agent>(`/api/agents/${agentId}`);
  }

  async runAgent(agentId: string, task: string, context?: Record<string, any>): Promise<any> {
    return this.request(`/api/agents/run`, {
      method: 'POST',
      body: JSON.stringify({ agent_id: agentId, task, context }),
    });
  }

  // Skills
  async listSkills(category?: string): Promise<Skill[]> {
    const params = category ? `?category=${category}` : '';
    const data = await this.request<{ skills: Skill[] }>(`/api/skills/${params}`);
    return data.skills;
  }

  async getSkill(skillId: string): Promise<Skill> {
    return this.request<Skill>(`/api/skills/${skillId}`);
  }

  // Chat
  async chat(message: string, conversationId?: string, agentId?: string): Promise<ChatResponse> {
    return this.request<ChatResponse>(`/api/chat/`, {
      method: 'POST',
      body: JSON.stringify({ message, conversation_id: conversationId, agent_id: agentId }),
    });
  }

  // Pipelines
  async listPipelines(): Promise<any[]> {
    const data = await this.request<{ pipelines: any[] }>(`/api/pipelines/`);
    return data.pipelines;
  }

  async runPipeline(pipelineId: string, input: Record<string, any>): Promise<any> {
    return this.request(`/api/pipelines/run`, {
      method: 'POST',
      body: JSON.stringify({ pipeline_id: pipelineId, input }),
    });
  }

  // Agency
  async listProjects(): Promise<any[]> {
    const data = await this.request<{ projects: any[] }>(`/api/agency/projects`);
    return data.projects;
  }

  async createProject(name: string, clientEmail: string, description?: string): Promise<any> {
    return this.request(`/api/agency/projects`, {
      method: 'POST',
      body: JSON.stringify({ name, client_email: clientEmail, description }),
    });
  }

  // Knowledge
  async searchKnowledge(query: string, collection?: string): Promise<any> {
    const params = new URLSearchParams({ query });
    if (collection) params.set('collection', collection);
    return this.request(`/api/knowledge/search?${params}`);
  }

  // Marketplace
  async searchMarketplace(query: string, type: string = 'all'): Promise<any> {
    return this.request(`/api/marketplace/search?q=${encodeURIComponent(query)}&type=${type}`);
  }

  // Realtime - WebSocket helper
  connectRealtime(room: string = 'general', userId?: string, onMessage?: (data: any) => void): WebSocket {
    const protocol = this.baseUrl.startsWith('https') ? 'wss:' : 'ws:';
    const host = this.baseUrl.replace(/^https?:\/\//, '');
    const url = `${protocol}//${host}/api/realtime/ws/${room}${userId ? `?user_id=${userId}` : ''}`;
    
    const ws = new WebSocket(url);
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage?.(data);
      } catch {
        onMessage?.({ type: 'message', text: event.data });
      }
    };

    return ws;
  }
}

// Example usage:
/*
import { AIAgencyClient } from 'ai-agency-sdk';

const client = new AIAgencyClient({
  baseUrl: 'https://your-agency.os',
  apiKey: 'your-api-key'
});

// List agents
const agents = await client.listAgents();
console.log(`Found ${agents.length} agents`);

// Run an agent
const result = await client.runAgent('backend-dev', 'Build a REST API for todos');

// Chat
const chat = await client.chat('Build me a landing page');
console.log(chat.response);

// Realtime
const ws = client.connectRealtime('project-123', 'user-456', (data) => {
  console.log('Realtime:', data);
});
*/

export default AIAgencyClient;

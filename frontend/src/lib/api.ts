import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add user_id header for demo (in production use auth)
api.interceptors.request.use(config => {
  config.params = {
    ...config.params,
    user_id: 'default-user'
  };
  return config;
});

export default api;

// API helpers
export const chatApi = {
  list: () => api.get('/chats/').then(r => r.data),
  create: (data: any) => api.post('/chats/', data).then(r => r.data),
  get: (id: string) => api.get(`/chats/${id}`).then(r => r.data),
  delete: (id: string) => api.delete(`/chats/${id}`).then(r => r.data),
  completion: (data: any) => api.post('/chats/completions', data).then(r => r.data),
  models: () => api.get('/chats/models/list').then(r => r.data),
};

export const agentsApi = {
  list: (category?: string) => api.get('/agents/', { params: { category } }).then(r => r.data),
  get: (id: string) => api.get(`/agents/${id}`).then(r => r.data),
  run: (data: any) => api.post('/agents/run', data).then(r => r.data),
  workflows: () => api.get('/agents/workflows/list').then(r => r.data),
  runWorkflow: (data: any) => api.post('/agents/workflow/run', data).then(r => r.data),
};

export const skillsApi = {
  list: (category?: string) => api.get('/skills/', { params: { category } }).then(r => r.data),
  get: (id: string) => api.get(`/skills/${id}`).then(r => r.data),
  search: (q: string) => api.get(`/skills/search/${q}`).then(r => r.data),
};

export const memoryApi = {
  list: (type?: string) => api.get('/memory/', { params: { type } }).then(r => r.data),
  search: (q: string) => api.get('/memory/search', { params: { q } }).then(r => r.data),
  instincts: () => api.get('/memory/instincts/').then(r => r.data),
};

export const toolsApi = {
  list: () => api.get('/tools/').then(r => r.data),
  execute: (data: any) => api.post('/tools/execute', data).then(r => r.data),
};

export const functionsApi = {
  list: (type?: string) => api.get('/functions/', { params: { type } }).then(r => r.data),
};

export const pipelinesApi = {
  list: () => api.get('/pipelines/').then(r => r.data),
  get: (id: string) => api.get(`/pipelines/${id}`).then(r => r.data),
  execute: (id: string, context: any) => api.post(`/pipelines/${id}/execute`, { context }).then(r => r.data),
  history: () => api.get('/pipelines/history/list').then(r => r.data),
};

export const agencyApi = {
  dashboard: () => api.get('/agency/dashboard').then(r => r.data),
  clients: () => api.get('/agency/clients').then(r => r.data),
  createClient: (data: any) => api.post('/agency/clients', data).then(r => r.data),
  getClient: (id: string) => api.get(`/agency/clients/${id}`).then(r => r.data),
  projects: (clientId?: string) => api.get('/agency/projects', { params: { client_id: clientId } }).then(r => r.data),
  createProject: (data: any) => api.post('/agency/projects', data).then(r => r.data),
  getProject: (id: string) => api.get(`/agency/projects/${id}`).then(r => r.data),
  tasks: (projectId?: string) => api.get('/agency/tasks', { params: { project_id: projectId } }).then(r => r.data),
  createTask: (data: any) => api.post('/agency/tasks', data).then(r => r.data),
  updateTask: (id: string, data: any) => api.put(`/agency/tasks/${id}`, data).then(r => r.data),
  securityAudit: () => api.get('/agency/security/audit').then(r => r.data),
  verify: (data: any) => api.post('/agency/verify', null, { params: data }).then(r => r.data),
};

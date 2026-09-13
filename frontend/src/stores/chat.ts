import { create } from 'zustand';

interface Message {
  id: string;
  role: string;
  content: string;
  created_at?: string;
}

interface ChatState {
  chats: any[];
  currentChat: any | null;
  messages: Message[];
  selectedAgent: string | null;
  selectedModel: string;
  isLoading: boolean;
  setChats: (chats: any[]) => void;
  setCurrentChat: (chat: any) => void;
  setMessages: (messages: Message[]) => void;
  addMessage: (msg: Message) => void;
  setSelectedAgent: (agentId: string | null) => void;
  setSelectedModel: (model: string) => void;
  setIsLoading: (loading: boolean) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  chats: [],
  currentChat: null,
  messages: [],
  selectedAgent: null,
  selectedModel: 'gpt-4o-mini',
  isLoading: false,
  setChats: (chats) => set({ chats }),
  setCurrentChat: (chat) => set({ currentChat: chat }),
  setMessages: (messages) => set({ messages }),
  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  setSelectedAgent: (agentId) => set({ selectedAgent: agentId }),
  setSelectedModel: (model) => set({ selectedModel: model }),
  setIsLoading: (loading) => set({ isLoading: loading }),
}));

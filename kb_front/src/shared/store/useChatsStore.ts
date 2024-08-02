import { create } from "zustand";

interface Chat {
  id: string;
  isAiResponse: boolean;
  content: string;
  createdAt: Date;
}

interface ChatsStore {
  chats: Chat[];
  setChats: (chats: Chat[]) => void;
  addChat: (chat: Chat) => void;
}

export const useChatsStore = create<ChatsStore>((set) => ({
  chats: [],
  setChats: (chats) => set({ chats }),
  addChat: (chat) => set((state) => ({ chats: [...state.chats, chat] })),
}));

export const notYetRendered = [];

export function isNotYetRenderedChat(id) {
  const isNotYetRendered = notYetRendered.includes(id);
  if (isNotYetRendered) {
    notYetRendered.splice(notYetRendered.indexOf(id), 1);
  }
  return isNotYetRendered;
}

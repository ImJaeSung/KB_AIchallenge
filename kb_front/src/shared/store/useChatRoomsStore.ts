import { create } from "zustand";

interface ChatRoom {
  id: string;
  createdAt: Date;
}

interface ChatRoomsStore {
  chatRooms: ChatRoom[];
  setChatRooms: (chatRooms: ChatRoom[]) => void;
  addChatRoom: (chatRoom: ChatRoom) => void;
}

export const useChatRoomsStore = create<ChatRoomsStore>((set) => ({
  chatRooms: [],
  setChatRooms: (chatRooms) => set({ chatRooms }),
  addChatRoom: (chatRoom) =>
    set((state) => ({ chatRooms: [...state.chatRooms, chatRoom] })),
}));

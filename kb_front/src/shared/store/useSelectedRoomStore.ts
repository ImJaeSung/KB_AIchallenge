import { create } from "zustand";

interface SelectedRoomStore {
  selectedRoomId: string | null;
  setSelectedRoom: (selectedRoom: string) => void;
}

export const useSelectedRoomStore = create<SelectedRoomStore>((set) => ({
  selectedRoomId: null,
  setSelectedRoom: (selectedRoomId) => set({ selectedRoomId }),
}));

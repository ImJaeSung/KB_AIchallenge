import { create } from "zustand";

interface Member {
  id: string;
  email: string;
}

interface MemberStore {
  member: Member;
  isLoading: boolean;
  setMember: (member: Member) => void;
  setIsLoading: (isLoading: boolean) => void;
}

export const useMemberStore = create<MemberStore>((set) => ({
  member: null,
  isLoading: true,
  setMember: (member) => set({ member }),
  setIsLoading: (isLoading) => set({ isLoading }),
}));

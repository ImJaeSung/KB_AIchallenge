import { create } from "zustand";

interface Member {
  id: number;
  email: string;
}

interface MemberStore {
  member: Member;
  setMember: (member: Member) => void;
}

export const useMemberStore = create<MemberStore>((set) => ({
  member: null,
  setMember: (member) => set({ member }),
}));

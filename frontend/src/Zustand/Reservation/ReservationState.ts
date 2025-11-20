import { create } from "zustand";

interface ReservationFormState {
  date: string;
  time: string;
  guests: number;
  tableId: number | null;
  specialRequests: string;
  currentStep: number;
  setDate: (date: string) => void;
  setTime: (time: string) => void;
  setGuests: (guests: number) => void;
  setTableId: (tableId: number | null) => void;
  setSpecialRequests: (requests: string) => void;
  setCurrentStep: (step: number) => void;
  nextStep: () => void;
  prevStep: () => void;
  resetForm: () => void;
}

export const useReservationFormStore = create<ReservationFormState>((set) => ({
  date: "",
  time: "",
  guests: 2,
  tableId: null,
  specialRequests: "",
  currentStep: 1,

  setDate: (date) => set({ date }),
  setTime: (time) => set({ time }),
  setGuests: (guests) => set({ guests }),
  setTableId: (tableId) => set({ tableId }),
  setSpecialRequests: (specialRequests) => set({ specialRequests }),
  setCurrentStep: (currentStep) => set({ currentStep }),

  nextStep: () => set((state) => ({
    currentStep: Math.min(state.currentStep + 1, 4)
  })),

  prevStep: () => set((state) => ({
    currentStep: Math.max(state.currentStep - 1, 1)
  })),

  resetForm: () => set({
    date: "",
    time: "",
    guests: 2,
    tableId: null,
    specialRequests: "",
    currentStep: 1,
  }),
}));
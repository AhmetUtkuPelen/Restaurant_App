import { create } from "zustand";

export interface PaymentCard {
  cardNumber: string;
  expiryMonth: string;
  expiryYear: string;
  cvc: string;
  cardHolderName: string;
}

export interface BillingAddress {
  contactName: string;
  city: string;
  country: string;
  address: string;
  zipCode: string;
}

export interface PaymentData {
  card: PaymentCard;
  billingAddress: BillingAddress;
  amount: number;
  orderId?: number;
  reservationId?: number;
  paymentType: "cart" | "reservation";
}

export interface Payment {
  id: number;
  amount: number;
  status: "pending" | "completed" | "failed" | "refunded";
  payment_method: string;
  transaction_id?: string;
  order_id?: number;
  reservation_id?: number;
  created_at: string;
}

interface PaymentState {
  currentPayment: PaymentData | null;
  payments: Payment[];
  isProcessing: boolean;
  
  // Actions
  setPaymentData: (data: PaymentData) => void;
  setProcessing: (processing: boolean) => void;
  addPayment: (payment: Payment) => void;
  clearCurrentPayment: () => void;
  updatePaymentStatus: (paymentId: number, status: Payment["status"]) => void;
}

export const usePaymentStore = create<PaymentState>()((set) => ({
  currentPayment: null,
  payments: [],
  isProcessing: false,

  setPaymentData: (data: PaymentData) => {
    set({ currentPayment: data });
  },

  setProcessing: (processing: boolean) => {
    set({ isProcessing: processing });
  },

  addPayment: (payment: Payment) => {
    set((state) => ({
      payments: [payment, ...state.payments],
    }));
  },

  clearCurrentPayment: () => {
    set({ currentPayment: null });
  },

  updatePaymentStatus: (paymentId: number, status: Payment["status"]) => {
    set((state) => ({
      payments: state.payments.map((payment) =>
        payment.id === paymentId ? { ...payment, status } : payment
      ),
    }));
  },
}));
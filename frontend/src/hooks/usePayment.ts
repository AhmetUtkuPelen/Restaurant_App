/* eslint-disable @typescript-eslint/no-explicit-any */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";
import { usePaymentStore } from "@/Zustand/Payment/PaymentState";


export interface CreatePaymentRequest {
  order_ids?: number[];
  reservation_id?: number;
  amount: number;
  currency?: string;
  installment?: number;
  ip_address: string;
  metadata?: any;
}

export interface PaymentResponse {
  id: number;
  amount: number;
  status: "pending" | "completed" | "failed" | "refunded";
  payment_method: string;
  transaction_id?: string;
  order_id?: number;
  reservation_id?: number;
  created_at: string;
  iyzico_response?: any;
}

// Create payment \\
export const useCreatePayment = () => {
  const queryClient = useQueryClient();
  const { addPayment, setProcessing, clearCurrentPayment } = usePaymentStore();

  return useMutation({
    mutationFn: async (data: CreatePaymentRequest) => {
      setProcessing(true);
      const response = await axiosInstance.post<PaymentResponse>("/payments", data);
      return response.data;
    },
    onSuccess: (payment) => {
      addPayment(payment);
      clearCurrentPayment();
      queryClient.invalidateQueries({ queryKey: ["payments"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
    onError: () => {
      setProcessing(false);
    },
    onSettled: () => {
      setProcessing(false);
    },
  });
};

// Get user payments \\
export const useMyPayments = () => {
  return useQuery({
    queryKey: ["payments", "my"],
    queryFn: async () => {
      const response = await axiosInstance.get<PaymentResponse[]>("/payments/my-payments");
      return response.data;
    },
  });
};

// Get single payment \\
export const usePayment = (paymentId: number) => {
  return useQuery({
    queryKey: ["payments", paymentId],
    queryFn: async () => {
      const response = await axiosInstance.get<PaymentResponse>(`/payments/${paymentId}`);
      return response.data;
    },
    enabled: !!paymentId,
  });
};

// Refund payment \\
export const useRefundPayment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (paymentId: number) => {
      const response = await axiosInstance.post(`/payments/${paymentId}/refund`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["payments"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";
import { useOrderStore } from "@/Zustand/Order/OrderState";
import type { Order } from "@/Zustand/Order/OrderState";

// Types
export interface CreateOrderRequest {
  delivery_address?: string;
  special_instructions?: string;
}

export interface OrderResponse {
  message: string;
  order: {
    id: number;
    user_id: number;
    total_amount: number;
    status: "pending" | "completed" | "cancelled";
    delivery_address?: string;
    special_instructions?: string;
    created_at: string;
    updated_at?: string;
    completed_at?: string;
    order_items: Array<{
      id: number;
      order_id: number;
      product_id: number;
      quantity: number;
      unit_price: number;
      subtotal: number;
      created_at: string;
    }>;
  };
}

// Create order
export const useCreateOrder = () => {
  const queryClient = useQueryClient();
  const { addOrder, clearCurrentOrder } = useOrderStore();

  return useMutation({
    mutationFn: async (data: CreateOrderRequest) => {
      const response = await axiosInstance.post<OrderResponse>("/orders", data);
      return response.data;
    },
    onSuccess: (response) => {
      // Convert backend response to Order format for store
      const order: Order = {
        id: response.order.id,
        items: [], // Items will be fetched separately if needed
        total_amount: response.order.total_amount,
        status: response.order.status,
        created_at: response.order.created_at,
      };
      addOrder(order);
      clearCurrentOrder();
      queryClient.invalidateQueries({ queryKey: ["orders"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};

// Get user orders
export const useMyOrders = () => {
  return useQuery({
    queryKey: ["orders", "my"],
    queryFn: async () => {
      const response = await axiosInstance.get<{
        total: number;
        skip: number;
        limit: number;
        orders: Array<{
          id: number;
          user_id: number;
          status: string;
          total_amount: number;
          delivery_address?: string;
          special_instructions?: string;
          created_at: string;
          updated_at?: string;
          completed_at?: string;
          items_count: number;
        }>;
      }>("/orders/my-orders");
      return response.data;
    },
  });
};

// Get single order
export const useOrder = (orderId: number) => {
  return useQuery({
    queryKey: ["orders", orderId],
    queryFn: async () => {
      const response = await axiosInstance.get<OrderResponse>(`/orders/${orderId}`);
      return response.data;
    },
    enabled: !!orderId,
  });
};

// Update order status
export const useUpdateOrderStatus = () => {
  const queryClient = useQueryClient();
  const { updateOrderStatus } = useOrderStore();

  return useMutation({
    mutationFn: async ({ orderId, status }: { orderId: number; status: Order["status"] }) => {
      const response = await axiosInstance.patch(`/orders/${orderId}/status`, { status });
      return response.data;
    },
    onSuccess: (_, { orderId, status }) => {
      updateOrderStatus(orderId, status);
      queryClient.invalidateQueries({ queryKey: ["orders"] });
    },
  });
};
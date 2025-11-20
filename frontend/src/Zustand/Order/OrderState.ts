import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface OrderItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  image_url: string;
  category: string;
}

export interface Order {
  id?: number;
  items: OrderItem[];
  total_amount: number;
  status: "pending" | "completed" | "cancelled";
  payment_id?: number;
  reservation_id?: number;
  created_at?: string;
}

interface OrderState {
  currentOrder: Order | null;
  orders: Order[];

  // Actions
  createOrder: (items: OrderItem[], reservationId?: number) => void;
  updateOrderStatus: (orderId: number, status: Order["status"]) => void;
  clearCurrentOrder: () => void;
  addOrder: (order: Order) => void;
}

export const useOrderStore = create<OrderState>()(
  persist(
    (set) => ({
      currentOrder: null,
      orders: [],

      createOrder: (items: OrderItem[], reservationId?: number) => {
        const total = items.reduce(
          (sum, item) => sum + item.price * item.quantity,
          0
        );

        const newOrder: Order = {
          items,
          total_amount: total,
          status: "pending",
          reservation_id: reservationId,
        };

        set({ currentOrder: newOrder });
      },

      updateOrderStatus: (orderId: number, status: Order["status"]) => {
        set((state) => ({
          orders: state.orders.map((order) =>
            order.id === orderId ? { ...order, status } : order
          ),
          currentOrder:
            state.currentOrder?.id === orderId
              ? { ...state.currentOrder, status }
              : state.currentOrder,
        }));
      },

      clearCurrentOrder: () => {
        set({ currentOrder: null });
      },

      addOrder: (order: Order) => {
        set((state) => ({
          orders: [order, ...state.orders],
        }));
      },
    }),
    {
      name: "order-storage",
    }
  )
);
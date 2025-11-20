import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface CartItem {
  id: number;
  name: string;
  price: string;
  final_price: string;
  image_url: string;
  category: string;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addToCart: (product: Omit<CartItem, "quantity">, quantity?: number) => void;
  removeFromCart: (productId: number) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  clearCart: () => void;
  getTotalItems: () => number;
  getTotalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addToCart: (product, quantity = 1) => {
        set((state) => {
          const existingItem = state.items.find(
            (item) => item.id === product.id
          );

          if (existingItem) {
            return {
              items: state.items.map((item) =>
                item.id === product.id
                  ? { ...item, quantity: item.quantity + quantity }
                  : item
              ),
            };
          }

          // Add new item \\
          return {
            items: [...state.items, { ...product, quantity }],
          };
        });
      },

      removeFromCart: (productId) => {
        set((state) => ({
          items: state.items.filter((item) => item.id !== productId),
        }));
      },

      updateQuantity: (productId, quantity) => {
        if (quantity <= 0) {
          get().removeFromCart(productId);
          return;
        }

        set((state) => ({
          items: state.items.map((item) =>
            item.id === productId ? { ...item, quantity } : item
          ),
        }));
      },

      clearCart: () => {
        set({ items: [] });
      },

      getTotalItems: () => {
        return get().items.reduce((total, item) => total + item.quantity, 0);
      },

      getTotalPrice: () => {
        return get().items.reduce(
          (total, item) =>
            total + parseFloat(item.final_price || item.price) * item.quantity,
          0
        );
      },
    }),
    {
      name: "cart-storage", // localStorage key
      partialize: (state) => ({ items: state.items }),
    }
  )
);

if (typeof window !== "undefined") {
  import("../Auth/AuthState").then(({ useAuthStore }) => {
    let previousAuth = useAuthStore.getState().isAuthenticated;
    let previousUserId = useAuthStore.getState().user?.id;

    useAuthStore.subscribe((state) => {
      const currentAuth = state.isAuthenticated;
      const currentUserId = state.user?.id;

      // Clear cart when user logs out \\
      if (previousAuth && !currentAuth) {
        useCartStore.getState().clearCart();
      }

      // Clear cart when switching users \\
      if (previousUserId && currentUserId && previousUserId !== currentUserId) {
        useCartStore.getState().clearCart();
      }

      previousAuth = currentAuth;
      previousUserId = currentUserId;
    });
  });
}
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { UserRole } from "../../Types/User/UserTypes";

// Define the shape of the user object
export interface User {
  id: number;
  username: string;
  email: string;
  role: UserRole;
  phone?: string | null;
  image_url?: string | null;
  address: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  deleted_at?: string | null;
}

// Define the shape of the auth state
export interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: {
    username: string;
    email: string;
    password: string;
    phone?: string;
    address: string;
    image_url?: string;
  }) => Promise<void>;
  logout: () => void;
  refreshAccessToken: () => Promise<boolean>;
  updateUser: (userData: Partial<User>) => void;
  clearError: () => void;
}

// Create the store with persistence
export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (username: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(
            `${import.meta.env.VITE_API_URL}/users/login`,
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ username, password }),
            }
          );

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Login failed");
          }

          const { access_token, refresh_token, user } = await response.json();

          set({
            user,
            accessToken: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : "Login failed",
            isLoading: false,
          });
          throw error;
        }
      },

      register: async (userData) => {
        set({ isLoading: true, error: null });
        try {
          const response = await fetch(
            `${import.meta.env.VITE_API_URL}/users/register`,
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(userData),
            }
          );

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Registration failed");
          }

          // Backend doesn't return tokens on registration, just success message
          // User needs to login after registration
          await response.json(); // Consume the response

          set({
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            error:
              error instanceof Error ? error.message : "Registration failed",
            isLoading: false,
          });
          throw error;
        }
      },

      logout: () => {
        // Call your logout API if needed
        // await fetch('/api/auth/logout', { method: 'POST' });

        // Clear the state
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
        });
      },

      refreshAccessToken: async (): Promise<boolean> => {
        const { refreshToken } = get();
        if (!refreshToken) return false;

        try {
          const response = await fetch(
            `${import.meta.env.VITE_API_URL}/users/refresh`,
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ refresh_token: refreshToken }),
            }
          );

          if (!response.ok) {
            throw new Error("Failed to refresh token");
          }

          const { access_token, refresh_token } = await response.json();

          set({
            accessToken: access_token,
            refreshToken: refresh_token || refreshToken,
          });

          return true;
        } catch (error) {
          // If refresh fails, log the user out
          console.error("Failed to refresh access token:", error);
          get().logout();
          return false;
        }
      },

      updateUser: (userData: Partial<User>) => {
        set((state) => ({
          user: state.user ? { ...state.user, ...userData } : null,
        }));
      },

      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: "auth-storage", // name of the item in the storage (must be unique)
      storage: createJSONStorage(() => localStorage), // (optional) by default, 'localStorage' is used
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// Export hooks for convenience
export const useUser = () => useAuthStore((state) => state.user);
export const useIsAuthenticated = () =>
  useAuthStore((state) => state.isAuthenticated);
export const useIsAdmin = () => {
  const user = useAuthStore((state) => state.user);
  return user?.role === "ADMIN";
};

export const useIsStaff = () => {
  const user = useAuthStore((state) => state.user);
  return user?.role === "STAFF";
};

export const useIsStaffOrAdmin = () => {
  const user = useAuthStore((state) => state.user);
  return user?.role === "ADMIN" || user?.role === "STAFF";
};

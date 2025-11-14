import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type{ UserRole } from '../../Types/User/UserTypes';

// Define the shape of the user object
export interface User {
  id: number;
  username: string;
  email: string;
  role: UserRole;
  phone?: string | null;
  profile_picture?: string | null;
  address: string;
  is_active: boolean;
  is_verified: boolean;
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
  login: (email: string, password: string) => Promise<void>;
  register: (userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    phone: string;
    address: string;
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

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          // Replace with your actual API call
          const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Login failed');
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
            error: error instanceof Error ? error.message : 'Login failed',
            isLoading: false,
          });
          throw error;
        }
      },

      register: async (userData) => {
        set({ isLoading: true, error: null });
        try {
          // Replace with your actual API call
          const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Registration failed');
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
            error: error instanceof Error ? error.message : 'Registration failed',
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
          const response = await fetch('/api/auth/refresh-token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_token: refreshToken }),
          });

          if (!response.ok) {
            throw new Error('Failed to refresh token');
          }

          const { access_token, refresh_token } = await response.json();
          
          set({
            accessToken: access_token,
            refreshToken: refresh_token || refreshToken,
          });
          
          return true;
        } catch (error) {
          // If refresh fails, log the user out
          console.error('Failed to refresh access token:', error);
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
      name: 'auth-storage', // name of the item in the storage (must be unique)
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
export const useIsAuthenticated = () => useAuthStore((state) => state.isAuthenticated);
export const useIsAdmin = () => {
  const user = useAuthStore((state) => state.user);
  return user?.role === 'admin';
};
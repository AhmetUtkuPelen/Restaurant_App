'use client';

import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { User, AuthState } from '@/types';
import { api } from '@/lib/api';

interface AuthContextType extends AuthState {
  login: (credentials: { username_or_email: string; password: string }) => Promise<void>;
  register: (userData: { username: string; email: string; password: string; display_name?: string }) => Promise<void>;
  logout: () => void;
  updateUser: (userData: { display_name?: string; bio?: string; avatar_url?: string }) => Promise<void>;
  updatePassword: (passwordData: { current_password: string; new_password: string }) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

type AuthAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_USER'; payload: User }
  | { type: 'SET_TOKEN'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: Partial<User> };

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
      };
    case 'SET_TOKEN':
      return { ...state, token: action.payload };
    case 'UPDATE_USER':
      return {
        ...state,
        user: state.user ? { ...state.user, ...action.payload } : null,
      };
    case 'LOGOUT':
      return {
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
      };
    default:
      return state;
  }
};

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
};

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');

        if (token && userData) {
          dispatch({ type: 'SET_TOKEN', payload: token });
          
          try {
            // Verify token is still valid by fetching current user
            const user = await api.getCurrentUser();
            dispatch({ type: 'SET_USER', payload: user });
          } catch (error) {
            // Token is invalid, clear storage
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            dispatch({ type: 'LOGOUT' });
          }
        } else {
          dispatch({ type: 'SET_LOADING', payload: false });
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    initializeAuth();
  }, []);

  const login = async (credentials: { username_or_email: string; password: string }) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      const response = await api.login(credentials);
      
      // Store token and user data
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      dispatch({ type: 'SET_TOKEN', payload: response.token });
      dispatch({ type: 'SET_USER', payload: response.user });
    } catch (error) {
      dispatch({ type: 'SET_LOADING', payload: false });
      throw error;
    }
  };

  const register = async (userData: { username: string; email: string; password: string; display_name?: string }) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      const response = await api.register(userData);
      
      // Store token and user data
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      
      dispatch({ type: 'SET_TOKEN', payload: response.token });
      dispatch({ type: 'SET_USER', payload: response.user });
    } catch (error) {
      dispatch({ type: 'SET_LOADING', payload: false });
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    dispatch({ type: 'LOGOUT' });
  };

  const updateUser = async (userData: { display_name?: string; bio?: string; avatar_url?: string }) => {
    if (!state.user) throw new Error('No user logged in');
    
    try {
      const updatedUser = await api.updateUser(state.user.id, userData);
      
      // Update localStorage
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      dispatch({ type: 'UPDATE_USER', payload: userData });
    } catch (error) {
      throw error;
    }
  };

  const updatePassword = async (passwordData: { current_password: string; new_password: string }) => {
    if (!state.user) throw new Error('No user logged in');
    
    try {
      await api.updatePassword(state.user.id, passwordData);
    } catch (error) {
      throw error;
    }
  };

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    updateUser,
    updatePassword,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

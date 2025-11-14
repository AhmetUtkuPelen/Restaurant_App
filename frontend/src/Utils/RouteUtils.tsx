import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useIsAuthenticated, useIsAdmin } from '../Zustand/Auth/AuthState';

// Public Route - Accessible to everyone
export const PublicRoute = ({ children }: { children: ReactNode }) => {
  return <>{children}</>;
};

// Protected Route - Only for authenticated users
export const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const isAuthenticated = useIsAuthenticated();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

// Admin Route - Only for admin users
export const AdminRoute = ({ children }: { children: ReactNode }) => {
  const isAuthenticated = useIsAuthenticated();
  const isAdmin = useIsAdmin();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};

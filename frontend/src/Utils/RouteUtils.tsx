import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import {
  useAuthStore,
  useIsAuthenticated,
  useIsAdmin,
} from "../Zustand/Auth/AuthState";
import { Spinner } from "@/Components/ui/spinner";

// Open Route \\
export const OpenRoute = ({ children }: { children: ReactNode }) => {
  return <>{children}</>;
};

// Authenticated Route \\
export const AuthenticatedRoute = ({ children }: { children: ReactNode }) => {
  const isAuthenticated = useIsAuthenticated();
  const { isLoading } = useAuthStore();
  const location = useLocation();

  if (isLoading) {
    return <Spinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

// Admin Route \\
export const AdminRoute = ({ children }: { children: ReactNode }) => {
  const isAuthenticated = useIsAuthenticated();
  const isAdmin = useIsAdmin();
  const { isLoading } = useAuthStore();
  const location = useLocation();

  if (isLoading) {
    return <Spinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (!isAdmin) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="text-6xl text-red-400 mb-4">🚫</div>
          <h1 className="text-2xl font-bold text-white mb-2">Access Denied</h1>
          <p className="text-gray-400 mb-4">
            You don't have permission to access this page.
          </p>
          <button
            onClick={() => window.history.back()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};
'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { Eye, EyeOff, LogIn, Mail, Lock } from 'lucide-react';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    username_or_email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { login } = useAuth();
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login(formData);
      
      // Get redirect URL from query params or default to chat
      const urlParams = new URLSearchParams(window.location.search);
      const redirect = urlParams.get('redirect') || '/chat';
      
      router.push(redirect);
    } catch (err: any) {
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-base-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-base-content">
            Welcome back
          </h2>
          <p className="mt-2 text-sm text-base-content/70">
            Sign in to your account to continue chatting
          </p>
        </div>

        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <form className="space-y-6" onSubmit={handleSubmit}>
              {error && (
                <div className="alert alert-error">
                  <span>{error}</span>
                </div>
              )}

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Email or Username</span>
                </label>
                <div className="relative">
                  <input
                    type="text"
                    name="username_or_email"
                    value={formData.username_or_email}
                    onChange={handleChange}
                    className="input input-bordered w-full pl-10"
                    placeholder="Enter your email or username"
                    required
                  />
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50" size={18} />
                </div>
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Password</span>
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="input input-bordered w-full pl-10 pr-10"
                    placeholder="Enter your password"
                    required
                  />
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50" size={18} />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-base-content/50 hover:text-base-content"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <label className="label cursor-pointer">
                  <input type="checkbox" className="checkbox checkbox-sm" />
                  <span className="label-text ml-2">Remember me</span>
                </label>
                <Link href="/forgot-password" className="link link-primary text-sm">
                  Forgot password?
                </Link>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="btn btn-primary w-full"
              >
                {isLoading ? (
                  <span className="loading loading-spinner loading-sm"></span>
                ) : (
                  <>
                    <LogIn size={18} />
                    Sign In
                  </>
                )}
              </button>
            </form>

            <div className="divider">OR</div>

            <div className="text-center">
              <p className="text-sm text-base-content/70">
                Don't have an account?{' '}
                <Link href="/register" className="link link-primary">
                  Sign up here
                </Link>
              </p>
            </div>
          </div>
        </div>

        <div className="text-center">
          <Link href="/" className="link link-neutral text-sm">
            ← Back to home
          </Link>
        </div>
      </div>
    </div>
  );
}

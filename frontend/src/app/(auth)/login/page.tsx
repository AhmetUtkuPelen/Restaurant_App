'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { LogIn, Mail, Lock } from 'lucide-react';
import { useFormValidation } from '@/hooks/useFormValidation';
import { ValidatedInput } from '@/components/ui/ValidatedInput';

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [serverError, setServerError] = useState('');

  const { login } = useAuth();
  const router = useRouter();

  // Form validation setup
  const {
    formData,
    setFieldValue,
    validateForm,
    touchAllFields,
    setFieldError
  } = useFormValidation(
    {
      username_or_email: '',
      password: '',
    },
    {
      username_or_email: [{ required: true, minLength: 3 }],
      password: [{ required: true, minLength: 1 }],
    }
  );

  const handleFieldChange = (name: string, value: string) => {
    setFieldValue(name as keyof typeof formData, value);
    // Clear server error when user starts typing
    if (serverError) setServerError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Touch all fields to show validation errors
    touchAllFields();
    
    // Validate form
    const validationResult = await validateForm();
    if (!validationResult.isValid) {
      return;
    }

    setIsLoading(true);
    setServerError('');

    try {
      await login(formData);
      
      // Get redirect URL from query params or default to chat
      const urlParams = new URLSearchParams(window.location.search);
      const redirect = urlParams.get('redirect') || '/chat';
      
      router.push(redirect);
    } catch (err: unknown) {
      console.error('Login error:', err);
      
      // Handle specific field errors from server
      const error = err as { response?: { data?: { field_errors?: Record<string, string>; detail?: string } }; message?: string };
      const errorData = error.response?.data;
      if (errorData?.field_errors) {
        Object.entries(errorData.field_errors).forEach(([field, message]) => {
          setFieldError(field as keyof typeof formData, message as string);
        });
      } else {
        setServerError(errorData?.detail || error.message || 'Login failed. Please try again.');
      }
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
              {serverError && (
                <div className="alert alert-error">
                  <span>{serverError}</span>
                </div>
              )}

              <ValidatedInput
                name="username_or_email"
                label="Email or Username"
                type="text"
                value={formData.username_or_email}
                onChange={handleFieldChange}
                validationRules={[{ required: true, minLength: 3 }]}
                placeholder="Enter your email or username"
                required
                icon={<Mail size={18} />}
              />

              <ValidatedInput
                name="password"
                label="Password"
                type="password"
                value={formData.password}
                onChange={handleFieldChange}
                validationRules={[{ required: true, minLength: 1 }]}
                placeholder="Enter your password"
                required
                icon={<Lock size={18} />}
                showValidationStatus={false}
              />

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
                Dont have an account?{' '}
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

'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { UserPlus, Mail, Lock, User } from 'lucide-react';
import { useFormValidation } from '@/hooks/useFormValidation';
import { ValidationRules } from '@/lib/validation';
import { ValidatedInput } from '@/components/ui/ValidatedInput';

export default function RegisterPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [serverError, setServerError] = useState('');

  const { register } = useAuth();
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
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      display_name: '',
    },
    {
      username: [ValidationRules.username()],
      email: [ValidationRules.email()],
      password: [ValidationRules.password()],
      confirmPassword: [ValidationRules.confirmPassword('password')],
      display_name: [ValidationRules.displayName()],
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
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        display_name: formData.display_name || undefined,
      });
      
      router.push('/chat');
    } catch (err: unknown) {
      console.error('Registration error:', err);
      
      // Handle specific field errors from server
      const error = err as { response?: { data?: { field_errors?: Record<string, string>; detail?: string } }; message?: string };
      const errorData = error.response?.data;
      if (errorData?.field_errors) {
        Object.entries(errorData.field_errors).forEach(([field, message]) => {
          setFieldError(field as keyof typeof formData, message as string);
        });
      } else {
        setServerError(errorData?.detail || error.message || 'Registration failed. Please try again.');
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
            Create your account
          </h2>
          <p className="mt-2 text-sm text-base-content/70">
            Join our community and start chatting
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
                name="username"
                label="Username"
                type="text"
                value={formData.username}
                onChange={handleFieldChange}
                validationRules={[ValidationRules.username()]}
                placeholder="Choose a username"
                required
                icon={<User size={18} />}
              />

              <ValidatedInput
                name="display_name"
                label="Display Name"
                type="text"
                value={formData.display_name}
                onChange={handleFieldChange}
                validationRules={[ValidationRules.displayName()]}
                placeholder="Your display name (optional)"
                icon={<User size={18} />}
              />

              <ValidatedInput
                name="email"
                label="Email"
                type="email"
                value={formData.email}
                onChange={handleFieldChange}
                validationRules={[ValidationRules.email()]}
                placeholder="Enter your email"
                required
                icon={<Mail size={18} />}
              />

              <ValidatedInput
                name="password"
                label="Password"
                type="password"
                value={formData.password}
                onChange={handleFieldChange}
                validationRules={[ValidationRules.password()]}
                placeholder="Create a password"
                required
                icon={<Lock size={18} />}
              />

              <ValidatedInput
                name="confirmPassword"
                label="Confirm Password"
                type="password"
                value={formData.confirmPassword}
                onChange={handleFieldChange}
                validationRules={[ValidationRules.confirmPassword('password')]}
                placeholder="Confirm your password"
                required
                icon={<Lock size={18} />}
                showValidationStatus={false}
              />

              <div className="form-control">
                <label className="label cursor-pointer justify-start">
                  <input type="checkbox" className="checkbox checkbox-sm" required />
                  <span className="label-text ml-2">
                    I agree to the{' '}
                    <Link href="/terms" className="link link-primary">
                      Terms of Service
                    </Link>{' '}
                    and{' '}
                    <Link href="/privacy" className="link link-primary">
                      Privacy Policy
                    </Link>
                  </span>
                </label>
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
                    <UserPlus size={18} />
                    Create Account
                  </>
                )}
              </button>
            </form>

            <div className="divider">OR</div>

            <div className="text-center">
              <p className="text-sm text-base-content/70">
                Already have an account?{' '}
                <Link href="/login" className="link link-primary">
                  Sign in here
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

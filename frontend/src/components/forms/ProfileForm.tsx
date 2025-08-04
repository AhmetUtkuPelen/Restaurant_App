/**
 * Profile Form Component
 * Example of comprehensive form validation usage
 */

import React, { useState, useEffect } from 'react';
import { User, Mail, FileText, Save, X } from 'lucide-react';
import { useFormValidation } from '@/hooks/useFormValidation';
import { ValidationRules } from '@/lib/validation';
import { ValidatedInput } from '@/components/ui/ValidatedInput';
import { FormErrorSummary } from '@/components/ui/ValidationError';
import { User as UserType } from '@/types';

interface ProfileFormProps {
  user: UserType;
  onSave: (data: ProfileFormData) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

interface ProfileFormData {
  display_name: string;
  bio: string;
  email: string;
  username: string;
}

export const ProfileForm: React.FC<ProfileFormProps> = ({
  user,
  onSave,
  onCancel,
  isLoading = false
}) => {
  const [serverError, setServerError] = useState('');
  const [showErrorSummary, setShowErrorSummary] = useState(false);

  // Form validation setup
  const {
    formData,
    errors,
    isValid,
    hasErrors,
    setFieldValue,
    validateForm,
    touchAllFields,
    setFieldError,
    resetForm
  } = useFormValidation(
    {
      display_name: user.display_name || '',
      bio: user.bio || '',
      email: user.email,
      username: user.username,
    },
    {
      display_name: [ValidationRules.displayName()],
      bio: [ValidationRules.bio()],
      email: [ValidationRules.email()],
      username: [ValidationRules.username()],
    }
  );

  // Reset form when user changes
  useEffect(() => {
    resetForm({
      display_name: user.display_name || '',
      bio: user.bio || '',
      email: user.email,
      username: user.username,
    });
  }, [user, resetForm]);

  const handleFieldChange = (name: string, value: string) => {
    setFieldValue(name as keyof ProfileFormData, value);
    // Clear server error when user starts typing
    if (serverError) setServerError('');
    if (showErrorSummary) setShowErrorSummary(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Touch all fields to show validation errors
    touchAllFields();
    
    // Validate form
    const validationResult = await validateForm();
    if (!validationResult.isValid) {
      setShowErrorSummary(true);
      return;
    }

    setServerError('');

    try {
      await onSave(formData);
    } catch (err: unknown) {
      console.error('Profile update error:', err);
      
      // Handle specific field errors from server
      const error = err as { response?: { data?: { field_errors?: Record<string, string>; detail?: string } }; message?: string };
      const errorData = error.response?.data;
      if (errorData?.field_errors) {
        Object.entries(errorData.field_errors).forEach(([field, message]) => {
          setFieldError(field as keyof ProfileFormData, message as string);
        });
        setShowErrorSummary(true);
      } else {
        setServerError(errorData?.detail || error.message || 'Failed to update profile. Please try again.');
      }
    }
  };

  const handleCancel = () => {
    resetForm();
    setServerError('');
    setShowErrorSummary(false);
    onCancel();
  };

  // Check if form has changes
  const hasChanges = 
    formData.display_name !== (user.display_name || '') ||
    formData.bio !== (user.bio || '') ||
    formData.email !== user.email ||
    formData.username !== user.username;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title mb-6">Edit Profile</h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Server error */}
            {serverError && (
              <div className="alert alert-error">
                <span>{serverError}</span>
              </div>
            )}

            {/* Error summary */}
            {showErrorSummary && hasErrors && (
              <FormErrorSummary
                errors={errors}
                fieldLabels={{
                  display_name: 'Display Name',
                  bio: 'Bio',
                  email: 'Email',
                  username: 'Username'
                }}
                dismissible
                onDismiss={() => setShowErrorSummary(false)}
              />
            )}

            {/* Form fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ValidatedInput
                name="username"
                label="Username"
                type="text"
                value={formData.username}
                onChange={handleFieldChange}
                validationRules={[ValidationRules.username()]}
                placeholder="Your unique username"
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
                placeholder="How others see your name"
                icon={<User size={18} />}
              />
            </div>

            <ValidatedInput
              name="email"
              label="Email Address"
              type="email"
              value={formData.email}
              onChange={handleFieldChange}
              validationRules={[ValidationRules.email()]}
              placeholder="Your email address"
              required
              icon={<Mail size={18} />}
            />

            <ValidatedInput
              name="bio"
              label="Bio"
              type="textarea"
              value={formData.bio}
              onChange={handleFieldChange}
              validationRules={[ValidationRules.bio()]}
              placeholder="Tell others about yourself..."
              rows={4}
              icon={<FileText size={18} />}
            />

            {/* Form actions */}
            <div className="flex justify-end gap-3 pt-4 border-t border-base-300">
              <button
                type="button"
                onClick={handleCancel}
                disabled={isLoading}
                className="btn btn-ghost"
              >
                <X size={18} />
                Cancel
              </button>
              
              <button
                type="submit"
                disabled={isLoading || !isValid || !hasChanges}
                className="btn btn-primary"
              >
                {isLoading ? (
                  <span className="loading loading-spinner loading-sm"></span>
                ) : (
                  <Save size={18} />
                )}
                Save Changes
              </button>
            </div>

            {/* Form status */}
            {hasChanges && (
              <div className="text-sm text-base-content/70 text-center">
                You have unsaved changes
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};
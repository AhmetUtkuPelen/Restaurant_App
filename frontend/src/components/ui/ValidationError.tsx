/**
 * Validation Error Display Components
 * Provides consistent error display for form validation
 */

import React from 'react';
import { AlertCircle, X } from 'lucide-react';

interface ValidationErrorProps {
  errors: string[];
  className?: string;
  showIcon?: boolean;
}

/**
 * Display validation errors for a single field
 */
export const ValidationError: React.FC<ValidationErrorProps> = ({ 
  errors, 
  className = '', 
  showIcon = true 
}) => {
  if (!errors || errors.length === 0) {
    return null;
  }

  return (
    <div className={`text-sm text-error mt-1 ${className}`}>
      {errors.map((error, index) => (
        <div key={index} className="flex items-start gap-1">
          {showIcon && <AlertCircle size={14} className="mt-0.5 flex-shrink-0" />}
          <span>{error}</span>
        </div>
      ))}
    </div>
  );
};

interface FieldErrorProps {
  error?: string;
  className?: string;
}

/**
 * Display a single error message for a field (simplified version)
 */
export const FieldError: React.FC<FieldErrorProps> = ({ error, className = '' }) => {
  if (!error) {
    return null;
  }

  return (
    <label className={`label ${className}`}>
      <span className="label-text-alt text-error flex items-center gap-1">
        <AlertCircle size={12} />
        {error}
      </span>
    </label>
  );
};

interface FormErrorSummaryProps {
  errors: { [fieldName: string]: string[] };
  fieldLabels?: { [fieldName: string]: string };
  className?: string;
  dismissible?: boolean;
  onDismiss?: () => void;
}

/**
 * Display a summary of all form errors
 */
export const FormErrorSummary: React.FC<FormErrorSummaryProps> = ({
  errors,
  fieldLabels = {},
  className = '',
  dismissible = false,
  onDismiss
}) => {
  const errorEntries = Object.entries(errors).filter(([_, fieldErrors]) => fieldErrors.length > 0);
  
  if (errorEntries.length === 0) {
    return null;
  }

  const totalErrors = errorEntries.reduce((sum, [_, fieldErrors]) => sum + fieldErrors.length, 0);

  return (
    <div className={`alert alert-error ${className}`}>
      <div className="flex-1">
        <div className="flex items-start gap-2">
          <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h4 className="font-semibold mb-2">
              Please fix the following {totalErrors === 1 ? 'error' : 'errors'}:
            </h4>
            <ul className="list-disc list-inside space-y-1">
              {errorEntries.map(([fieldName, fieldErrors]) => 
                fieldErrors.map((error, index) => (
                  <li key={`${fieldName}-${index}`} className="text-sm">
                    <strong>{fieldLabels[fieldName] || fieldName}:</strong> {error}
                  </li>
                ))
              )}
            </ul>
          </div>
        </div>
      </div>
      {dismissible && onDismiss && (
        <button
          onClick={onDismiss}
          className="btn btn-sm btn-ghost btn-square"
          aria-label="Dismiss errors"
        >
          <X size={16} />
        </button>
      )}
    </div>
  );
};

interface PasswordStrengthIndicatorProps {
  password: string;
  className?: string;
}

/**
 * Display password strength indicator
 */
export const PasswordStrengthIndicator: React.FC<PasswordStrengthIndicatorProps> = ({
  password,
  className = ''
}) => {
  const getPasswordStrength = (password: string) => {
    if (!password) {
      return { score: 0, label: 'No password', color: 'text-gray-400' };
    }

    let score = 0;
    
    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    
    // Character variety checks
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) score++;
    
    // Bonus for very long passwords
    if (password.length >= 16) score++;
    
    // Cap at 4
    score = Math.min(score, 4);

    const labels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const colors = ['text-red-500', 'text-orange-500', 'text-yellow-500', 'text-blue-500', 'text-green-500'];
    const bgColors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500'];

    return {
      score,
      label: labels[score],
      color: colors[score],
      bgColor: bgColors[score]
    };
  };

  const strength = getPasswordStrength(password);

  if (!password) {
    return null;
  }

  return (
    <div className={`mt-2 ${className}`}>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-base-content/70">Password strength:</span>
        <span className={`text-xs font-medium ${strength.color}`}>
          {strength.label}
        </span>
      </div>
      <div className="w-full bg-base-300 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all duration-300 ${strength.bgColor}`}
          style={{ width: `${(strength.score / 4) * 100}%` }}
        />
      </div>
    </div>
  );
};

interface ValidationStatusProps {
  isValid: boolean;
  isValidating?: boolean;
  validMessage?: string;
  className?: string;
}

/**
 * Display validation status (valid/invalid/validating)
 */
export const ValidationStatus: React.FC<ValidationStatusProps> = ({
  isValid,
  isValidating = false,
  validMessage = 'Looks good!',
  className = ''
}) => {
  if (isValidating) {
    return (
      <div className={`text-sm text-base-content/70 mt-1 ${className}`}>
        <div className="flex items-center gap-1">
          <span className="loading loading-spinner loading-xs"></span>
          <span>Validating...</span>
        </div>
      </div>
    );
  }

  if (isValid) {
    return (
      <div className={`text-sm text-success mt-1 ${className}`}>
        <div className="flex items-center gap-1">
          <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          <span>{validMessage}</span>
        </div>
      </div>
    );
  }

  return null;
};


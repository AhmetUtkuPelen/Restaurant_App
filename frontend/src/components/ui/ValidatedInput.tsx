/**
 * Validated Input Components
 * Provides form inputs with built-in validation and error display
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { FormValidator, ValidationRule, ValidationResult } from '@/lib/validation';
import { ValidationError, PasswordStrengthIndicator, ValidationStatus } from './ValidationError';

interface ValidatedInputProps {
  name: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'textarea';
  value: string;
  onChange: (name: string, value: string) => void;
  onValidation?: (name: string, result: ValidationResult) => void;
  validationRules?: ValidationRule[];
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  showValidationStatus?: boolean;
  validateOnChange?: boolean;
  validateOnBlur?: boolean;
  debounceMs?: number;
  rows?: number; // for textarea
  icon?: React.ReactNode;
}

/**
 * Input component with built-in validation
 */
export const ValidatedInput: React.FC<ValidatedInputProps> = ({
  name,
  label,
  type = 'text',
  value,
  onChange,
  onValidation,
  validationRules = [],
  placeholder,
  required = false,
  disabled = false,
  className = '',
  showValidationStatus = true,
  validateOnChange = true,
  validateOnBlur = true,
  debounceMs = 300,
  rows = 3,
  icon
}) => {
  const [errors, setErrors] = useState<string[]>([]);
  const [isValidating, setIsValidating] = useState(false);
  const [hasBeenBlurred, setHasBeenBlurred] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Debounced validation function
  const debouncedValidate = useCallback(
    FormValidator.createDebouncedValidator(
      (val: string) => FormValidator.validateField(val, validationRules),
      debounceMs
    ),
    [validationRules, debounceMs]
  );

  // Validate field
  const validateField = useCallback((val: string, immediate: boolean = false) => {
    if (validationRules.length === 0) return;

    if (immediate) {
      const result = FormValidator.validateField(val, validationRules);
      setErrors(result.errors);
      setIsValidating(false);
      onValidation?.(name, result);
    } else {
      setIsValidating(true);
      debouncedValidate(val, (result) => {
        setErrors(result.errors);
        setIsValidating(false);
        onValidation?.(name, result);
      });
    }
  }, [validationRules, name, onValidation, debouncedValidate]);

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    onChange(name, newValue);

    if (validateOnChange && (hasBeenBlurred || newValue.length > 0)) {
      validateField(newValue);
    }
  };

  // Handle input blur
  const handleBlur = () => {
    setHasBeenBlurred(true);
    if (validateOnBlur) {
      validateField(value, true);
    }
  };

  // Validate on mount if value exists
  useEffect(() => {
    if (value && validationRules.length > 0) {
      validateField(value, true);
    }
  }, []); // Only run on mount

  const isValid = errors.length === 0 && value.length > 0;
  const shouldShowErrors = hasBeenBlurred && errors.length > 0;
  const inputClassName = `input input-bordered w-full ${
    icon ? 'pl-10' : ''
  } ${type === 'password' ? 'pr-10' : ''} ${
    shouldShowErrors ? 'input-error' : isValid && showValidationStatus ? 'input-success' : ''
  } ${className}`;

  if (type === 'textarea') {
    return (
      <div className="form-control">
        <label className="label">
          <span className="label-text">
            {label}
            {required && <span className="text-error ml-1">*</span>}
          </span>
        </label>
        <textarea
          name={name}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          rows={rows}
          className={`textarea textarea-bordered w-full ${
            shouldShowErrors ? 'textarea-error' : isValid && showValidationStatus ? 'textarea-success' : ''
          } ${className}`}
        />
        {shouldShowErrors && <ValidationError errors={errors} />}
        {showValidationStatus && !shouldShowErrors && (
          <ValidationStatus 
            isValid={isValid} 
            isValidating={isValidating}
          />
        )}
      </div>
    );
  }

  return (
    <div className="form-control">
      <label className="label">
        <span className="label-text">
          {label}
          {required && <span className="text-error ml-1">*</span>}
        </span>
      </label>
      <div className="relative">
        <input
          type={type === 'password' ? (showPassword ? 'text' : 'password') : type}
          name={name}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          className={inputClassName}
        />
        {icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50">
            {icon}
          </div>
        )}
        {type === 'password' && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-base-content/50 hover:text-base-content"
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        )}
      </div>
      {type === 'password' && value && (
        <PasswordStrengthIndicator password={value} />
      )}
      {shouldShowErrors && <ValidationError errors={errors} />}
      {showValidationStatus && !shouldShowErrors && (
        <ValidationStatus 
          isValid={isValid} 
          isValidating={isValidating}
        />
      )}
    </div>
  );
};

interface ValidatedFormProps {
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent) => void;
  className?: string;
}

/**
 * Form wrapper that can display error summary
 */
export const ValidatedForm: React.FC<ValidatedFormProps> = ({
  children,
  onSubmit,
  className = ''
}) => {
  return (
    <form onSubmit={onSubmit} className={className} noValidate>
      {children}
    </form>
  );
};

interface FormFieldProps {
  name: string;
  label: string;
  type?: 'text' | 'email' | 'password' | 'textarea' | 'select';
  value: string;
  onChange: (name: string, value: string) => void;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  icon?: React.ReactNode;
  options?: { value: string; label: string }[]; // for select
  rows?: number; // for textarea
  error?: string; // external error
}

/**
 * Simplified form field component
 */
export const FormField: React.FC<FormFieldProps> = ({
  name,
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  disabled = false,
  className = '',
  icon,
  options = [],
  rows = 3,
  error
}) => {
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    onChange(name, e.target.value);
  };

  const inputClassName = `input input-bordered w-full ${
    icon ? 'pl-10' : ''
  } ${type === 'password' ? 'pr-10' : ''} ${
    error ? 'input-error' : ''
  } ${className}`;

  if (type === 'select') {
    return (
      <div className="form-control">
        <label className="label">
          <span className="label-text">
            {label}
            {required && <span className="text-error ml-1">*</span>}
          </span>
        </label>
        <select
          name={name}
          value={value}
          onChange={handleChange}
          disabled={disabled}
          className={`select select-bordered w-full ${error ? 'select-error' : ''} ${className}`}
        >
          <option value="">{placeholder || `Select ${label}`}</option>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {error && <ValidationError errors={[error]} />}
      </div>
    );
  }

  if (type === 'textarea') {
    return (
      <div className="form-control">
        <label className="label">
          <span className="label-text">
            {label}
            {required && <span className="text-error ml-1">*</span>}
          </span>
        </label>
        <textarea
          name={name}
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          disabled={disabled}
          rows={rows}
          className={`textarea textarea-bordered w-full ${error ? 'textarea-error' : ''} ${className}`}
        />
        {error && <ValidationError errors={[error]} />}
      </div>
    );
  }

  return (
    <div className="form-control">
      <label className="label">
        <span className="label-text">
          {label}
          {required && <span className="text-error ml-1">*</span>}
        </span>
      </label>
      <div className="relative">
        <input
          type={type === 'password' ? (showPassword ? 'text' : 'password') : type}
          name={name}
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          disabled={disabled}
          className={inputClassName}
        />
        {icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-base-content/50">
            {icon}
          </div>
        )}
        {type === 'password' && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-base-content/50 hover:text-base-content"
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        )}
      </div>
      {error && <ValidationError errors={[error]} />}
    </div>
  );
};
// Re-export validation components for convenience
export { 
  ValidationError, 
  FieldError, 
  FormErrorSummary, 
  PasswordStrengthIndicator, 
  ValidationStatus 
} from './ValidationError';
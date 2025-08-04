/**
 * Custom hook for form validation
 * Provides real-time form validation with state management
 */

import { useState, useCallback, useEffect } from 'react';
import { FormValidator, ValidationRule, ValidationResult, FormValidationResult } from '@/lib/validation';

interface UseFormValidationOptions {
  validateOnChange?: boolean;
  validateOnBlur?: boolean;
  debounceMs?: number;
}

interface FormField {
  value: string;
  errors: string[];
  isValid: boolean;
  hasBeenTouched: boolean;
  isValidating: boolean;
}

interface UseFormValidationReturn<T extends Record<string, unknown>> {
  formData: T;
  formFields: Record<keyof T, FormField>;
  errors: Record<keyof T, string[]>;
  isValid: boolean;
  isValidating: boolean;
  hasErrors: boolean;
  
  // Actions
  setFieldValue: (name: keyof T, value: string) => void;
  setFormData: (data: Partial<T>) => void;
  validateField: (name: keyof T) => Promise<ValidationResult>;
  validateForm: () => Promise<FormValidationResult>;
  touchField: (name: keyof T) => void;
  touchAllFields: () => void;
  resetForm: (data?: Partial<T>) => void;
  clearErrors: () => void;
  setFieldError: (name: keyof T, error: string) => void;
  
  // Utilities
  getFieldProps: (name: keyof T) => {
    name: string;
    value: string;
    onChange: (name: string, value: string) => void;
    onBlur: () => void;
    error: string | undefined;
    isValid: boolean;
    hasBeenTouched: boolean;
  };
}

export function useFormValidation<T extends Record<string, unknown>>(
  initialData: T,
  validationRules: Record<keyof T, ValidationRule[]>,
  options: UseFormValidationOptions = {}
): UseFormValidationReturn<T> {
  const {
    validateOnChange = true,
    validateOnBlur = true,
    debounceMs = 300
  } = options;

  // Form data state
  const [formData, setFormDataState] = useState<T>(initialData);
  
  // Field states
  const [formFields, setFormFields] = useState<Record<keyof T, FormField>>(() => {
    const fields: Record<keyof T, FormField> = {} as Record<keyof T, FormField>;
    Object.keys(initialData).forEach((key) => {
      fields[key as keyof T] = {
        value: initialData[key] || '',
        errors: [],
        isValid: false,
        hasBeenTouched: false,
        isValidating: false
      };
    });
    return fields;
  });

  // Debounced validation timers
  const [validationTimers, setValidationTimers] = useState<Record<string, NodeJS.Timeout>>({});

  // Computed states
  const errors = Object.keys(formFields).reduce((acc, key) => {
    acc[key as keyof T] = formFields[key as keyof T].errors;
    return acc;
  }, {} as Record<keyof T, string[]>);

  const isValid = Object.values(formFields).every(field => field.isValid && field.value.length > 0);
  const isValidating = Object.values(formFields).some(field => field.isValidating);
  const hasErrors = Object.values(formFields).some(field => field.errors.length > 0);

  // Validate a single field
  const validateField = useCallback(async (name: keyof T): Promise<ValidationResult> => {
    const fieldValue = formData[name];
    const rules = validationRules[name] || [];
    
    // Handle confirm password validation
    const processedRules = rules.map(rule => {
      if (rule.confirmPassword) {
        const passwordValue = formData[rule.confirmPassword as keyof T];
        return {
          ...rule,
          custom: (value: unknown) => {
            if (value !== passwordValue) {
              return 'Passwords do not match';
            }
            return null;
          }
        };
      }
      return rule;
    });

    const result = FormValidator.validateField(fieldValue, processedRules);
    
    setFormFields(prev => ({
      ...prev,
      [name]: {
        ...prev[name],
        errors: result.errors,
        isValid: result.isValid,
        isValidating: false
      }
    }));

    return result;
  }, [formData, validationRules]);

  // Debounced field validation
  const validateFieldDebounced = useCallback((name: keyof T) => {
    // Clear existing timer
    if (validationTimers[name as string]) {
      clearTimeout(validationTimers[name as string]);
    }

    // Set validating state
    setFormFields(prev => ({
      ...prev,
      [name]: {
        ...prev[name],
        isValidating: true
      }
    }));

    // Create new timer
    const timer = setTimeout(() => {
      validateField(name);
      setValidationTimers(prev => {
        const newTimers = { ...prev };
        delete newTimers[name as string];
        return newTimers;
      });
    }, debounceMs);

    setValidationTimers(prev => ({
      ...prev,
      [name as string]: timer
    }));
  }, [validateField, validationTimers, debounceMs]);

  // Validate entire form
  const validateForm = useCallback(async (): Promise<FormValidationResult> => {
    const results = await Promise.all(
      Object.keys(formData).map(async (key) => {
        const result = await validateField(key as keyof T);
        return [key, result] as const;
      })
    );

    const formErrors: Record<keyof T, string[]> = {} as Record<keyof T, string[]>;
    let formIsValid = true;

    results.forEach(([key, result]) => {
      formErrors[key as keyof T] = result.errors;
      if (!result.isValid) {
        formIsValid = false;
      }
    });

    return {
      isValid: formIsValid,
      errors: formErrors
    };
  }, [formData, validateField]);

  // Set field value
  const setFieldValue = useCallback((name: keyof T, value: string) => {
    // Sanitize input
    const sanitizedValue = FormValidator.sanitizeInput(value);
    
    setFormDataState(prev => ({
      ...prev,
      [name]: sanitizedValue
    }));

    setFormFields(prev => ({
      ...prev,
      [name]: {
        ...prev[name],
        value: sanitizedValue
      }
    }));

    // Validate on change if enabled and field has been touched
    if (validateOnChange && formFields[name]?.hasBeenTouched) {
      validateFieldDebounced(name);
    }
  }, [validateOnChange, formFields, validateFieldDebounced]);

  // Set form data
  const setFormData = useCallback((data: Partial<T>) => {
    setFormDataState(prev => ({ ...prev, ...data }));
    
    Object.keys(data).forEach(key => {
      const typedKey = key as keyof T;
      setFormFields(prev => ({
        ...prev,
        [typedKey]: {
          ...prev[typedKey],
          value: data[typedKey] || ''
        }
      }));
    });
  }, []);

  // Touch field (mark as interacted with)
  const touchField = useCallback((name: keyof T) => {
    setFormFields(prev => ({
      ...prev,
      [name]: {
        ...prev[name],
        hasBeenTouched: true
      }
    }));

    if (validateOnBlur) {
      validateField(name);
    }
  }, [validateOnBlur, validateField]);

  // Touch all fields
  const touchAllFields = useCallback(() => {
    setFormFields(prev => {
      const newFields = { ...prev };
      Object.keys(newFields).forEach(key => {
        newFields[key as keyof T] = {
          ...newFields[key as keyof T],
          hasBeenTouched: true
        };
      });
      return newFields;
    });
  }, []);

  // Reset form
  const resetForm = useCallback((data?: Partial<T>) => {
    const resetData = data ? { ...initialData, ...data } : initialData;
    
    setFormDataState(resetData);
    
    setFormFields(prev => {
      const newFields = { ...prev };
      Object.keys(newFields).forEach(key => {
        newFields[key as keyof T] = {
          value: resetData[key as keyof T] || '',
          errors: [],
          isValid: false,
          hasBeenTouched: false,
          isValidating: false
        };
      });
      return newFields;
    });

    // Clear all timers
    Object.values(validationTimers).forEach(timer => clearTimeout(timer));
    setValidationTimers({});
  }, [initialData, validationTimers]);

  // Clear errors
  const clearErrors = useCallback(() => {
    setFormFields(prev => {
      const newFields = { ...prev };
      Object.keys(newFields).forEach(key => {
        newFields[key as keyof T] = {
          ...newFields[key as keyof T],
          errors: [],
          isValid: true
        };
      });
      return newFields;
    });
  }, []);

  // Set field error (for server-side validation errors)
  const setFieldError = useCallback((name: keyof T, error: string) => {
    setFormFields(prev => ({
      ...prev,
      [name]: {
        ...prev[name],
        errors: [error],
        isValid: false
      }
    }));
  }, []);

  // Get field props for easy integration with form components
  const getFieldProps = useCallback((name: keyof T) => {
    const field = formFields[name];
    return {
      name: name as string,
      value: field?.value || '',
      onChange: setFieldValue,
      onBlur: () => touchField(name),
      error: field?.errors?.[0],
      isValid: field?.isValid || false,
      hasBeenTouched: field?.hasBeenTouched || false
    };
  }, [formFields, setFieldValue, touchField]);

  // Cleanup timers on unmount
  useEffect(() => {
    return () => {
      Object.values(validationTimers).forEach(timer => clearTimeout(timer));
    };
  }, [validationTimers]);

  // Update form fields when form data changes externally
  useEffect(() => {
    setFormFields(prev => {
      const newFields = { ...prev };
      Object.keys(formData).forEach(key => {
        const typedKey = key as keyof T;
        if (newFields[typedKey]) {
          newFields[typedKey] = {
            ...newFields[typedKey],
            value: formData[typedKey] || ''
          };
        }
      });
      return newFields;
    });
  }, [formData]);

  return {
    formData,
    formFields,
    errors,
    isValid,
    isValidating,
    hasErrors,
    
    setFieldValue,
    setFormData,
    validateField,
    validateForm,
    touchField,
    touchAllFields,
    resetForm,
    clearErrors,
    setFieldError,
    
    getFieldProps
  };
}
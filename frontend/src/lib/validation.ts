/**
 * Frontend Form Validation System
 * Provides comprehensive validation rules, real-time validation, and input sanitization
 */

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  email?: boolean;
  username?: boolean;
  password?: boolean;
  confirmPassword?: string; // field name to match against
  custom?: (value: unknown) => string | null;
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export interface FormValidationResult {
  isValid: boolean;
  errors: { [fieldName: string]: string[] };
}

export class FormValidator {
  /**
   * Validate a single field value against provided rules
   */
  static validateField(value: unknown, rules: ValidationRule[]): ValidationResult {
    const errors: string[] = [];

    for (const rule of rules) {
      // Required validation
      if (rule.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
        errors.push('This field is required');
        continue; // Skip other validations if required field is empty
      }

      // Skip other validations if field is empty and not required
      if (!value || (typeof value === 'string' && value.trim() === '')) {
        continue;
      }

      const stringValue = String(value).trim();

      // Min length validation
      if (rule.minLength && stringValue.length < rule.minLength) {
        errors.push(`Must be at least ${rule.minLength} characters long`);
      }

      // Max length validation
      if (rule.maxLength && stringValue.length > rule.maxLength) {
        errors.push(`Must be no more than ${rule.maxLength} characters long`);
      }

      // Pattern validation
      if (rule.pattern && !rule.pattern.test(stringValue)) {
        errors.push('Invalid format');
      }

      // Email validation
      if (rule.email && !this.isValidEmail(stringValue)) {
        errors.push('Please enter a valid email address');
      }

      // Username validation
      if (rule.username && !this.isValidUsername(stringValue)) {
        errors.push('Username must be 3-20 characters, letters, numbers, and underscores only');
      }

      // Password validation
      if (rule.password) {
        const passwordErrors = this.validatePassword(stringValue);
        errors.push(...passwordErrors);
      }

      // Custom validation
      if (rule.custom) {
        const customError = rule.custom(value);
        if (customError) {
          errors.push(customError);
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Validate an entire form object against validation rules
   */
  static validateForm(
    formData: { [key: string]: unknown },
    validationRules: { [key: string]: ValidationRule[] }
  ): FormValidationResult {
    const errors: { [fieldName: string]: string[] } = {};
    let isValid = true;

    for (const [fieldName, rules] of Object.entries(validationRules)) {
      const fieldValue = formData[fieldName];
      
      // Handle confirm password validation
      const processedRules = rules.map(rule => {
        if (rule.confirmPassword) {
          const passwordValue = formData[rule.confirmPassword];
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

      const result = this.validateField(fieldValue, processedRules);
      
      if (!result.isValid) {
        errors[fieldName] = result.errors;
        isValid = false;
      }
    }

    return { isValid, errors };
  }

  /**
   * Sanitize input to prevent XSS attacks
   */
  static sanitizeInput(input: string): string {
    if (typeof input !== 'string') {
      return String(input);
    }

    return input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;')
      .trim();
  }

  /**
   * Sanitize HTML content while preserving safe tags
   */
  static sanitizeHtml(html: string, allowedTags: string[] = ['b', 'i', 'em', 'strong', 'br']): string {
    if (typeof html !== 'string') {
      return String(html);
    }

    // Remove script tags and their content
    html = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    
    // Remove on* event handlers
    html = html.replace(/\s*on\w+\s*=\s*["'][^"']*["']/gi, '');
    
    // Remove javascript: protocols
    html = html.replace(/javascript:/gi, '');
    
    // If no allowed tags, strip all HTML
    if (allowedTags.length === 0) {
      return html.replace(/<[^>]*>/g, '');
    }

    // Create regex for allowed tags
    const allowedTagsRegex = new RegExp(`<(?!\/?(?:${allowedTags.join('|')})\s*\/?>)[^>]+>`, 'gi');
    
    return html.replace(allowedTagsRegex, '');
  }

  /**
   * Validate email format
   */
  private static isValidEmail(email: string): boolean {
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    return emailRegex.test(email);
  }

  /**
   * Validate username format
   */
  private static isValidUsername(username: string): boolean {
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    return usernameRegex.test(username);
  }

  /**
   * Validate password strength
   */
  private static validatePassword(password: string): string[] {
    const errors: string[] = [];

    if (password.length < 8) {
      errors.push('Password must be at least 8 characters long');
    }

    if (password.length > 128) {
      errors.push('Password must be no more than 128 characters long');
    }

    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }

    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }

    if (!/\d/.test(password)) {
      errors.push('Password must contain at least one number');
    }

    if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
      errors.push('Password must contain at least one special character');
    }

    // Check for common weak passwords
    const commonPasswords = [
      'password', '123456', '123456789', 'qwerty', 'abc123', 
      'password123', 'admin', 'letmein', 'welcome', 'monkey'
    ];
    
    if (commonPasswords.includes(password.toLowerCase())) {
      errors.push('Password is too common, please choose a stronger password');
    }

    return errors;
  }

  /**
   * Get password strength score (0-4)
   */
  static getPasswordStrength(password: string): { score: number; label: string; color: string } {
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

    return {
      score,
      label: labels[score],
      color: colors[score]
    };
  }

  /**
   * Debounced validation for real-time feedback
   */
  static createDebouncedValidator(
    validationFn: (value: unknown) => ValidationResult,
    delay: number = 300
  ): (value: unknown, callback: (result: ValidationResult) => void) => void {
    let timeoutId: NodeJS.Timeout;

    return (value: unknown, callback: (result: ValidationResult) => void) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        const result = validationFn(value);
        callback(result);
      }, delay);
    };
  }
}

/**
 * Common validation rule presets
 */
export const ValidationRules = {
  required: (): ValidationRule => ({ required: true }),
  
  email: (): ValidationRule => ({ 
    required: true, 
    email: true,
    maxLength: 255
  }),
  
  username: (): ValidationRule => ({ 
    required: true, 
    username: true,
    minLength: 3,
    maxLength: 20
  }),
  
  password: (): ValidationRule => ({ 
    required: true, 
    password: true,
    minLength: 8,
    maxLength: 128
  }),
  
  confirmPassword: (passwordField: string): ValidationRule => ({ 
    required: true,
    confirmPassword: passwordField
  }),
  
  displayName: (): ValidationRule => ({ 
    maxLength: 100,
    pattern: /^[a-zA-Z0-9\s._-]*$/
  }),
  
  bio: (): ValidationRule => ({ 
    maxLength: 500
  }),
  
  chatMessage: (): ValidationRule => ({ 
    required: true,
    maxLength: 2000,
    custom: (value: unknown) => {
      const stringValue = String(value || '');
      if (stringValue && stringValue.trim().length === 0) {
        return 'Message cannot be empty or contain only whitespace';
      }
      return null;
    }
  }),
  
  roomName: (): ValidationRule => ({ 
    required: true,
    minLength: 3,
    maxLength: 50,
    pattern: /^[a-zA-Z0-9\s._-]+$/
  }),
  
  roomDescription: (): ValidationRule => ({ 
    maxLength: 200
  })
};
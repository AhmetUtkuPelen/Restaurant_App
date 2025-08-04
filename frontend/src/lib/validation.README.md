# Frontend Form Validation System

This validation system provides comprehensive form validation with real-time feedback, input sanitization, and consistent error display components.

## Features

- **Real-time validation** with debouncing
- **Input sanitization** to prevent XSS attacks
- **Password strength indicators**
- **Consistent error display components**
- **TypeScript support** with full type safety
- **Customizable validation rules**
- **Server-side error integration**

## Quick Start

### 1. Basic Form with useFormValidation Hook

```tsx
import { useFormValidation } from '@/hooks/useFormValidation';
import { ValidationRules } from '@/lib/validation';
import { ValidatedInput } from '@/components/ui/ValidatedInput';

function MyForm() {
  const {
    formData,
    errors,
    isValid,
    setFieldValue,
    validateForm,
    touchAllFields
  } = useFormValidation(
    {
      email: '',
      password: ''
    },
    {
      email: [ValidationRules.email()],
      password: [ValidationRules.password()]
    }
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    touchAllFields();
    
    const result = await validateForm();
    if (!result.isValid) return;
    
    // Submit form data
    console.log('Valid form data:', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <ValidatedInput
        name="email"
        label="Email"
        type="email"
        value={formData.email}
        onChange={setFieldValue}
        validationRules={[ValidationRules.email()]}
        required
      />
      
      <ValidatedInput
        name="password"
        label="Password"
        type="password"
        value={formData.password}
        onChange={setFieldValue}
        validationRules={[ValidationRules.password()]}
        required
      />
      
      <button type="submit" disabled={!isValid}>
        Submit
      </button>
    </form>
  );
}
```

### 2. Manual Validation with FormValidator

```tsx
import { FormValidator, ValidationRules } from '@/lib/validation';

// Validate a single field
const result = FormValidator.validateField('test@example.com', [
  ValidationRules.email()
]);

console.log(result.isValid); // true
console.log(result.errors);  // []

// Validate entire form
const formResult = FormValidator.validateForm(
  { email: 'invalid', password: '123' },
  {
    email: [ValidationRules.email()],
    password: [ValidationRules.password()]
  }
);

console.log(formResult.isValid); // false
console.log(formResult.errors);  // { email: [...], password: [...] }
```

## Validation Rules

### Pre-built Rules

```tsx
import { ValidationRules } from '@/lib/validation';

// Common validation rules
ValidationRules.required()           // Field is required
ValidationRules.email()             // Valid email format
ValidationRules.username()          // 3-20 chars, alphanumeric + underscore
ValidationRules.password()          // Strong password requirements
ValidationRules.confirmPassword('password') // Must match another field
ValidationRules.displayName()       // Display name format
ValidationRules.bio()              // Bio text (max 500 chars)
ValidationRules.chatMessage()       // Chat message validation
ValidationRules.roomName()          // Chat room name
ValidationRules.roomDescription()   // Room description
```

### Custom Rules

```tsx
import { ValidationRule } from '@/lib/validation';

const customRules: ValidationRule[] = [
  {
    required: true,
    minLength: 5,
    maxLength: 50,
    pattern: /^[a-zA-Z0-9\s]+$/,
    custom: (value: string) => {
      if (value.includes('banned')) {
        return 'This word is not allowed';
      }
      return null;
    }
  }
];
```

## Components

### ValidatedInput

Full-featured input component with built-in validation:

```tsx
<ValidatedInput
  name="username"
  label="Username"
  type="text"
  value={formData.username}
  onChange={handleFieldChange}
  validationRules={[ValidationRules.username()]}
  placeholder="Enter username"
  required
  icon={<User size={18} />}
  showValidationStatus={true}
  validateOnChange={true}
  validateOnBlur={true}
  debounceMs={300}
/>
```

### FormField (Simplified)

Simpler form field component:

```tsx
<FormField
  name="bio"
  label="Bio"
  type="textarea"
  value={formData.bio}
  onChange={handleFieldChange}
  placeholder="Tell us about yourself..."
  rows={4}
  error={errors.bio?.[0]}
/>
```

### Error Display Components

```tsx
import { 
  ValidationError, 
  FieldError, 
  FormErrorSummary,
  PasswordStrengthIndicator 
} from '@/components/ui/ValidationError';

// Single field errors
<ValidationError errors={['Error 1', 'Error 2']} />

// Simple field error
<FieldError error="This field is required" />

// Form error summary
<FormErrorSummary 
  errors={formErrors}
  fieldLabels={{ email: 'Email Address' }}
  dismissible
  onDismiss={() => setShowErrors(false)}
/>

// Password strength
<PasswordStrengthIndicator password={password} />
```

## Input Sanitization

All inputs are automatically sanitized to prevent XSS attacks:

```tsx
import { FormValidator } from '@/lib/validation';

// Basic sanitization (removes HTML tags and dangerous characters)
const safe = FormValidator.sanitizeInput('<script>alert("xss")</script>');
// Result: "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;"

// HTML sanitization (allows safe tags)
const safeHtml = FormValidator.sanitizeHtml(
  '<p>Safe content</p><script>dangerous()</script>',
  ['p', 'b', 'i', 'em', 'strong']
);
// Result: "<p>Safe content</p>"
```

## Server-Side Error Integration

Handle server validation errors:

```tsx
const handleSubmit = async (e: React.FormEvent) => {
  try {
    await submitForm(formData);
  } catch (err: any) {
    const errorData = err.response?.data;
    
    // Handle field-specific errors
    if (errorData?.field_errors) {
      Object.entries(errorData.field_errors).forEach(([field, message]) => {
        setFieldError(field, message as string);
      });
    } else {
      // Handle general errors
      setServerError(errorData?.detail || 'Submission failed');
    }
  }
};
```

## Advanced Usage

### Custom Validation Hook

```tsx
function useCustomValidation() {
  const validation = useFormValidation(
    { /* initial data */ },
    { /* validation rules */ },
    {
      validateOnChange: true,
      validateOnBlur: true,
      debounceMs: 500
    }
  );

  // Add custom logic
  const submitForm = async () => {
    validation.touchAllFields();
    const result = await validation.validateForm();
    
    if (result.isValid) {
      // Submit logic
    }
  };

  return {
    ...validation,
    submitForm
  };
}
```

### Debounced Validation

```tsx
import { FormValidator } from '@/lib/validation';

const debouncedValidator = FormValidator.createDebouncedValidator(
  (value) => FormValidator.validateField(value, [ValidationRules.email()]),
  500 // 500ms delay
);

debouncedValidator('test@example.com', (result) => {
  console.log('Validation result:', result);
});
```

## Best Practices

1. **Always sanitize user input** - The system does this automatically
2. **Use real-time validation** for better UX
3. **Touch fields on blur** to show validation errors
4. **Validate on submit** to ensure data integrity
5. **Handle server errors** gracefully
6. **Use appropriate validation rules** for each field type
7. **Provide clear error messages** to users
8. **Test validation logic** thoroughly

## Examples

See the following files for complete examples:
- `frontend/src/app/(auth)/login/page.tsx` - Login form
- `frontend/src/app/(auth)/register/page.tsx` - Registration form
- `frontend/src/components/forms/ProfileForm.tsx` - Profile editing
- `frontend/src/components/chat/MessageInput.tsx` - Chat message input
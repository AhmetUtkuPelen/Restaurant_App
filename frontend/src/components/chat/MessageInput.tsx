/**
 * Message Input Component with Validation
 * Example of using the validation system for chat messages
 */

import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Smile } from 'lucide-react';
import { FormValidator, ValidationRules } from '@/lib/validation';
import { ValidationError } from '@/components/ui/ValidationError';

interface MessageInputProps {
  onSendMessage: (message: string, attachments?: File[]) => void;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
  className?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = 'Type your message...',
  maxLength = 2000,
  className = ''
}) => {
  const [message, setMessage] = useState('');
  const [errors, setErrors] = useState<string[]>([]);
  const [attachments, setAttachments] = useState<File[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Validation rules for chat messages
  const validationRules = [
    ValidationRules.chatMessage(),
    { maxLength }
  ];

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  // Handle message change with validation
  const handleMessageChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    
    // Sanitize input
    const sanitizedValue = FormValidator.sanitizeInput(value);
    setMessage(sanitizedValue);

    // Real-time validation
    const result = FormValidator.validateField(sanitizedValue, validationRules);
    setErrors(result.errors);
  };

  // Handle file attachment
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    
    // Validate file types and sizes
    const validFiles: File[] = [];
    const fileErrors: string[] = [];

    files.forEach(file => {
      // Check file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        fileErrors.push(`${file.name} is too large (max 10MB)`);
        return;
      }

      // Check file type
      const allowedTypes = [
        'image/jpeg', 'image/png', 'image/gif', 'image/webp',
        'application/pdf', 'text/plain', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
      ];

      if (!allowedTypes.includes(file.type)) {
        fileErrors.push(`${file.name} is not a supported file type`);
        return;
      }

      validFiles.push(file);
    });

    if (fileErrors.length > 0) {
      setErrors(prev => [...prev, ...fileErrors]);
    }

    setAttachments(prev => [...prev, ...validFiles]);
    
    // Clear file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Remove attachment
  const removeAttachment = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate message
    const result = FormValidator.validateField(message, validationRules);
    setErrors(result.errors);

    if (!result.isValid) {
      return;
    }

    // Send message
    onSendMessage(message.trim(), attachments);

    // Reset form
    setMessage('');
    setAttachments([]);
    setErrors([]);
  };

  // Handle Enter key (Shift+Enter for new line)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as React.FormEvent);
    }
  };

  const isValid = errors.length === 0 && message.trim().length > 0;
  const characterCount = message.length;
  const isNearLimit = characterCount > maxLength * 0.8;

  return (
    <div className={`bg-base-100 border-t border-base-300 p-4 ${className}`}>
      <form onSubmit={handleSubmit} className="space-y-2">
        {/* Attachments preview */}
        {attachments.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-2">
            {attachments.map((file, index) => (
              <div
                key={index}
                className="flex items-center gap-2 bg-base-200 rounded-lg px-3 py-1 text-sm"
              >
                <Paperclip size={14} />
                <span className="truncate max-w-32">{file.name}</span>
                <button
                  type="button"
                  onClick={() => removeAttachment(index)}
                  className="text-error hover:text-error/80"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Message input */}
        <div className="flex items-end gap-2">
          <div className="flex-1">
            <div className="relative">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={handleMessageChange}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                disabled={disabled}
                rows={1}
                className={`textarea textarea-bordered w-full resize-none min-h-[2.5rem] max-h-32 pr-20 ${
                  errors.length > 0 ? 'textarea-error' : ''
                }`}
                style={{ paddingRight: '5rem' }}
              />
              
              {/* Character count */}
              <div className={`absolute bottom-2 right-12 text-xs ${
                isNearLimit ? 'text-warning' : 'text-base-content/50'
              }`}>
                {characterCount}/{maxLength}
              </div>
            </div>

            {/* Validation errors */}
            {errors.length > 0 && (
              <ValidationError errors={errors} className="mt-1" />
            )}
          </div>

          {/* Action buttons */}
          <div className="flex items-center gap-1">
            {/* File attachment button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={disabled}
              className="btn btn-ghost btn-sm btn-square"
              title="Attach file"
            >
              <Paperclip size={18} />
            </button>

            {/* Emoji button (placeholder) */}
            <button
              type="button"
              disabled={disabled}
              className="btn btn-ghost btn-sm btn-square"
              title="Add emoji"
            >
              <Smile size={18} />
            </button>

            {/* Send button */}
            <button
              type="submit"
              disabled={disabled || !isValid}
              className="btn btn-primary btn-sm btn-square"
              title="Send message (Enter)"
            >
              <Send size={18} />
            </button>
          </div>
        </div>

        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          accept="image/*,.pdf,.txt,.doc,.docx"
        />
      </form>
    </div>
  );
};
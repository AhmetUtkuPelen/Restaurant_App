import re
import bleach
from typing import Dict, List, Optional, Any
from fastapi import UploadFile, HTTPException, status
from email_validator import validate_email, EmailNotValidError
from config import settings
import mimetypes
import magic
from pathlib import Path

class ValidationService:
    """Comprehensive input validation and sanitization service"""
    
    # Allowed HTML tags and attributes for message content
    ALLOWED_HTML_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'code', 'pre', 'blockquote',
        'ul', 'ol', 'li', 'a', 'img'
    ]
    
    ALLOWED_HTML_ATTRIBUTES = {
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        '*': ['class']
    }
    
    # Common SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
        r"(\b(OR|AND)\s+\d+\s*=\s*\d+)",
        r"(\b(OR|AND)\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?)",
        r"(--|#|/\*|\*/)",
        r"(\bxp_\w+)",
        r"(\bsp_\w+)"
    ]
    
    @staticmethod
    def validate_email_address(email: str) -> Dict[str, Any]:
        """
        Validate email address format and deliverability
        
        Args:
            email: Email address to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Basic format validation
            if not email or len(email.strip()) == 0:
                return {
                    "is_valid": False,
                    "error": "Email address is required",
                    "normalized_email": None
                }
            
            # Length check
            if len(email) > 254:  # RFC 5321 limit
                return {
                    "is_valid": False,
                    "error": "Email address is too long",
                    "normalized_email": None
                }
            
            # Use email-validator library for comprehensive validation
            validated_email = validate_email(email)
            
            return {
                "is_valid": True,
                "error": None,
                "normalized_email": validated_email.email
            }
            
        except EmailNotValidError as e:
            return {
                "is_valid": False,
                "error": str(e),
                "normalized_email": None
            }
    
    @staticmethod
    def validate_username(username: str) -> Dict[str, Any]:
        """
        Validate username format and constraints
        
        Args:
            username: Username to validate
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        
        if not username or len(username.strip()) == 0:
            errors.append("Username is required")
        else:
            username = username.strip()
            
            # Length constraints
            if len(username) < 3:
                errors.append("Username must be at least 3 characters long")
            elif len(username) > 30:
                errors.append("Username must be no more than 30 characters long")
            
            # Character constraints
            if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
                errors.append("Username can only contain letters, numbers, underscores, dots, and hyphens")
            
            # Must start with letter or number
            if not re.match(r'^[a-zA-Z0-9]', username):
                errors.append("Username must start with a letter or number")
            
            # Cannot end with special characters
            if username.endswith(('.', '-', '_')):
                errors.append("Username cannot end with special characters")
            
            # Reserved usernames
            reserved_usernames = [
                'admin', 'administrator', 'root', 'system', 'api', 'www',
                'mail', 'email', 'support', 'help', 'info', 'contact',
                'user', 'users', 'guest', 'anonymous', 'null', 'undefined'
            ]
            
            if username.lower() in reserved_usernames:
                errors.append("This username is reserved and cannot be used")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "normalized_username": username.lower() if username else None
        }
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """
        Validate password strength (delegates to PasswordService)
        
        Args:
            password: Password to validate
            
        Returns:
            Dictionary with validation results
        """
        from Services.PasswordService import PasswordService
        return PasswordService.validate_password_strength(password)
    
    @staticmethod
    def sanitize_html(content: str, allowed_tags: Optional[List[str]] = None) -> str:
        """
        Sanitize HTML content to prevent XSS attacks
        
        Args:
            content: HTML content to sanitize
            allowed_tags: List of allowed HTML tags (uses default if None)
            
        Returns:
            Sanitized HTML content
        """
        if not content:
            return ""
        
        allowed_tags = allowed_tags or ValidationService.ALLOWED_HTML_TAGS
        
        # Use bleach to sanitize HTML
        sanitized = bleach.clean(
            content,
            tags=allowed_tags,
            attributes=ValidationService.ALLOWED_HTML_ATTRIBUTES,
            strip=True,
            strip_comments=True
        )
        
        return sanitized
    
    @staticmethod
    def sanitize_text_input(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize plain text input
        
        Args:
            text: Text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        # Truncate if necessary
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length].strip()
        
        return sanitized
    
    @staticmethod
    def check_sql_injection(input_string: str) -> Dict[str, Any]:
        """
        Check for potential SQL injection patterns
        
        Args:
            input_string: String to check
            
        Returns:
            Dictionary with check results
        """
        if not input_string:
            return {"is_safe": True, "detected_patterns": []}
        
        detected_patterns = []
        
        for pattern in ValidationService.SQL_INJECTION_PATTERNS:
            if re.search(pattern, input_string, re.IGNORECASE):
                detected_patterns.append(pattern)
        
        return {
            "is_safe": len(detected_patterns) == 0,
            "detected_patterns": detected_patterns
        }
    
    @staticmethod
    def validate_file_upload(file: UploadFile) -> Dict[str, Any]:
        """
        Validate uploaded file for security and constraints
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        # Check if file exists
        if not file or not file.filename:
            errors.append("No file provided")
            return {
                "is_valid": False,
                "errors": errors,
                "warnings": warnings,
                "file_info": None
            }
        
        # File size check
        if hasattr(file, 'size') and file.size:
            if file.size > settings.max_file_size:
                errors.append(f"File size ({file.size} bytes) exceeds maximum allowed size ({settings.max_file_size} bytes)")
        
        # File extension check
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in settings.allowed_file_types_list:
            errors.append(f"File type '{file_extension}' is not allowed. Allowed types: {', '.join(settings.allowed_file_types_list)}")
        
        # MIME type validation
        try:
            # Read a small portion of the file to check MIME type
            file_content = file.file.read(1024)
            file.file.seek(0)  # Reset file pointer
            
            # Use python-magic to detect actual file type
            try:
                detected_mime = magic.from_buffer(file_content, mime=True)
                
                # Map file extensions to expected MIME types
                expected_mimes = {
                    '.jpg': ['image/jpeg'],
                    '.jpeg': ['image/jpeg'],
                    '.png': ['image/png'],
                    '.gif': ['image/gif'],
                    '.pdf': ['application/pdf'],
                    '.txt': ['text/plain'],
                    '.doc': ['application/msword'],
                    '.docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
                }
                
                if file_extension in expected_mimes:
                    if detected_mime not in expected_mimes[file_extension]:
                        warnings.append(f"File extension '{file_extension}' doesn't match detected MIME type '{detected_mime}'")
                
            except Exception:
                warnings.append("Could not verify file MIME type")
        
        except Exception as e:
            warnings.append(f"Could not read file for validation: {str(e)}")
        
        # Filename validation
        filename_validation = ValidationService.validate_filename(file.filename)
        if not filename_validation["is_valid"]:
            errors.extend(filename_validation["errors"])
        
        file_info = {
            "original_filename": file.filename,
            "file_extension": file_extension,
            "content_type": file.content_type,
            "size": getattr(file, 'size', None)
        }
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "file_info": file_info
        }
    
    @staticmethod
    def validate_filename(filename: str) -> Dict[str, Any]:
        """
        Validate filename for security and constraints
        
        Args:
            filename: Filename to validate
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        
        if not filename:
            errors.append("Filename is required")
            return {"is_valid": False, "errors": errors}
        
        # Length check
        if len(filename) > 255:
            errors.append("Filename is too long (maximum 255 characters)")
        
        # Dangerous characters check
        dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\0']
        for char in dangerous_chars:
            if char in filename:
                errors.append(f"Filename contains dangerous character: '{char}'")
        
        # Path traversal check
        if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
            errors.append("Filename contains path traversal patterns")
        
        # Reserved names check (Windows)
        reserved_names = [
            'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
            'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
            'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        ]
        
        filename_without_ext = Path(filename).stem.upper()
        if filename_without_ext in reserved_names:
            errors.append(f"Filename '{filename}' is a reserved system name")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def validate_message_content(content: str) -> Dict[str, Any]:
        """
        Validate message content for chat messages
        
        Args:
            content: Message content to validate
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        if not content or len(content.strip()) == 0:
            errors.append("Message content cannot be empty")
            return {
                "is_valid": False,
                "errors": errors,
                "warnings": warnings,
                "sanitized_content": ""
            }
        
        # Length check
        max_message_length = 5000  # Configurable limit
        if len(content) > max_message_length:
            errors.append(f"Message is too long (maximum {max_message_length} characters)")
        
        # Check for potential SQL injection
        sql_check = ValidationService.check_sql_injection(content)
        if not sql_check["is_safe"]:
            warnings.append("Message contains patterns that might be unsafe")
        
        # Sanitize HTML content
        sanitized_content = ValidationService.sanitize_html(content)
        
        # Check for excessive formatting
        if len(sanitized_content) < len(content) * 0.5:  # More than 50% was removed
            warnings.append("Message contained excessive or potentially unsafe formatting")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "sanitized_content": sanitized_content
        }
    
    @staticmethod
    def validate_room_name(name: str) -> Dict[str, Any]:
        """
        Validate chat room name
        
        Args:
            name: Room name to validate
            
        Returns:
            Dictionary with validation results
        """
        errors = []
        
        if not name or len(name.strip()) == 0:
            errors.append("Room name is required")
        else:
            name = name.strip()
            
            # Length constraints
            if len(name) < 2:
                errors.append("Room name must be at least 2 characters long")
            elif len(name) > 50:
                errors.append("Room name must be no more than 50 characters long")
            
            # Character constraints (allow more flexibility than usernames)
            if not re.match(r'^[a-zA-Z0-9\s_.-]+$', name):
                errors.append("Room name can only contain letters, numbers, spaces, underscores, dots, and hyphens")
            
            # Cannot be only special characters or spaces
            if re.match(r'^[\s_.-]+$', name):
                errors.append("Room name must contain at least one letter or number")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "normalized_name": name.strip() if name else None
        }
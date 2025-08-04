import bcrypt
import re
from typing import Dict, List
from config import settings

class PasswordService:
    """Secure password hashing and validation service using bcrypt"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt with salt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=settings.bcrypt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password: Plain text password to verify
            hashed_password: Stored hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, any]:
        """
        Validate password strength and return detailed feedback
        
        Args:
            password: Password to validate
            
        Returns:
            Dictionary with validation results and feedback
        """
        errors = []
        score = 0
        
        # Length check
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        elif len(password) >= 12:
            score += 2
        else:
            score += 1
            
        # Uppercase letter check
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        else:
            score += 1
            
        # Lowercase letter check
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        else:
            score += 1
            
        # Number check
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        else:
            score += 1
            
        # Special character check
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        else:
            score += 1
            
        # Common password patterns check
        common_patterns = [
            r'123456', r'password', r'qwerty', r'abc123',
            r'admin', r'letmein', r'welcome', r'monkey'
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                errors.append("Password contains common patterns and is not secure")
                score = max(0, score - 2)
                break
        
        # Sequential characters check
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            errors.append("Password should not contain sequential numbers")
            score = max(0, score - 1)
            
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            errors.append("Password should not contain sequential letters")
            score = max(0, score - 1)
        
        # Determine strength level
        if score >= 5:
            strength = "Strong"
        elif score >= 3:
            strength = "Medium"
        else:
            strength = "Weak"
            
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "score": score,
            "strength": strength,
            "suggestions": PasswordService._get_password_suggestions(errors)
        }
    
    @staticmethod
    def _get_password_suggestions(errors: List[str]) -> List[str]:
        """
        Generate helpful suggestions based on validation errors
        
        Args:
            errors: List of validation errors
            
        Returns:
            List of suggestions to improve password
        """
        suggestions = []
        
        if any("8 characters" in error for error in errors):
            suggestions.append("Use at least 8 characters, preferably 12 or more")
            
        if any("uppercase" in error for error in errors):
            suggestions.append("Add at least one uppercase letter (A-Z)")
            
        if any("lowercase" in error for error in errors):
            suggestions.append("Add at least one lowercase letter (a-z)")
            
        if any("number" in error for error in errors):
            suggestions.append("Include at least one number (0-9)")
            
        if any("special character" in error for error in errors):
            suggestions.append("Add special characters like !@#$%^&*()")
            
        if any("common patterns" in error for error in errors):
            suggestions.append("Avoid common passwords and dictionary words")
            
        if any("sequential" in error for error in errors):
            suggestions.append("Avoid sequential characters like 123 or abc")
            
        # General suggestions
        suggestions.extend([
            "Consider using a passphrase with multiple words",
            "Use a password manager to generate and store secure passwords",
            "Make your password unique for this application"
        ])
        
        return suggestions
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """
        Generate a cryptographically secure password
        
        Args:
            length: Desired password length (minimum 12)
            
        Returns:
            Generated secure password
        """
        import secrets
        import string
        
        if length < 12:
            length = 12
            
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each set
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # Fill the rest with random characters from all sets
        all_chars = lowercase + uppercase + digits + special
        for _ in range(length - 4):
            password.append(secrets.choice(all_chars))
            
        # Shuffle the password list
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
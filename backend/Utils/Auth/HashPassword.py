from typing import Dict
import logging
from passlib.context import CryptContext

# Configure logging
logger = logging.getLogger(__name__)

# Configure password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Good balance between security and performance
)

class PasswordError(Exception):
    """Base exception for password related errors"""
    def __init__(self, message: str = "Password operation failed", **kwargs):
        self.message = message
        self.details = kwargs
        super().__init__(self.message)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
        
    Raises:
        PasswordError: If there's an error during verification
    """
    try:
        if not plain_password or not hashed_password:
            logger.warning("Empty password or hash provided for verification")
            return False
            
        if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
            logger.error("Password and hash must be strings")
            return False
            
        return pwd_context.verify(plain_password, hashed_password)
        
    except (ValueError, TypeError) as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in verify_password: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """
    Generate a secure hash from a password.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        str: The hashed password
        
    Raises:
        PasswordError: If password is invalid or hashing fails
    """
    if not password or not isinstance(password, str):
        raise PasswordError("Password must be a non-empty string")
        
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise PasswordError("Failed to hash password") from e

def is_password_strong(password: str) -> Dict[str, bool]:
    """
    Check if a password meets strength requirements.
    
    Args:
        password: The password to check
        
    Returns:
        Dict[str, bool]: Dictionary with strength check results
    """
    if not password or not isinstance(password, str):
        return {
            "valid": False,
            "length": False,
            "uppercase": False,
            "lowercase": False,
            "digit": False,
            "special": False
        }
    
    return {
        "valid": all([
            len(password) >= 8,
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(not c.isalnum() for c in password)
        ]),
        "length": len(password) >= 8,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "digit": any(c.isdigit() for c in password),
        "special": any(not c.isalnum() for c in password)
    }
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Set
from fastapi import HTTPException, status
from config import settings
import redis
import json
import uuid

class AuthService:
    """Enhanced JWT authentication service with refresh tokens and blacklisting"""
    
    # Redis client for token blacklisting
    _redis_client = None
    
    @classmethod
    def _get_redis_client(cls):
        """Get Redis client for token blacklisting"""
        if cls._redis_client is None:
            try:
                cls._redis_client = redis.from_url(settings.redis_url)
                # Test connection
                cls._redis_client.ping()
            except Exception:
                # Fallback to in-memory storage for development
                cls._redis_client = {}
        return cls._redis_client
    
    @classmethod
    def create_access_token(cls, user_id: str, role: str = "USER", expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token with user ID and role
        
        Args:
            user_id: User identifier
            role: User role (USER, ADMIN, MODERATOR)
            expires_delta: Custom expiration time
            
        Returns:
            JWT access token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        
        # Create unique token ID for blacklisting
        token_id = str(uuid.uuid4())
        
        payload = {
            "sub": user_id,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": token_id,  # JWT ID for blacklisting
            "type": "access"
        }
        
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    @classmethod
    def create_refresh_token(cls, user_id: str, role: str = "USER") -> str:
        """
        Create JWT refresh token
        
        Args:
            user_id: User identifier
            role: User role
            
        Returns:
            JWT refresh token
        """
        expire = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expire_days)
        token_id = str(uuid.uuid4())
        
        payload = {
            "sub": user_id,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": token_id,
            "type": "refresh"
        }
        
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    @classmethod
    def verify_token(cls, token: str, token_type: str = "access") -> Dict:
        """
        Verify JWT token and return payload
        
        Args:
            token: JWT token to verify
            token_type: Expected token type (access or refresh)
            
        Returns:
            Token payload
            
        Raises:
            HTTPException: If token is invalid or blacklisted
        """
        try:
            # Decode token
            payload = jwt.decode(
                token, 
                settings.jwt_secret_key, 
                algorithms=[settings.jwt_algorithm]
            )
            
            # Verify token type
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type. Expected {token_type}",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check if token is blacklisted
            token_id = payload.get("jti")
            if token_id and cls._is_token_blacklisted(token_id):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has been revoked",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Verify required fields
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> Dict[str, str]:
        """
        Create new access token from refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Dictionary with new access token and refresh token
        """
        # Verify refresh token
        payload = cls.verify_token(refresh_token, "refresh")
        
        user_id = payload.get("sub")
        role = payload.get("role", "USER")
        
        # Create new tokens
        new_access_token = cls.create_access_token(user_id, role)
        new_refresh_token = cls.create_refresh_token(user_id, role)
        
        # Blacklist old refresh token
        old_token_id = payload.get("jti")
        if old_token_id:
            cls.blacklist_token(old_token_id, settings.jwt_refresh_token_expire_days * 24 * 3600)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    
    @classmethod
    def blacklist_token(cls, token_id: str, expire_seconds: int = None) -> None:
        """
        Add token to blacklist
        
        Args:
            token_id: JWT ID to blacklist
            expire_seconds: Expiration time for blacklist entry
        """
        redis_client = cls._get_redis_client()
        
        if isinstance(redis_client, dict):
            # Fallback in-memory storage
            redis_client[f"blacklist:{token_id}"] = True
        else:
            # Redis storage
            if expire_seconds:
                redis_client.setex(f"blacklist:{token_id}", expire_seconds, "true")
            else:
                redis_client.set(f"blacklist:{token_id}", "true")
    
    @classmethod
    def _is_token_blacklisted(cls, token_id: str) -> bool:
        """
        Check if token is blacklisted
        
        Args:
            token_id: JWT ID to check
            
        Returns:
            True if token is blacklisted
        """
        redis_client = cls._get_redis_client()
        
        if isinstance(redis_client, dict):
            # Fallback in-memory storage
            return f"blacklist:{token_id}" in redis_client
        else:
            # Redis storage
            try:
                return redis_client.exists(f"blacklist:{token_id}")
            except Exception:
                return False
    
    @classmethod
    def revoke_all_user_tokens(cls, user_id: str) -> None:
        """
        Revoke all tokens for a specific user
        
        Args:
            user_id: User identifier
        """
        redis_client = cls._get_redis_client()
        
        if not isinstance(redis_client, dict):
            try:
                # Set a flag to invalidate all tokens for this user
                redis_client.set(f"user_revoked:{user_id}", "true", ex=settings.jwt_refresh_token_expire_days * 24 * 3600)
            except Exception:
                pass
    
    @classmethod
    def get_user_id_from_token(cls, token: str) -> str:
        """
        Extract user ID from JWT token
        
        Args:
            token: JWT token
            
        Returns:
            User ID
        """
        payload = cls.verify_token(token)
        return payload.get("sub")
    
    @classmethod
    def get_user_role_from_token(cls, token: str) -> str:
        """
        Extract user role from JWT token
        
        Args:
            token: JWT token
            
        Returns:
            User role
        """
        payload = cls.verify_token(token)
        return payload.get("role", "USER")
    
    @classmethod
    def decode_token_without_verification(cls, token: str) -> Optional[Dict]:
        """
        Decode token without verification (for debugging/logging)
        
        Args:
            token: JWT token
            
        Returns:
            Token payload or None if invalid
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception:
            return None

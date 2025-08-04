"""
Unit tests for AuthService

Tests JWT token creation, verification, refresh, and blacklisting functionality.
Includes security-focused tests for token validation and edge cases.
"""

import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from fastapi import HTTPException

from Services.AuthService import AuthService
from config import settings


class TestAuthService:
    """Test cases for AuthService functionality."""
    
    def test_create_access_token_success(self, mock_redis):
        """Test successful access token creation."""
        user_id = "test-user-123"
        role = "USER"
        
        token = AuthService.create_access_token(user_id, role)
        
        # Verify token is created
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify payload
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        
        assert payload["sub"] == user_id
        assert payload["role"] == role
        assert payload["type"] == "access"
        assert "jti" in payload
        assert "exp" in payload
        assert "iat" in payload
    
    def test_create_access_token_with_custom_expiry(self, mock_redis):
        """Test access token creation with custom expiration."""
        user_id = "test-user-123"
        role = "USER"
        custom_expiry = timedelta(minutes=5)
        
        token = AuthService.create_access_token(user_id, role, custom_expiry)
        
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        
        # Check expiration is approximately 5 minutes from now
        exp_time = datetime.fromtimestamp(payload["exp"])
        expected_exp = datetime.utcnow() + custom_expiry
        
        # Allow 10 second tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 10
    
    def test_create_refresh_token_success(self, mock_redis):
        """Test successful refresh token creation."""
        user_id = "test-user-123"
        role = "USER"
        
        token = AuthService.create_refresh_token(user_id, role)
        
        # Verify token is created
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify payload
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        
        assert payload["sub"] == user_id
        assert payload["role"] == role
        assert payload["type"] == "refresh"
        assert "jti" in payload
    
    def test_verify_token_success(self, mock_redis):
        """Test successful token verification."""
        user_id = "test-user-123"
        role = "ADMIN"
        
        token = AuthService.create_access_token(user_id, role)
        payload = AuthService.verify_token(token, "access")
        
        assert payload["sub"] == user_id
        assert payload["role"] == role
        assert payload["type"] == "access"
    
    def test_verify_token_wrong_type(self, mock_redis):
        """Test token verification with wrong token type."""
        user_id = "test-user-123"
        role = "USER"
        
        access_token = AuthService.create_access_token(user_id, role)
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(access_token, "refresh")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token type" in str(exc_info.value.detail)
    
    def test_verify_token_expired(self, mock_redis):
        """Test verification of expired token."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create token with very short expiry
        expired_token = AuthService.create_access_token(
            user_id, role, timedelta(seconds=-1)
        )
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(expired_token)
        
        assert exc_info.value.status_code == 401
        assert "Token has expired" in str(exc_info.value.detail)
    
    def test_verify_token_invalid_signature(self, mock_redis):
        """Test verification of token with invalid signature."""
        # Create token with wrong secret
        payload = {
            "sub": "test-user-123",
            "role": "USER",
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "jti": "test-jti"
        }
        
        invalid_token = jwt.encode(payload, "wrong-secret", algorithm="HS256")
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)
    
    def test_verify_token_blacklisted(self, mock_redis):
        """Test verification of blacklisted token."""
        user_id = "test-user-123"
        role = "USER"
        
        token = AuthService.create_access_token(user_id, role)
        
        # Mock blacklisted token
        mock_redis.exists.return_value = True
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(token)
        
        assert exc_info.value.status_code == 401
        assert "Token has been revoked" in str(exc_info.value.detail)
    
    def test_verify_token_missing_user_id(self, mock_redis):
        """Test verification of token without user ID."""
        payload = {
            "role": "USER",
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "jti": "test-jti"
        }
        
        invalid_token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(invalid_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token payload" in str(exc_info.value.detail)
    
    def test_refresh_access_token_success(self, mock_redis):
        """Test successful token refresh."""
        user_id = "test-user-123"
        role = "USER"
        
        refresh_token = AuthService.create_refresh_token(user_id, role)
        result = AuthService.refresh_access_token(refresh_token)
        
        assert "access_token" in result
        assert "refresh_token" in result
        assert "token_type" in result
        assert result["token_type"] == "bearer"
        
        # Verify new access token is valid
        new_payload = AuthService.verify_token(result["access_token"])
        assert new_payload["sub"] == user_id
        assert new_payload["role"] == role
    
    def test_refresh_access_token_invalid_refresh_token(self, mock_redis):
        """Test token refresh with invalid refresh token."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create access token instead of refresh token
        access_token = AuthService.create_access_token(user_id, role)
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.refresh_access_token(access_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token type" in str(exc_info.value.detail)
    
    def test_blacklist_token_redis(self, mock_redis):
        """Test token blacklisting with Redis."""
        token_id = "test-token-id"
        expire_seconds = 3600
        
        AuthService.blacklist_token(token_id, expire_seconds)
        
        mock_redis.setex.assert_called_once_with(
            f"blacklist:{token_id}", 
            expire_seconds, 
            "true"
        )
    
    def test_blacklist_token_no_expiry(self, mock_redis):
        """Test token blacklisting without expiry."""
        token_id = "test-token-id"
        
        AuthService.blacklist_token(token_id)
        
        mock_redis.set.assert_called_once_with(
            f"blacklist:{token_id}", 
            "true"
        )
    
    def test_blacklist_token_fallback_storage(self):
        """Test token blacklisting with fallback in-memory storage."""
        with patch('Services.AuthService.AuthService._get_redis_client') as mock_get_redis:
            # Mock fallback to dict storage
            mock_storage = {}
            mock_get_redis.return_value = mock_storage
            
            token_id = "test-token-id"
            AuthService.blacklist_token(token_id)
            
            assert f"blacklist:{token_id}" in mock_storage
    
    def test_is_token_blacklisted_redis(self, mock_redis):
        """Test checking if token is blacklisted with Redis."""
        token_id = "test-token-id"
        
        # Test token is blacklisted
        mock_redis.exists.return_value = True
        assert AuthService._is_token_blacklisted(token_id) is True
        
        # Test token is not blacklisted
        mock_redis.exists.return_value = False
        assert AuthService._is_token_blacklisted(token_id) is False
    
    def test_is_token_blacklisted_fallback(self):
        """Test checking blacklisted token with fallback storage."""
        with patch('Services.AuthService.AuthService._get_redis_client') as mock_get_redis:
            mock_storage = {"blacklist:test-token": True}
            mock_get_redis.return_value = mock_storage
            
            assert AuthService._is_token_blacklisted("test-token") is True
            assert AuthService._is_token_blacklisted("other-token") is False
    
    def test_revoke_all_user_tokens(self, mock_redis):
        """Test revoking all tokens for a user."""
        user_id = "test-user-123"
        
        AuthService.revoke_all_user_tokens(user_id)
        
        mock_redis.set.assert_called_once()
        call_args = mock_redis.set.call_args
        assert call_args[0][0] == f"user_revoked:{user_id}"
        assert call_args[0][1] == "true"
    
    def test_get_user_id_from_token(self, mock_redis):
        """Test extracting user ID from token."""
        user_id = "test-user-123"
        role = "USER"
        
        token = AuthService.create_access_token(user_id, role)
        extracted_user_id = AuthService.get_user_id_from_token(token)
        
        assert extracted_user_id == user_id
    
    def test_get_user_role_from_token(self, mock_redis):
        """Test extracting user role from token."""
        user_id = "test-user-123"
        role = "ADMIN"
        
        token = AuthService.create_access_token(user_id, role)
        extracted_role = AuthService.get_user_role_from_token(token)
        
        assert extracted_role == role
    
    def test_get_user_role_from_token_default(self, mock_redis):
        """Test extracting user role with default value."""
        # Create token without role
        payload = {
            "sub": "test-user-123",
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "jti": "test-jti"
        }
        
        token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        extracted_role = AuthService.get_user_role_from_token(token)
        
        assert extracted_role == "USER"
    
    def test_decode_token_without_verification_success(self):
        """Test decoding token without verification."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create token with wrong secret (would normally fail verification)
        payload = {
            "sub": user_id,
            "role": role,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "jti": "test-jti"
        }
        
        token = jwt.encode(payload, "wrong-secret", algorithm="HS256")
        decoded = AuthService.decode_token_without_verification(token)
        
        assert decoded is not None
        assert decoded["sub"] == user_id
        assert decoded["role"] == role
    
    def test_decode_token_without_verification_invalid(self):
        """Test decoding invalid token without verification."""
        invalid_token = "invalid.token.here"
        decoded = AuthService.decode_token_without_verification(invalid_token)
        
        assert decoded is None
    
    @pytest.mark.security
    def test_token_security_features(self, mock_redis):
        """Test security features of tokens."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create multiple tokens
        token1 = AuthService.create_access_token(user_id, role)
        token2 = AuthService.create_access_token(user_id, role)
        
        # Tokens should be different (unique JTI)
        assert token1 != token2
        
        payload1 = jwt.decode(token1, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        payload2 = jwt.decode(token2, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        
        # JTI should be unique
        assert payload1["jti"] != payload2["jti"]
        
        # Both should have issued at time
        assert "iat" in payload1
        assert "iat" in payload2
    
    @pytest.mark.security
    def test_token_tampering_detection(self, mock_redis):
        """Test that token tampering is detected."""
        user_id = "test-user-123"
        role = "USER"
        
        token = AuthService.create_access_token(user_id, role)
        
        # Tamper with token by changing a character
        tampered_token = token[:-1] + ('a' if token[-1] != 'a' else 'b')
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(tampered_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)
    
    @pytest.mark.performance
    def test_token_creation_performance(self, mock_redis):
        """Test token creation performance."""
        import time
        
        user_id = "test-user-123"
        role = "USER"
        
        start_time = time.time()
        
        # Create 100 tokens
        for _ in range(100):
            AuthService.create_access_token(user_id, role)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should create 100 tokens in less than 1 second
        assert duration < 1.0
    
    @pytest.mark.performance
    def test_token_verification_performance(self, mock_redis):
        """Test token verification performance."""
        import time
        
        user_id = "test-user-123"
        role = "USER"
        
        # Create token
        token = AuthService.create_access_token(user_id, role)
        
        start_time = time.time()
        
        # Verify token 100 times
        for _ in range(100):
            AuthService.verify_token(token)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should verify 100 tokens in less than 1 second
        assert duration < 1.0
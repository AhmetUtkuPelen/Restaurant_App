"""
Security-focused tests for the chat application

Tests authentication, authorization, input validation, rate limiting,
and protection against common security vulnerabilities.
"""

import pytest
import time
from unittest.mock import patch, Mock
from fastapi import HTTPException

from Services.AuthService import AuthService
from Services.PasswordService import PasswordService
from Services.ValidationService import ValidationService
from Services.RateLimitService import RateLimitService


class TestAuthenticationSecurity:
    """Security tests for authentication mechanisms."""
    
    @pytest.mark.security
    def test_jwt_token_security_features(self, mock_redis):
        """Test JWT token security features."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create token
        token = AuthService.create_access_token(user_id, role)
        
        # Verify token contains security features
        payload = AuthService.decode_token_without_verification(token)
        
        assert "jti" in payload  # JWT ID for blacklisting
        assert "iat" in payload  # Issued at time
        assert "exp" in payload  # Expiration time
        assert payload["type"] == "access"  # Token type
        
        # Verify expiration is set
        import datetime
        exp_time = datetime.datetime.fromtimestamp(payload["exp"])
        now = datetime.datetime.utcnow()
        assert exp_time > now  # Token should not be expired
    
    @pytest.mark.security
    def test_token_blacklisting_security(self, mock_redis):
        """Test token blacklisting prevents reuse."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create and verify token
        token = AuthService.create_access_token(user_id, role)
        payload = AuthService.verify_token(token)
        token_id = payload["jti"]
        
        # Blacklist token
        AuthService.blacklist_token(token_id)
        mock_redis.exists.return_value = True
        
        # Token should now be rejected
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(token)
        
        assert exc_info.value.status_code == 401
        assert "revoked" in str(exc_info.value.detail)
    
    @pytest.mark.security
    def test_refresh_token_security(self, mock_redis):
        """Test refresh token security features."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create refresh token
        refresh_token = AuthService.create_refresh_token(user_id, role)
        
        # Verify it's a refresh token
        payload = AuthService.verify_token(refresh_token, "refresh")
        assert payload["type"] == "refresh"
        
        # Use refresh token to get new access token
        result = AuthService.refresh_access_token(refresh_token)
        
        assert "access_token" in result
        assert "refresh_token" in result
        
        # Old refresh token should be blacklisted
        mock_redis.setex.assert_called()
    
    @pytest.mark.security
    def test_token_tampering_detection(self, mock_redis):
        """Test detection of token tampering."""
        user_id = "test-user-123"
        role = "USER"
        
        token = AuthService.create_access_token(user_id, role)
        
        # Tamper with token
        tampered_token = token[:-5] + "XXXXX"
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(tampered_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)
    
    @pytest.mark.security
    def test_token_type_validation(self, mock_redis):
        """Test token type validation prevents misuse."""
        user_id = "test-user-123"
        role = "USER"
        
        access_token = AuthService.create_access_token(user_id, role)
        refresh_token = AuthService.create_refresh_token(user_id, role)
        
        # Access token should not work as refresh token
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(access_token, "refresh")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token type" in str(exc_info.value.detail)
        
        # Refresh token should not work as access token
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(refresh_token, "access")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token type" in str(exc_info.value.detail)


class TestPasswordSecurity:
    """Security tests for password handling."""
    
    @pytest.mark.security
    def test_password_hashing_security(self):
        """Test password hashing security features."""
        password = "TestPassword123!"
        
        # Hash password
        hashed = PasswordService.hash_password(password)
        
        # Verify it's a proper bcrypt hash
        assert hashed.startswith('$2b$')
        
        # Verify original password is not in hash
        assert password not in hashed
        
        # Verify hash is different each time (salt)
        hashed2 = PasswordService.hash_password(password)
        assert hashed != hashed2
        
        # But both should verify correctly
        assert PasswordService.verify_password(password, hashed)
        assert PasswordService.verify_password(password, hashed2)
    
    @pytest.mark.security
    def test_password_strength_validation(self):
        """Test password strength validation security."""
        # Test weak passwords are rejected
        weak_passwords = [
            "123456",
            "password",
            "qwerty",
            "abc123",
            "admin",
            "letmein",
            "welcome",
            "monkey"
        ]
        
        for weak_password in weak_passwords:
            result = PasswordService.validate_password_strength(weak_password)
            assert result["is_valid"] is False
            assert result["strength"] == "Weak"
    
    @pytest.mark.security
    def test_password_common_patterns_detection(self):
        """Test detection of common password patterns."""
        common_patterns = [
            "password123",
            "123456789",
            "qwerty123",
            "admin123"
        ]
        
        for pattern in common_patterns:
            result = PasswordService.validate_password_strength(pattern)
            assert any("common patterns" in error for error in result["errors"])
    
    @pytest.mark.security
    def test_password_sequential_detection(self):
        """Test detection of sequential characters."""
        sequential_passwords = [
            "Test123456!",  # Sequential numbers
            "Testabcdef!",  # Sequential letters
            "Pass234567!"   # Sequential numbers
        ]
        
        for password in sequential_passwords:
            result = PasswordService.validate_password_strength(password)
            assert any("sequential" in error for error in result["errors"])
    
    @pytest.mark.security
    def test_password_verification_timing_attack_resistance(self):
        """Test password verification timing attack resistance."""
        password = "TestPassword123!"
        hashed = PasswordService.hash_password(password)
        
        # Measure verification times
        times_correct = []
        times_incorrect = []
        
        for _ in range(5):
            start = time.time()
            PasswordService.verify_password(password, hashed)
            times_correct.append(time.time() - start)
            
            start = time.time()
            PasswordService.verify_password("WrongPassword123!", hashed)
            times_incorrect.append(time.time() - start)
        
        # Times should be similar (bcrypt provides this naturally)
        avg_correct = sum(times_correct) / len(times_correct)
        avg_incorrect = sum(times_incorrect) / len(times_incorrect)
        
        # Ratio should be close to 1 (similar times)
        ratio = max(avg_correct, avg_incorrect) / min(avg_correct, avg_incorrect)
        assert ratio < 2.0


class TestInputValidationSecurity:
    """Security tests for input validation and sanitization."""
    
    @pytest.mark.security
    def test_xss_prevention(self, xss_payloads):
        """Test XSS prevention in HTML sanitization."""
        for payload in xss_payloads:
            sanitized = ValidationService.sanitize_html(payload)
            
            # Should not contain dangerous elements
            dangerous_patterns = [
                "<script>",
                "javascript:",
                "onerror=",
                "onload=",
                "onclick=",
                "onmouseover=",
                "<iframe",
                "vbscript:",
                "data:text/html"
            ]
            
            for pattern in dangerous_patterns:
                assert pattern.lower() not in sanitized.lower()
    
    @pytest.mark.security
    def test_sql_injection_detection(self, sql_injection_payloads):
        """Test SQL injection pattern detection."""
        for payload in sql_injection_payloads:
            result = ValidationService.check_sql_injection(payload)
            assert result["is_safe"] is False
            assert len(result["detected_patterns"]) > 0
    
    @pytest.mark.security
    def test_file_upload_security_validation(self):
        """Test file upload security validation."""
        # Test dangerous file types
        dangerous_files = [
            ("malware.exe", b"MZ\x90\x00", "application/octet-stream"),
            ("script.js", b"alert('xss')", "application/javascript"),
            ("shell.php", b"<?php system($_GET['cmd']); ?>", "application/x-php"),
            ("batch.bat", b"@echo off\ndel /f /q *.*", "application/x-msdos-program")
        ]
        
        with patch('config.settings') as mock_settings:
            mock_settings.max_file_size = 1024 * 1024
            mock_settings.allowed_file_types_list = ['.txt', '.pdf', '.jpg']
            
            for filename, content, content_type in dangerous_files:
                from fastapi import UploadFile
                import io
                
                file = UploadFile(
                    filename=filename,
                    file=io.BytesIO(content),
                    content_type=content_type
                )
                
                result = ValidationService.validate_file_upload(file)
                assert result["is_valid"] is False
                assert any("not allowed" in error for error in result["errors"])
    
    @pytest.mark.security
    def test_filename_security_validation(self):
        """Test filename security validation."""
        dangerous_filenames = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32\\config",
            "file<script>.txt",
            "file|pipe.txt",
            "CON.txt",  # Windows reserved name
            "file\x00.txt",  # Null byte
            "file?query.txt"
        ]
        
        for filename in dangerous_filenames:
            result = ValidationService.validate_filename(filename)
            assert result["is_valid"] is False
    
    @pytest.mark.security
    def test_message_content_security_validation(self, xss_payloads):
        """Test message content security validation."""
        for payload in xss_payloads:
            result = ValidationService.validate_message_content(payload)
            
            if result["is_valid"]:
                # Content should be sanitized
                sanitized = result["sanitized_content"]
                assert "<script>" not in sanitized.lower()
                assert "javascript:" not in sanitized.lower()
    
    @pytest.mark.security
    def test_username_security_validation(self):
        """Test username security validation."""
        malicious_usernames = [
            "admin",  # Reserved
            "root",   # Reserved
            "user<script>",  # XSS attempt
            "user'; DROP TABLE users; --",  # SQL injection attempt
            "../admin",  # Path traversal attempt
            "user\x00admin"  # Null byte injection
        ]
        
        for username in malicious_usernames:
            result = ValidationService.validate_username(username)
            assert result["is_valid"] is False
    
    @pytest.mark.security
    def test_email_security_validation(self):
        """Test email security validation."""
        malicious_emails = [
            "user@example.com<script>alert('xss')</script>",
            "user'; DROP TABLE users; --@example.com",
            "user@example.com\x00@malicious.com",
            "user@" + "a" * 300 + ".com",  # Extremely long domain
        ]
        
        for email in malicious_emails:
            result = ValidationService.validate_email_address(email)
            assert result["is_valid"] is False


class TestRateLimitingSecurity:
    """Security tests for rate limiting functionality."""
    
    @pytest.mark.security
    def test_rate_limiting_basic_functionality(self):
        """Test basic rate limiting functionality."""
        user_id = "test-user-123"
        endpoint = "login"
        
        with patch('Services.RateLimitService.RateLimitService._get_redis_client') as mock_redis:
            mock_client = Mock()
            mock_client.get.return_value = None  # No existing counter
            mock_client.setex.return_value = True
            mock_redis.return_value = mock_client
            
            # First request should be allowed
            assert RateLimitService.check_rate_limit(user_id, endpoint) is True
            
            # Increment counter
            RateLimitService.increment_counter(user_id, endpoint)
    
    @pytest.mark.security
    def test_rate_limiting_prevents_brute_force(self):
        """Test rate limiting prevents brute force attacks."""
        user_id = "test-user-123"
        endpoint = "login"
        
        with patch('Services.RateLimitService.RateLimitService._get_redis_client') as mock_redis:
            mock_client = Mock()
            
            # Simulate hitting rate limit
            mock_client.get.return_value = b"10"  # Already at limit
            mock_redis.return_value = mock_client
            
            # Should be rate limited
            assert RateLimitService.check_rate_limit(user_id, endpoint) is False
    
    @pytest.mark.security
    def test_rate_limiting_per_endpoint(self):
        """Test rate limiting is applied per endpoint."""
        user_id = "test-user-123"
        
        with patch('Services.RateLimitService.RateLimitService._get_redis_client') as mock_redis:
            mock_client = Mock()
            mock_client.get.return_value = None
            mock_client.setex.return_value = True
            mock_redis.return_value = mock_client
            
            # Different endpoints should have separate limits
            assert RateLimitService.check_rate_limit(user_id, "login") is True
            assert RateLimitService.check_rate_limit(user_id, "register") is True
            assert RateLimitService.check_rate_limit(user_id, "message") is True


class TestAuthorizationSecurity:
    """Security tests for authorization and access control."""
    
    @pytest.mark.security
    def test_role_based_access_control(self, mock_redis):
        """Test role-based access control in tokens."""
        # Create tokens with different roles
        admin_token = AuthService.create_access_token("admin-user", "ADMIN")
        user_token = AuthService.create_access_token("regular-user", "USER")
        
        # Verify roles are correctly embedded
        admin_payload = AuthService.verify_token(admin_token)
        user_payload = AuthService.verify_token(user_token)
        
        assert admin_payload["role"] == "ADMIN"
        assert user_payload["role"] == "USER"
        
        # Extract roles using service method
        assert AuthService.get_user_role_from_token(admin_token) == "ADMIN"
        assert AuthService.get_user_role_from_token(user_token) == "USER"
    
    @pytest.mark.security
    def test_user_isolation(self, mock_redis):
        """Test that users can only access their own data."""
        user1_id = "user-1"
        user2_id = "user-2"
        
        user1_token = AuthService.create_access_token(user1_id, "USER")
        user2_token = AuthService.create_access_token(user2_id, "USER")
        
        # Verify tokens contain correct user IDs
        assert AuthService.get_user_id_from_token(user1_token) == user1_id
        assert AuthService.get_user_id_from_token(user2_token) == user2_id
        
        # Users should not be able to use each other's tokens
        user1_payload = AuthService.verify_token(user1_token)
        user2_payload = AuthService.verify_token(user2_token)
        
        assert user1_payload["sub"] != user2_payload["sub"]


class TestSessionSecurity:
    """Security tests for session management."""
    
    @pytest.mark.security
    def test_session_invalidation(self, mock_redis):
        """Test session invalidation and token revocation."""
        user_id = "test-user-123"
        role = "USER"
        
        # Create token
        token = AuthService.create_access_token(user_id, role)
        payload = AuthService.verify_token(token)
        token_id = payload["jti"]
        
        # Revoke all user tokens
        AuthService.revoke_all_user_tokens(user_id)
        
        # Should set revocation flag
        mock_redis.set.assert_called()
        call_args = mock_redis.set.call_args
        assert call_args[0][0] == f"user_revoked:{user_id}"
    
    @pytest.mark.security
    def test_token_expiration_security(self, mock_redis):
        """Test token expiration handling."""
        from datetime import timedelta
        
        user_id = "test-user-123"
        role = "USER"
        
        # Create token with very short expiry
        short_expiry = timedelta(seconds=-1)  # Already expired
        expired_token = AuthService.create_access_token(user_id, role, short_expiry)
        
        # Should reject expired token
        with pytest.raises(HTTPException) as exc_info:
            AuthService.verify_token(expired_token)
        
        assert exc_info.value.status_code == 401
        assert "expired" in str(exc_info.value.detail).lower()


class TestCryptographicSecurity:
    """Security tests for cryptographic operations."""
    
    @pytest.mark.security
    def test_secure_random_generation(self):
        """Test secure random generation for passwords."""
        # Generate multiple passwords
        passwords = [PasswordService.generate_secure_password() for _ in range(10)]
        
        # All should be unique (extremely high probability)
        assert len(set(passwords)) == len(passwords)
        
        # All should meet security requirements
        for password in passwords:
            result = PasswordService.validate_password_strength(password)
            assert result["is_valid"] is True
            assert result["strength"] == "Strong"
    
    @pytest.mark.security
    def test_salt_uniqueness(self):
        """Test that password salts are unique."""
        password = "TestPassword123!"
        
        # Hash same password multiple times
        hashes = [PasswordService.hash_password(password) for _ in range(10)]
        
        # All hashes should be different due to unique salts
        assert len(set(hashes)) == len(hashes)
        
        # But all should verify against original password
        for hash_value in hashes:
            assert PasswordService.verify_password(password, hash_value)


class TestSecurityHeaders:
    """Security tests for HTTP security headers."""
    
    @pytest.mark.security
    def test_cors_configuration(self, client):
        """Test CORS configuration security."""
        response = client.options("/users/register")
        
        # Should have CORS headers
        headers = response.headers
        
        # Check for security-relevant CORS headers
        if "access-control-allow-origin" in headers:
            origin = headers["access-control-allow-origin"]
            # Should not be wildcard for credentials
            if "access-control-allow-credentials" in headers:
                assert origin != "*"
    
    @pytest.mark.security
    def test_error_information_disclosure(self, client):
        """Test that errors don't disclose sensitive information."""
        # Test with invalid endpoint
        response = client.get("/nonexistent")
        assert response.status_code == 404
        
        # Error should not contain sensitive information
        if response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
            error_text = str(data).lower()
            
            # Should not contain sensitive paths or information
            sensitive_patterns = [
                "/home/",
                "/usr/",
                "/var/",
                "c:\\",
                "database",
                "password",
                "secret",
                "key"
            ]
            
            for pattern in sensitive_patterns:
                assert pattern not in error_text


class TestSecurityAuditLog:
    """Security tests for audit logging."""
    
    @pytest.mark.security
    def test_security_event_logging(self, db_session):
        """Test that security events are logged."""
        from Models.database_models import AuditLogDB
        
        # Create a security audit log entry
        audit_log = AuditLogDB.create_log(
            db=db_session,
            user_id="test-user",
            action="login_failed",
            resource_type="user",
            resource_id="test-user",
            details={"reason": "invalid_password"},
            ip_address="192.168.1.1",
            success=False,
            risk_level="medium"
        )
        
        assert audit_log.action == "login_failed"
        assert audit_log.success is False
        assert audit_log.risk_level == "medium"
    
    @pytest.mark.security
    def test_failed_login_tracking(self, db_session):
        """Test tracking of failed login attempts."""
        from Models.database_models import AuditLogDB
        
        user_id = "test-user"
        ip_address = "192.168.1.1"
        
        # Create multiple failed login attempts
        for i in range(3):
            AuditLogDB.create_log(
                db=db_session,
                user_id=user_id,
                action="login",
                resource_type="user",
                resource_id=user_id,
                ip_address=ip_address,
                success=False,
                risk_level="medium"
            )
        
        # Get failed attempts
        failed_attempts = AuditLogDB.get_failed_attempts(db_session, user_id=user_id)
        assert len(failed_attempts) == 3
        
        # Get failed attempts by IP
        failed_by_ip = AuditLogDB.get_failed_attempts(db_session, ip_address=ip_address)
        assert len(failed_by_ip) == 3
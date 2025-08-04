"""
Unit tests for PasswordService

Tests password hashing, verification, strength validation, and secure password generation.
Includes security-focused tests for password policies and edge cases.
"""

import pytest
import bcrypt
from unittest.mock import patch

from Services.PasswordService import PasswordService


class TestPasswordService:
    """Test cases for PasswordService functionality."""
    
    def test_hash_password_success(self):
        """Test successful password hashing."""
        password = "TestPassword123!"
        hashed = PasswordService.hash_password(password)
        
        # Verify hash is created
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        
        # Verify it's a valid bcrypt hash
        assert hashed.startswith('$2b$')
        
        # Verify original password is not in hash
        assert password not in hashed
    
    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)."""
        password = "TestPassword123!"
        
        hash1 = PasswordService.hash_password(password)
        hash2 = PasswordService.hash_password(password)
        
        # Hashes should be different due to different salts
        assert hash1 != hash2
        
        # But both should verify against the original password
        assert PasswordService.verify_password(password, hash1)
        assert PasswordService.verify_password(password, hash2)
    
    def test_verify_password_success(self):
        """Test successful password verification."""
        password = "TestPassword123!"
        hashed = PasswordService.hash_password(password)
        
        # Correct password should verify
        assert PasswordService.verify_password(password, hashed) is True
    
    def test_verify_password_failure(self):
        """Test password verification failure."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = PasswordService.hash_password(password)
        
        # Wrong password should not verify
        assert PasswordService.verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty_password(self):
        """Test password verification with empty password."""
        hashed = PasswordService.hash_password("TestPassword123!")
        
        assert PasswordService.verify_password("", hashed) is False
        assert PasswordService.verify_password(None, hashed) is False
    
    def test_verify_password_invalid_hash(self):
        """Test password verification with invalid hash."""
        password = "TestPassword123!"
        invalid_hash = "invalid_hash"
        
        # Should return False for invalid hash, not raise exception
        assert PasswordService.verify_password(password, invalid_hash) is False
    
    def test_verify_password_exception_handling(self):
        """Test password verification exception handling."""
        password = "TestPassword123!"
        
        # Test with None hash
        assert PasswordService.verify_password(password, None) is False
        
        # Test with empty hash
        assert PasswordService.verify_password(password, "") is False
    
    def test_validate_password_strength_strong(self):
        """Test validation of strong password."""
        strong_password = "MyStr0ng!P@ssw0rd"
        result = PasswordService.validate_password_strength(strong_password)
        
        assert result["is_valid"] is True
        assert result["strength"] == "Strong"
        assert result["score"] >= 5
        assert len(result["errors"]) == 0
        assert isinstance(result["suggestions"], list)
    
    def test_validate_password_strength_medium(self):
        """Test validation of medium strength password."""
        medium_password = "TestPass123"
        result = PasswordService.validate_password_strength(medium_password)
        
        assert result["strength"] in ["Medium", "Strong"]
        assert result["score"] >= 3
    
    def test_validate_password_strength_weak(self):
        """Test validation of weak password."""
        weak_password = "123456"
        result = PasswordService.validate_password_strength(weak_password)
        
        assert result["is_valid"] is False
        assert result["strength"] == "Weak"
        assert result["score"] < 3
        assert len(result["errors"]) > 0
    
    def test_validate_password_strength_too_short(self):
        """Test validation of password that's too short."""
        short_password = "Abc1!"
        result = PasswordService.validate_password_strength(short_password)
        
        assert result["is_valid"] is False
        assert any("8 characters" in error for error in result["errors"])
    
    def test_validate_password_strength_no_uppercase(self):
        """Test validation of password without uppercase letters."""
        no_upper = "testpassword123!"
        result = PasswordService.validate_password_strength(no_upper)
        
        assert result["is_valid"] is False
        assert any("uppercase" in error for error in result["errors"])
    
    def test_validate_password_strength_no_lowercase(self):
        """Test validation of password without lowercase letters."""
        no_lower = "TESTPASSWORD123!"
        result = PasswordService.validate_password_strength(no_lower)
        
        assert result["is_valid"] is False
        assert any("lowercase" in error for error in result["errors"])
    
    def test_validate_password_strength_no_numbers(self):
        """Test validation of password without numbers."""
        no_numbers = "TestPassword!"
        result = PasswordService.validate_password_strength(no_numbers)
        
        assert result["is_valid"] is False
        assert any("number" in error for error in result["errors"])
    
    def test_validate_password_strength_no_special_chars(self):
        """Test validation of password without special characters."""
        no_special = "TestPassword123"
        result = PasswordService.validate_password_strength(no_special)
        
        assert result["is_valid"] is False
        assert any("special character" in error for error in result["errors"])
    
    def test_validate_password_strength_common_patterns(self):
        """Test validation of passwords with common patterns."""
        common_passwords = [
            "password123",
            "123456789",
            "qwerty123",
            "admin123",
            "letmein123"
        ]
        
        for password in common_passwords:
            result = PasswordService.validate_password_strength(password)
            # Should have errors about common patterns
            assert any("common patterns" in error for error in result["errors"])
    
    def test_validate_password_strength_sequential_numbers(self):
        """Test validation of passwords with sequential numbers."""
        sequential_passwords = [
            "Test123456!",
            "Pass234567!",
            "Word345678!"
        ]
        
        for password in sequential_passwords:
            result = PasswordService.validate_password_strength(password)
            assert any("sequential numbers" in error for error in result["errors"])
    
    def test_validate_password_strength_sequential_letters(self):
        """Test validation of passwords with sequential letters."""
        sequential_passwords = [
            "Testabcd123!",
            "Passbcde123!",
            "Wordefgh123!"
        ]
        
        for password in sequential_passwords:
            result = PasswordService.validate_password_strength(password)
            assert any("sequential letters" in error for error in result["errors"])
    
    def test_validate_password_strength_long_password_bonus(self):
        """Test that longer passwords get bonus points."""
        short_valid = "Test123!"  # 8 chars
        long_valid = "TestPassword123!"  # 16 chars
        
        short_result = PasswordService.validate_password_strength(short_valid)
        long_result = PasswordService.validate_password_strength(long_valid)
        
        # Longer password should have higher score
        assert long_result["score"] > short_result["score"]
    
    def test_get_password_suggestions(self):
        """Test password improvement suggestions."""
        weak_password = "test"
        result = PasswordService.validate_password_strength(weak_password)
        
        suggestions = result["suggestions"]
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        
        # Should contain helpful suggestions
        suggestion_text = " ".join(suggestions).lower()
        assert "characters" in suggestion_text or "length" in suggestion_text
    
    def test_generate_secure_password_default_length(self):
        """Test secure password generation with default length."""
        password = PasswordService.generate_secure_password()
        
        assert isinstance(password, str)
        assert len(password) == 16  # Default length
        
        # Verify it meets strength requirements
        result = PasswordService.validate_password_strength(password)
        assert result["is_valid"] is True
        assert result["strength"] == "Strong"
    
    def test_generate_secure_password_custom_length(self):
        """Test secure password generation with custom length."""
        length = 20
        password = PasswordService.generate_secure_password(length)
        
        assert len(password) == length
        
        # Verify it meets strength requirements
        result = PasswordService.validate_password_strength(password)
        assert result["is_valid"] is True
        assert result["strength"] == "Strong"
    
    def test_generate_secure_password_minimum_length(self):
        """Test secure password generation with length below minimum."""
        # Request length below minimum (12)
        password = PasswordService.generate_secure_password(8)
        
        # Should use minimum length of 12
        assert len(password) >= 12
    
    def test_generate_secure_password_character_requirements(self):
        """Test that generated password meets character requirements."""
        password = PasswordService.generate_secure_password()
        
        # Check for required character types
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        assert has_lower, "Generated password should contain lowercase letters"
        assert has_upper, "Generated password should contain uppercase letters"
        assert has_digit, "Generated password should contain digits"
        assert has_special, "Generated password should contain special characters"
    
    def test_generate_secure_password_uniqueness(self):
        """Test that generated passwords are unique."""
        passwords = [PasswordService.generate_secure_password() for _ in range(10)]
        
        # All passwords should be unique
        assert len(set(passwords)) == len(passwords)
    
    @pytest.mark.security
    def test_password_hashing_security(self):
        """Test security aspects of password hashing."""
        password = "TestPassword123!"
        
        # Test that hash uses proper bcrypt rounds
        hashed = PasswordService.hash_password(password)
        
        # Extract rounds from hash
        parts = hashed.split('$')
        rounds = int(parts[2])
        
        # Should use configured rounds (default 12)
        assert rounds >= 10, "Bcrypt rounds should be at least 10 for security"
    
    @pytest.mark.security
    def test_timing_attack_resistance(self):
        """Test that password verification is resistant to timing attacks."""
        import time
        
        password = "TestPassword123!"
        hashed = PasswordService.hash_password(password)
        
        # Test verification times for correct and incorrect passwords
        times_correct = []
        times_incorrect = []
        
        for _ in range(10):
            # Time correct password verification
            start = time.time()
            PasswordService.verify_password(password, hashed)
            times_correct.append(time.time() - start)
            
            # Time incorrect password verification
            start = time.time()
            PasswordService.verify_password("WrongPassword123!", hashed)
            times_incorrect.append(time.time() - start)
        
        # Average times should be similar (within reasonable variance)
        avg_correct = sum(times_correct) / len(times_correct)
        avg_incorrect = sum(times_incorrect) / len(times_incorrect)
        
        # Times should be in similar range (bcrypt naturally provides this)
        ratio = max(avg_correct, avg_incorrect) / min(avg_correct, avg_incorrect)
        assert ratio < 2.0, "Verification times should be similar to prevent timing attacks"
    
    @pytest.mark.performance
    def test_password_hashing_performance(self):
        """Test password hashing performance."""
        import time
        
        password = "TestPassword123!"
        
        start_time = time.time()
        
        # Hash 10 passwords
        for _ in range(10):
            PasswordService.hash_password(password)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time (bcrypt is intentionally slow)
        assert duration < 10.0, "Password hashing should complete in reasonable time"
        assert duration > 0.1, "Password hashing should take some time for security"
    
    @pytest.mark.performance
    def test_password_verification_performance(self):
        """Test password verification performance."""
        import time
        
        password = "TestPassword123!"
        hashed = PasswordService.hash_password(password)
        
        start_time = time.time()
        
        # Verify 10 passwords
        for _ in range(10):
            PasswordService.verify_password(password, hashed)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time
        assert duration < 10.0, "Password verification should complete in reasonable time"
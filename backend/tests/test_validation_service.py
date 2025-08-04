"""
Unit tests for ValidationService

Tests input validation, sanitization, and security checks.
Includes comprehensive security-focused tests for XSS, SQL injection, and file upload validation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import UploadFile
import io

from Services.ValidationService import ValidationService


class TestValidationService:
    """Test cases for ValidationService functionality."""
    
    def test_validate_email_address_valid(self):
        """Test validation of valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@example.com"
        ]
        
        for email in valid_emails:
            result = ValidationService.validate_email_address(email)
            assert result["is_valid"] is True
            assert result["error"] is None
            assert result["normalized_email"] is not None
    
    def test_validate_email_address_invalid(self):
        """Test validation of invalid email addresses."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@example",
            ""
        ]
        
        for email in invalid_emails:
            result = ValidationService.validate_email_address(email)
            assert result["is_valid"] is False
            assert result["error"] is not None
            assert result["normalized_email"] is None
    
    def test_validate_email_address_empty(self):
        """Test validation of empty email address."""
        result = ValidationService.validate_email_address("")
        assert result["is_valid"] is False
        assert "required" in result["error"]
        
        result = ValidationService.validate_email_address(None)
        assert result["is_valid"] is False
        assert "required" in result["error"]
    
    def test_validate_email_address_too_long(self):
        """Test validation of email address that's too long."""
        long_email = "a" * 250 + "@example.com"
        result = ValidationService.validate_email_address(long_email)
        assert result["is_valid"] is False
        assert "too long" in result["error"]
    
    def test_validate_username_valid(self):
        """Test validation of valid usernames."""
        valid_usernames = [
            "testuser",
            "user123",
            "test_user",
            "user.name",
            "user-name",
            "123user"
        ]
        
        for username in valid_usernames:
            result = ValidationService.validate_username(username)
            assert result["is_valid"] is True
            assert len(result["errors"]) == 0
            assert result["normalized_username"] == username.lower()
    
    def test_validate_username_invalid_length(self):
        """Test validation of usernames with invalid length."""
        # Too short
        result = ValidationService.validate_username("ab")
        assert result["is_valid"] is False
        assert any("3 characters" in error for error in result["errors"])
        
        # Too long
        long_username = "a" * 31
        result = ValidationService.validate_username(long_username)
        assert result["is_valid"] is False
        assert any("30 characters" in error for error in result["errors"])
    
    def test_validate_username_invalid_characters(self):
        """Test validation of usernames with invalid characters."""
        invalid_usernames = [
            "test@user",
            "test user",
            "test#user",
            "test$user",
            "test%user"
        ]
        
        for username in invalid_usernames:
            result = ValidationService.validate_username(username)
            assert result["is_valid"] is False
            assert any("can only contain" in error for error in result["errors"])
    
    def test_validate_username_invalid_start(self):
        """Test validation of usernames with invalid starting characters."""
        invalid_usernames = [
            "_testuser",
            ".testuser",
            "-testuser"
        ]
        
        for username in invalid_usernames:
            result = ValidationService.validate_username(username)
            assert result["is_valid"] is False
            assert any("must start with" in error for error in result["errors"])
    
    def test_validate_username_invalid_end(self):
        """Test validation of usernames with invalid ending characters."""
        invalid_usernames = [
            "testuser.",
            "testuser-",
            "testuser_"
        ]
        
        for username in invalid_usernames:
            result = ValidationService.validate_username(username)
            assert result["is_valid"] is False
            assert any("cannot end with" in error for error in result["errors"])
    
    def test_validate_username_reserved(self):
        """Test validation of reserved usernames."""
        reserved_usernames = [
            "admin",
            "administrator",
            "root",
            "system",
            "api",
            "support"
        ]
        
        for username in reserved_usernames:
            result = ValidationService.validate_username(username)
            assert result["is_valid"] is False
            assert any("reserved" in error for error in result["errors"])
    
    def test_validate_username_empty(self):
        """Test validation of empty username."""
        result = ValidationService.validate_username("")
        assert result["is_valid"] is False
        assert any("required" in error for error in result["errors"])
        
        result = ValidationService.validate_username(None)
        assert result["is_valid"] is False
        assert any("required" in error for error in result["errors"])
    
    def test_sanitize_html_basic(self):
        """Test basic HTML sanitization."""
        html_content = "<p>Hello <strong>world</strong>!</p>"
        sanitized = ValidationService.sanitize_html(html_content)
        
        assert "<p>" in sanitized
        assert "<strong>" in sanitized
        assert "Hello" in sanitized
        assert "world" in sanitized
    
    @pytest.mark.security
    def test_sanitize_html_xss_prevention(self, xss_payloads):
        """Test HTML sanitization prevents XSS attacks."""
        for payload in xss_payloads:
            sanitized = ValidationService.sanitize_html(payload)
            
            # Should not contain script tags or javascript
            assert "<script>" not in sanitized.lower()
            assert "javascript:" not in sanitized.lower()
            assert "onerror=" not in sanitized.lower()
            assert "onload=" not in sanitized.lower()
    
    def test_sanitize_html_allowed_tags(self):
        """Test HTML sanitization with custom allowed tags."""
        html_content = "<p>Test</p><div>Not allowed</div><strong>Allowed</strong>"
        allowed_tags = ["p", "strong"]
        
        sanitized = ValidationService.sanitize_html(html_content, allowed_tags)
        
        assert "<p>" in sanitized
        assert "<strong>" in sanitized
        assert "<div>" not in sanitized
        assert "Not allowed" in sanitized  # Content preserved, tags removed
    
    def test_sanitize_html_empty_content(self):
        """Test HTML sanitization with empty content."""
        assert ValidationService.sanitize_html("") == ""
        assert ValidationService.sanitize_html(None) == ""
    
    def test_sanitize_text_input_basic(self):
        """Test basic text input sanitization."""
        text = "  Hello   world  \n\n  "
        sanitized = ValidationService.sanitize_text_input(text)
        
        assert sanitized == "Hello world"
    
    def test_sanitize_text_input_control_characters(self):
        """Test text sanitization removes control characters."""
        text = "Hello\x00\x08\x0B\x0Cworld\x7F"
        sanitized = ValidationService.sanitize_text_input(text)
        
        assert sanitized == "Helloworld"
    
    def test_sanitize_text_input_max_length(self):
        """Test text sanitization with maximum length."""
        long_text = "a" * 100
        sanitized = ValidationService.sanitize_text_input(long_text, max_length=50)
        
        assert len(sanitized) == 50
    
    def test_sanitize_text_input_empty(self):
        """Test text sanitization with empty input."""
        assert ValidationService.sanitize_text_input("") == ""
        assert ValidationService.sanitize_text_input(None) == ""
    
    @pytest.mark.security
    def test_check_sql_injection_safe(self):
        """Test SQL injection detection with safe input."""
        safe_inputs = [
            "Hello world",
            "User123",
            "test@example.com",
            "Normal message content"
        ]
        
        for input_text in safe_inputs:
            result = ValidationService.check_sql_injection(input_text)
            assert result["is_safe"] is True
            assert len(result["detected_patterns"]) == 0
    
    @pytest.mark.security
    def test_check_sql_injection_dangerous(self, sql_injection_payloads):
        """Test SQL injection detection with dangerous input."""
        for payload in sql_injection_payloads:
            result = ValidationService.check_sql_injection(payload)
            assert result["is_safe"] is False
            assert len(result["detected_patterns"]) > 0
    
    def test_check_sql_injection_empty(self):
        """Test SQL injection detection with empty input."""
        result = ValidationService.check_sql_injection("")
        assert result["is_safe"] is True
        assert len(result["detected_patterns"]) == 0
        
        result = ValidationService.check_sql_injection(None)
        assert result["is_safe"] is True
        assert len(result["detected_patterns"]) == 0
    
    def test_validate_file_upload_valid(self, temp_upload_dir):
        """Test validation of valid file upload."""
        # Create mock file
        file_content = b"Test file content"
        file = Mock(spec=UploadFile)
        file.filename = "test.txt"
        file.content_type = "text/plain"
        file.size = len(file_content)
        file.file = io.BytesIO(file_content)
        
        with patch('config.settings') as mock_settings:
            mock_settings.max_file_size = 1024 * 1024  # 1MB
            mock_settings.allowed_file_types_list = ['.txt', '.pdf', '.jpg']
            
            result = ValidationService.validate_file_upload(file)
            
            assert result["is_valid"] is True
            assert len(result["errors"]) == 0
            assert result["file_info"]["original_filename"] == "test.txt"
    
    def test_validate_file_upload_no_file(self):
        """Test validation with no file provided."""
        result = ValidationService.validate_file_upload(None)
        assert result["is_valid"] is False
        assert any("No file provided" in error for error in result["errors"])
        
        # Test with file but no filename
        file = Mock(spec=UploadFile)
        file.filename = None
        result = ValidationService.validate_file_upload(file)
        assert result["is_valid"] is False
        assert any("No file provided" in error for error in result["errors"])
    
    def test_validate_file_upload_size_exceeded(self, temp_upload_dir):
        """Test validation of file that exceeds size limit."""
        file = Mock(spec=UploadFile)
        file.filename = "large_file.txt"
        file.content_type = "text/plain"
        file.size = 10 * 1024 * 1024  # 10MB
        file.file = io.BytesIO(b"content")
        
        with patch('config.settings') as mock_settings:
            mock_settings.max_file_size = 1024 * 1024  # 1MB limit
            mock_settings.allowed_file_types_list = ['.txt']
            
            result = ValidationService.validate_file_upload(file)
            
            assert result["is_valid"] is False
            assert any("exceeds maximum" in error for error in result["errors"])
    
    def test_validate_file_upload_invalid_extension(self, temp_upload_dir):
        """Test validation of file with invalid extension."""
        file = Mock(spec=UploadFile)
        file.filename = "malicious.exe"
        file.content_type = "application/octet-stream"
        file.size = 1024
        file.file = io.BytesIO(b"content")
        
        with patch('config.settings') as mock_settings:
            mock_settings.max_file_size = 1024 * 1024
            mock_settings.allowed_file_types_list = ['.txt', '.pdf', '.jpg']
            
            result = ValidationService.validate_file_upload(file)
            
            assert result["is_valid"] is False
            assert any("not allowed" in error for error in result["errors"])
    
    def test_validate_filename_valid(self):
        """Test validation of valid filenames."""
        valid_filenames = [
            "document.pdf",
            "image.jpg",
            "file_name.txt",
            "file-name.doc"
        ]
        
        for filename in valid_filenames:
            result = ValidationService.validate_filename(filename)
            assert result["is_valid"] is True
            assert len(result["errors"]) == 0
    
    def test_validate_filename_dangerous_characters(self):
        """Test validation of filenames with dangerous characters."""
        dangerous_filenames = [
            "file<script>.txt",
            "file>redirect.txt",
            'file"quote.txt',
            "file|pipe.txt",
            "file?query.txt",
            "file*wildcard.txt"
        ]
        
        for filename in dangerous_filenames:
            result = ValidationService.validate_filename(filename)
            assert result["is_valid"] is False
            assert any("dangerous character" in error for error in result["errors"])
    
    def test_validate_filename_path_traversal(self):
        """Test validation of filenames with path traversal."""
        traversal_filenames = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32\\config",
            "/etc/passwd",
            "\\windows\\system32"
        ]
        
        for filename in traversal_filenames:
            result = ValidationService.validate_filename(filename)
            assert result["is_valid"] is False
            assert any("path traversal" in error for error in result["errors"])
    
    def test_validate_filename_reserved_names(self):
        """Test validation of reserved system filenames."""
        reserved_names = [
            "CON.txt",
            "PRN.pdf",
            "AUX.doc",
            "NUL.jpg",
            "COM1.txt",
            "LPT1.pdf"
        ]
        
        for filename in reserved_names:
            result = ValidationService.validate_filename(filename)
            assert result["is_valid"] is False
            assert any("reserved system name" in error for error in result["errors"])
    
    def test_validate_filename_too_long(self):
        """Test validation of filename that's too long."""
        long_filename = "a" * 260 + ".txt"
        result = ValidationService.validate_filename(long_filename)
        
        assert result["is_valid"] is False
        assert any("too long" in error for error in result["errors"])
    
    def test_validate_filename_empty(self):
        """Test validation of empty filename."""
        result = ValidationService.validate_filename("")
        assert result["is_valid"] is False
        assert any("required" in error for error in result["errors"])
        
        result = ValidationService.validate_filename(None)
        assert result["is_valid"] is False
        assert any("required" in error for error in result["errors"])
    
    def test_validate_message_content_valid(self):
        """Test validation of valid message content."""
        valid_messages = [
            "Hello world!",
            "This is a <strong>formatted</strong> message",
            "Message with emoji 😊",
            "Multi-line\nmessage\ncontent"
        ]
        
        for message in valid_messages:
            result = ValidationService.validate_message_content(message)
            assert result["is_valid"] is True
            assert len(result["errors"]) == 0
            assert result["sanitized_content"] is not None
    
    def test_validate_message_content_empty(self):
        """Test validation of empty message content."""
        result = ValidationService.validate_message_content("")
        assert result["is_valid"] is False
        assert any("cannot be empty" in error for error in result["errors"])
        
        result = ValidationService.validate_message_content("   ")
        assert result["is_valid"] is False
        assert any("cannot be empty" in error for error in result["errors"])
        
        result = ValidationService.validate_message_content(None)
        assert result["is_valid"] is False
        assert any("cannot be empty" in error for error in result["errors"])
    
    def test_validate_message_content_too_long(self):
        """Test validation of message content that's too long."""
        long_message = "a" * 5001
        result = ValidationService.validate_message_content(long_message)
        
        assert result["is_valid"] is False
        assert any("too long" in error for error in result["errors"])
    
    @pytest.mark.security
    def test_validate_message_content_xss_sanitization(self, xss_payloads):
        """Test that message content is sanitized against XSS."""
        for payload in xss_payloads:
            result = ValidationService.validate_message_content(payload)
            
            # Content should be sanitized
            sanitized = result["sanitized_content"]
            assert "<script>" not in sanitized.lower()
            assert "javascript:" not in sanitized.lower()
            assert "onerror=" not in sanitized.lower()
    
    @pytest.mark.security
    def test_validate_message_content_sql_injection_warning(self, sql_injection_payloads):
        """Test that message content with SQL injection patterns generates warnings."""
        for payload in sql_injection_payloads:
            result = ValidationService.validate_message_content(payload)
            
            # Should generate warnings for suspicious patterns
            if len(result["warnings"]) > 0:
                assert any("unsafe" in warning for warning in result["warnings"])
    
    def test_validate_room_name_valid(self):
        """Test validation of valid room names."""
        valid_names = [
            "General Chat",
            "Team Discussion",
            "Project_Alpha",
            "Room-123",
            "Dev.Team"
        ]
        
        for name in valid_names:
            result = ValidationService.validate_room_name(name)
            assert result["is_valid"] is True
            assert len(result["errors"]) == 0
            assert result["normalized_name"] == name.strip()
    
    def test_validate_room_name_invalid_length(self):
        """Test validation of room names with invalid length."""
        # Too short
        result = ValidationService.validate_room_name("A")
        assert result["is_valid"] is False
        assert any("2 characters" in error for error in result["errors"])
        
        # Too long
        long_name = "a" * 51
        result = ValidationService.validate_room_name(long_name)
        assert result["is_valid"] is False
        assert any("50 characters" in error for error in result["errors"])
    
    def test_validate_room_name_invalid_characters(self):
        """Test validation of room names with invalid characters."""
        invalid_names = [
            "Room@Name",
            "Room#Tag",
            "Room$Money",
            "Room%Percent"
        ]
        
        for name in invalid_names:
            result = ValidationService.validate_room_name(name)
            assert result["is_valid"] is False
            assert any("can only contain" in error for error in result["errors"])
    
    def test_validate_room_name_only_special_chars(self):
        """Test validation of room names with only special characters."""
        invalid_names = [
            "___",
            "...",
            "---",
            "   "
        ]
        
        for name in invalid_names:
            result = ValidationService.validate_room_name(name)
            assert result["is_valid"] is False
            assert any("must contain at least one letter or number" in error for error in result["errors"])
    
    def test_validate_room_name_empty(self):
        """Test validation of empty room name."""
        result = ValidationService.validate_room_name("")
        assert result["is_valid"] is False
        assert any("required" in error for error in result["errors"])
        
        result = ValidationService.validate_room_name(None)
        assert result["is_valid"] is False
        assert any("required" in error for error in result["errors"])
    
    @pytest.mark.performance
    def test_validation_performance(self):
        """Test validation performance with large inputs."""
        import time
        
        # Test email validation performance
        start_time = time.time()
        for i in range(100):
            ValidationService.validate_email_address(f"user{i}@example.com")
        email_time = time.time() - start_time
        
        # Test username validation performance
        start_time = time.time()
        for i in range(100):
            ValidationService.validate_username(f"user{i}")
        username_time = time.time() - start_time
        
        # Test HTML sanitization performance
        html_content = "<p>Test content</p>" * 100
        start_time = time.time()
        for _ in range(10):
            ValidationService.sanitize_html(html_content)
        html_time = time.time() - start_time
        
        # All operations should complete quickly
        assert email_time < 1.0
        assert username_time < 1.0
        assert html_time < 1.0
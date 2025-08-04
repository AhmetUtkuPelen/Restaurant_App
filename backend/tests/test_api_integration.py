"""
Integration tests for API endpoints

Tests complete API workflows including authentication, user management,
messaging, and security features. Tests real HTTP requests and responses.
"""

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch

from .conftest import assert_error_response, assert_success_response


class TestUserAPIIntegration:
    """Integration tests for User API endpoints."""
    
    def test_user_registration_success(self, client):
        """Test successful user registration."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "display_name": "Test User"
        }
        
        response = client.post("/users/register", json=user_data)
        
        assert_success_response(response, 201)
        data = response.json()
        
        assert "user" in data
        assert "token" in data
        assert data["user"]["username"] == user_data["username"]
        assert data["user"]["email"] == user_data["email"]
        assert data["user"]["display_name"] == user_data["display_name"]
        assert "password" not in data["user"]  # Password should not be returned
    
    def test_user_registration_duplicate_username(self, client, created_user):
        """Test registration with duplicate username."""
        user_data = {
            "username": created_user.username,
            "email": "different@example.com",
            "password": "TestPassword123!",
            "display_name": "Different User"
        }
        
        response = client.post("/users/register", json=user_data)
        assert_error_response(response, 400, "already exists")
    
    def test_user_registration_duplicate_email(self, client, created_user):
        """Test registration with duplicate email."""
        user_data = {
            "username": "differentuser",
            "email": created_user.email,
            "password": "TestPassword123!",
            "display_name": "Different User"
        }
        
        response = client.post("/users/register", json=user_data)
        assert_error_response(response, 400, "already exists")
    
    def test_user_registration_invalid_email(self, client):
        """Test registration with invalid email."""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "TestPassword123!",
            "display_name": "Test User"
        }
        
        response = client.post("/users/register", json=user_data)
        assert_error_response(response, 422)
    
    def test_user_registration_weak_password(self, client):
        """Test registration with weak password."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "weak",
            "display_name": "Test User"
        }
        
        response = client.post("/users/register", json=user_data)
        assert_error_response(response, 400)
    
    def test_user_login_success(self, client, created_user, test_user_data):
        """Test successful user login."""
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        response = client.post("/users/login", json=login_data)
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert "user" in data
        assert "token" in data
        assert data["user"]["id"] == created_user.id
        assert data["user"]["username"] == created_user.username
    
    def test_user_login_with_email(self, client, created_user, test_user_data):
        """Test login with email instead of username."""
        login_data = {
            "username": test_user_data["email"],  # Using email as username
            "password": test_user_data["password"]
        }
        
        response = client.post("/users/login", json=login_data)
        assert_success_response(response, 200)
    
    def test_user_login_invalid_credentials(self, client, created_user):
        """Test login with invalid credentials."""
        login_data = {
            "username": created_user.username,
            "password": "wrongpassword"
        }
        
        response = client.post("/users/login", json=login_data)
        assert_error_response(response, 401, "Invalid")
    
    def test_user_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        
        response = client.post("/users/login", json=login_data)
        assert_error_response(response, 401, "Invalid")
    
    def test_get_current_user_success(self, client, auth_headers, created_user):
        """Test getting current user profile."""
        response = client.get("/users/me", headers=auth_headers)
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert data["id"] == created_user.id
        assert data["username"] == created_user.username
        assert data["email"] == created_user.email
    
    def test_get_current_user_no_auth(self, client):
        """Test getting current user without authentication."""
        response = client.get("/users/me")
        assert_error_response(response, 401)
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        assert_error_response(response, 401)
    
    def test_update_current_user_success(self, client, auth_headers):
        """Test updating current user profile."""
        update_data = {
            "display_name": "Updated Name",
            "bio": "Updated bio"
        }
        
        response = client.put("/users/me", json=update_data, headers=auth_headers)
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert data["display_name"] == update_data["display_name"]
        assert data["bio"] == update_data["bio"]
    
    def test_get_all_users(self, client, created_user):
        """Test getting all users (public info only)."""
        response = client.get("/users/")
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Check that only public info is returned
        user_data = data[0]
        assert "id" in user_data
        assert "username" in user_data
        assert "display_name" in user_data
        assert "email" not in user_data  # Email should not be in public info
    
    def test_search_users(self, client, created_user):
        """Test user search functionality."""
        response = client.get(f"/users/search/?q={created_user.username[:3]}")
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 1
        
        # Should find the created user
        usernames = [user["username"] for user in data]
        assert created_user.username in usernames


class TestMessageAPIIntegration:
    """Integration tests for Message API endpoints."""
    
    def test_send_message_success(self, client, auth_headers, created_room):
        """Test sending a message to a chat room."""
        message_data = {
            "content": "Hello, world!",
            "chat_id": created_room.id,
            "message_type": "TEXT"
        }
        
        response = client.post("/messages/", json=message_data, headers=auth_headers)
        
        assert_success_response(response, 201)
        data = response.json()
        
        assert data["content"] == message_data["content"]
        assert data["chat_id"] == message_data["chat_id"]
        assert data["message_type"] == message_data["message_type"]
        assert data["status"] == "sent"
    
    def test_send_private_message_success(self, client, auth_headers, created_admin):
        """Test sending a private message to another user."""
        message_data = {
            "content": "Private message",
            "recipient_id": created_admin.id,
            "message_type": "TEXT"
        }
        
        response = client.post("/messages/", json=message_data, headers=auth_headers)
        
        assert_success_response(response, 201)
        data = response.json()
        
        assert data["content"] == message_data["content"]
        assert data["recipient_id"] == message_data["recipient_id"]
        assert data["chat_id"] is None
    
    def test_send_message_no_auth(self, client):
        """Test sending message without authentication."""
        message_data = {
            "content": "Hello, world!",
            "message_type": "TEXT"
        }
        
        response = client.post("/messages/", json=message_data)
        assert_error_response(response, 401)
    
    def test_send_empty_message(self, client, auth_headers, created_room):
        """Test sending empty message."""
        message_data = {
            "content": "",
            "chat_id": created_room.id,
            "message_type": "TEXT"
        }
        
        response = client.post("/messages/", json=message_data, headers=auth_headers)
        assert_error_response(response, 400, "empty")
    
    def test_get_chat_messages(self, client, auth_headers, created_room):
        """Test getting messages from a chat room."""
        # First send a message
        message_data = {
            "content": "Test message",
            "chat_id": created_room.id,
            "message_type": "TEXT"
        }
        client.post("/messages/", json=message_data, headers=auth_headers)
        
        # Then get messages
        response = client.get(f"/messages/?chat_id={created_room.id}", headers=auth_headers)
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["content"] == message_data["content"]
    
    def test_get_conversation_messages(self, client, auth_headers, created_admin):
        """Test getting conversation messages between two users."""
        # First send a private message
        message_data = {
            "content": "Private conversation",
            "recipient_id": created_admin.id,
            "message_type": "TEXT"
        }
        client.post("/messages/", json=message_data, headers=auth_headers)
        
        # Then get conversation
        response = client.get(f"/messages/?recipient_id={created_admin.id}", headers=auth_headers)
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["content"] == message_data["content"]
    
    def test_get_messages_pagination(self, client, auth_headers, created_room):
        """Test message pagination."""
        # Send multiple messages
        for i in range(5):
            message_data = {
                "content": f"Message {i}",
                "chat_id": created_room.id,
                "message_type": "TEXT"
            }
            client.post("/messages/", json=message_data, headers=auth_headers)
        
        # Test pagination
        response = client.get(f"/messages/?chat_id={created_room.id}&limit=2", headers=auth_headers)
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert len(data) == 2
        
        # Test skip parameter
        response = client.get(f"/messages/?chat_id={created_room.id}&limit=2&skip=2", headers=auth_headers)
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert len(data) <= 2


class TestSecurityIntegration:
    """Integration tests for security features."""
    
    @pytest.mark.security
    def test_rate_limiting(self, client, rate_limit_setup):
        """Test API rate limiting."""
        # Make requests up to the limit
        for i in range(5):
            response = client.get("/")
            assert response.status_code == 200
        
        # Next request should be rate limited
        response = client.get("/")
        assert response.status_code == 429
    
    @pytest.mark.security
    def test_sql_injection_protection(self, client, sql_injection_payloads):
        """Test SQL injection protection in search endpoints."""
        for payload in sql_injection_payloads:
            response = client.get(f"/users/search/?q={payload}")
            
            # Should not cause server error, should handle gracefully
            assert response.status_code in [200, 400, 422]
            
            if response.status_code == 200:
                # Should return empty or safe results
                data = response.json()
                assert isinstance(data, list)
    
    @pytest.mark.security
    def test_xss_protection_in_messages(self, client, auth_headers, created_room, xss_payloads):
        """Test XSS protection in message content."""
        for payload in xss_payloads:
            message_data = {
                "content": payload,
                "chat_id": created_room.id,
                "message_type": "TEXT"
            }
            
            response = client.post("/messages/", json=message_data, headers=auth_headers)
            
            if response.status_code == 201:
                data = response.json()
                # Content should be sanitized
                assert "<script>" not in data["content"].lower()
                assert "javascript:" not in data["content"].lower()
    
    @pytest.mark.security
    def test_authentication_required_endpoints(self, client):
        """Test that protected endpoints require authentication."""
        protected_endpoints = [
            ("GET", "/users/me"),
            ("PUT", "/users/me"),
            ("POST", "/messages/"),
            ("GET", "/messages/"),
        ]
        
        for method, endpoint in protected_endpoints:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            elif method == "PUT":
                response = client.put(endpoint, json={})
            
            assert response.status_code == 401
    
    @pytest.mark.security
    def test_jwt_token_validation(self, client):
        """Test JWT token validation."""
        # Test with malformed token
        headers = {"Authorization": "Bearer malformed.token"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 401
        
        # Test with expired token (mock)
        with patch('Services.AuthService.AuthService.verify_token') as mock_verify:
            from fastapi import HTTPException
            mock_verify.side_effect = HTTPException(status_code=401, detail="Token has expired")
            
            headers = {"Authorization": "Bearer expired_token"}
            response = client.get("/users/me", headers=headers)
            assert response.status_code == 401
    
    @pytest.mark.security
    def test_password_security_requirements(self, client):
        """Test password security requirements during registration."""
        weak_passwords = [
            "123456",
            "password",
            "abc123",
            "qwerty",
            "short"
        ]
        
        for weak_password in weak_passwords:
            user_data = {
                "username": f"user_{weak_password}",
                "email": f"user_{weak_password}@example.com",
                "password": weak_password,
                "display_name": "Test User"
            }
            
            response = client.post("/users/register", json=user_data)
            assert response.status_code == 400


class TestAPIErrorHandling:
    """Integration tests for API error handling."""
    
    def test_404_not_found(self, client):
        """Test 404 error handling."""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client):
        """Test 405 error handling."""
        response = client.patch("/users/register")  # POST-only endpoint
        assert response.status_code == 405
    
    def test_422_validation_error(self, client):
        """Test validation error handling."""
        # Send invalid JSON data
        response = client.post("/users/register", json={"invalid": "data"})
        assert response.status_code == 422
        
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], list)
    
    def test_500_internal_server_error_handling(self, client):
        """Test internal server error handling."""
        # Mock a database error
        with patch('database.get_db') as mock_get_db:
            mock_get_db.side_effect = Exception("Database connection failed")
            
            response = client.get("/test-db")
            # Should handle gracefully, not crash
            assert response.status_code in [200, 500]


class TestAPIPerformance:
    """Performance tests for API endpoints."""
    
    @pytest.mark.performance
    def test_user_registration_performance(self, client):
        """Test user registration performance."""
        import time
        
        start_time = time.time()
        
        # Register 10 users
        for i in range(10):
            user_data = {
                "username": f"perfuser{i}",
                "email": f"perfuser{i}@example.com",
                "password": "TestPassword123!",
                "display_name": f"Performance User {i}"
            }
            
            response = client.post("/users/register", json=user_data)
            assert response.status_code == 201
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time
        assert duration < 10.0  # 10 seconds for 10 registrations
    
    @pytest.mark.performance
    def test_message_sending_performance(self, client, auth_headers, created_room):
        """Test message sending performance."""
        import time
        
        start_time = time.time()
        
        # Send 20 messages
        for i in range(20):
            message_data = {
                "content": f"Performance test message {i}",
                "chat_id": created_room.id,
                "message_type": "TEXT"
            }
            
            response = client.post("/messages/", json=message_data, headers=auth_headers)
            assert response.status_code == 201
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time
        assert duration < 5.0  # 5 seconds for 20 messages
    
    @pytest.mark.performance
    def test_message_retrieval_performance(self, client, auth_headers, created_room):
        """Test message retrieval performance."""
        import time
        
        # First, send some messages
        for i in range(50):
            message_data = {
                "content": f"Message {i}",
                "chat_id": created_room.id,
                "message_type": "TEXT"
            }
            client.post("/messages/", json=message_data, headers=auth_headers)
        
        start_time = time.time()
        
        # Retrieve messages multiple times
        for _ in range(10):
            response = client.get(f"/messages/?chat_id={created_room.id}&limit=20", headers=auth_headers)
            assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time
        assert duration < 2.0  # 2 seconds for 10 retrievals


class TestWebSocketIntegration:
    """Integration tests for WebSocket functionality."""
    
    def test_websocket_connection(self, websocket_client):
        """Test WebSocket connection establishment."""
        with websocket_client.websocket_connect("/ws/test_user") as websocket:
            # Connection should be established
            assert websocket is not None
    
    def test_websocket_message_sending(self, websocket_client):
        """Test sending messages via WebSocket."""
        with websocket_client.websocket_connect("/ws/test_user") as websocket:
            # Send a message
            message_data = {
                "message": "Hello WebSocket!",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            
            websocket.send_json(message_data)
            
            # Should receive confirmation
            response = websocket.receive_json()
            assert response["content"] == message_data["message"]
            assert response["status"] == "delivered"
    
    def test_websocket_invalid_user(self, websocket_client):
        """Test WebSocket connection with invalid user."""
        # This test depends on authentication implementation
        # For now, just test that connection can be established
        with websocket_client.websocket_connect("/ws/invalid_user") as websocket:
            assert websocket is not None


class TestHealthEndpoints:
    """Integration tests for health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root health check endpoint."""
        response = client.get("/")
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert "message" in data
        assert "running" in data["message"].lower()
    
    def test_database_health_check(self, client):
        """Test database health check endpoint."""
        response = client.get("/test-db")
        
        # Should return either success or error, but not crash
        assert response.status_code in [200, 500]
        
        data = response.json()
        assert "message" in data or "error" in data
    
    def test_openapi_documentation(self, client):
        """Test OpenAPI documentation endpoint."""
        response = client.get("/openapi.json")
        
        assert_success_response(response, 200)
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
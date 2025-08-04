"""
OpenAPI Documentation Service

This module provides comprehensive OpenAPI/Swagger documentation configuration
for the Chat API, including security schemes, response examples, and detailed
endpoint documentation.
"""

from typing import Dict, Any, List
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer
from fastapi import FastAPI

class OpenAPIService:
    """Service for managing OpenAPI documentation configuration."""
    
    @staticmethod
    def get_custom_openapi(app: FastAPI) -> Dict[str, Any]:
        """
        Generate custom OpenAPI schema with enhanced documentation.
        
        Args:
            app: FastAPI application instance
            
        Returns:
            Custom OpenAPI schema dictionary
        """
        if app.openapi_schema:
            return app.openapi_schema
            
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        
        # Add security schemes
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT token obtained from login endpoint"
            }
        }
        
        # Add global security requirement
        openapi_schema["security"] = [{"BearerAuth": []}]
        
        # Add custom response schemas
        openapi_schema["components"]["schemas"].update({
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {"type": "boolean", "example": True},
                    "message": {"type": "string", "example": "An error occurred"},
                    "code": {"type": "string", "example": "VALIDATION_ERROR"},
                    "details": {"type": "object", "nullable": True},
                    "timestamp": {"type": "string", "format": "date-time"},
                    "request_id": {"type": "string", "nullable": True}
                },
                "required": ["error", "message", "code", "timestamp"]
            },
            "ValidationError": {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "loc": {"type": "array", "items": {"type": "string"}},
                                "msg": {"type": "string"},
                                "type": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "RateLimitError": {
                "type": "object",
                "properties": {
                    "error": {"type": "boolean", "example": True},
                    "message": {"type": "string", "example": "Rate limit exceeded"},
                    "retry_after": {"type": "integer", "example": 3600}
                }
            }
        })
        
        # Add common response examples
        common_responses = {
            "401": {
                "description": "Authentication required",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "error": True,
                            "message": "Invalid authentication credentials",
                            "code": "AUTHENTICATION_ERROR",
                            "timestamp": "2024-01-01T12:00:00Z"
                        }
                    }
                }
            },
            "403": {
                "description": "Access forbidden",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "error": True,
                            "message": "Insufficient permissions",
                            "code": "AUTHORIZATION_ERROR",
                            "timestamp": "2024-01-01T12:00:00Z"
                        }
                    }
                }
            },
            "422": {
                "description": "Validation error",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ValidationError"}
                    }
                }
            },
            "429": {
                "description": "Rate limit exceeded",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/RateLimitError"}
                    }
                }
            },
            "500": {
                "description": "Internal server error",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                        "example": {
                            "error": True,
                            "message": "Internal server error",
                            "code": "INTERNAL_ERROR",
                            "timestamp": "2024-01-01T12:00:00Z"
                        }
                    }
                }
            }
        }
        
        # Add common responses to all paths
        for path_data in openapi_schema["paths"].values():
            for method_data in path_data.values():
                if isinstance(method_data, dict) and "responses" in method_data:
                    # Add common error responses if not already present
                    for status_code, response in common_responses.items():
                        if status_code not in method_data["responses"]:
                            method_data["responses"][status_code] = response
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    @staticmethod
    def get_authentication_examples() -> Dict[str, Any]:
        """Get authentication examples for documentation."""
        return {
            "login_request": {
                "summary": "Login with username",
                "value": {
                    "username_or_email": "johndoe",
                    "password": "securepassword123"
                }
            },
            "login_email_request": {
                "summary": "Login with email",
                "value": {
                    "username_or_email": "john@example.com",
                    "password": "securepassword123"
                }
            },
            "register_request": {
                "summary": "Register new user",
                "value": {
                    "username": "johndoe",
                    "email": "john@example.com",
                    "password": "securepassword123",
                    "display_name": "John Doe"
                }
            }
        }
    
    @staticmethod
    def get_message_examples() -> Dict[str, Any]:
        """Get message examples for documentation."""
        return {
            "text_message": {
                "summary": "Send text message to chat room",
                "value": {
                    "chat_id": "room_123",
                    "content": "Hello everyone!",
                    "message_type": "text"
                }
            },
            "private_message": {
                "summary": "Send private message to user",
                "value": {
                    "recipient_id": "user_456",
                    "content": "Hi there!",
                    "message_type": "text"
                }
            },
            "reply_message": {
                "summary": "Reply to a message",
                "value": {
                    "chat_id": "room_123",
                    "content": "Thanks for the info!",
                    "message_type": "text",
                    "reply_to_message_id": "msg_789"
                }
            },
            "file_message": {
                "summary": "Send message with file attachment",
                "value": {
                    "chat_id": "room_123",
                    "content": "Check out this document",
                    "message_type": "file",
                    "metadata": {
                        "file_name": "document.pdf",
                        "file_size": 1024000,
                        "file_type": "application/pdf"
                    }
                }
            }
        }
    
    @staticmethod
    def get_websocket_examples() -> Dict[str, Any]:
        """Get WebSocket message examples for documentation."""
        return {
            "client_message": {
                "summary": "Client sends message",
                "value": {
                    "message": "Hello, world!",
                    "timestamp": "2024-01-01T12:00:00Z",
                    "attachments": []
                }
            },
            "server_response": {
                "summary": "Server broadcasts message",
                "value": {
                    "id": "msg_1234567890",
                    "sender_id": "user123",
                    "content": "Hello, world!",
                    "created_at": "2024-01-01T12:00:00Z",
                    "status": "delivered",
                    "attachments": [],
                    "is_edited": False
                }
            },
            "user_status": {
                "summary": "User status update",
                "value": {
                    "type": "user_status",
                    "user_id": "user123",
                    "status": "online",
                    "timestamp": "2024-01-01T12:00:00Z"
                }
            }
        }
    
    @staticmethod
    def get_error_examples() -> Dict[str, Any]:
        """Get error response examples for documentation."""
        return {
            "validation_error": {
                "summary": "Validation error example",
                "value": {
                    "detail": [
                        {
                            "loc": ["body", "email"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        },
                        {
                            "loc": ["body", "password"],
                            "msg": "ensure this value has at least 8 characters",
                            "type": "value_error.any_str.min_length"
                        }
                    ]
                }
            },
            "authentication_error": {
                "summary": "Authentication error",
                "value": {
                    "error": True,
                    "message": "Invalid authentication credentials",
                    "code": "AUTHENTICATION_ERROR",
                    "timestamp": "2024-01-01T12:00:00Z"
                }
            },
            "rate_limit_error": {
                "summary": "Rate limit exceeded",
                "value": {
                    "error": True,
                    "message": "Rate limit exceeded. Try again in 3600 seconds.",
                    "code": "RATE_LIMIT_EXCEEDED",
                    "retry_after": 3600,
                    "timestamp": "2024-01-01T12:00:00Z"
                }
            }
        }
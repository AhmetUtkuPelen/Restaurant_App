from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from Services.RateLimitService import RateLimitService
import time
from typing import Callable, Optional

class RateLimitMiddleware:
    """Rate limiting middleware for FastAPI"""
    
    def __init__(
        self, 
        app, 
        default_requests: int = 100, 
        default_window: int = 3600,
        skip_paths: Optional[list] = None
    ):
        self.app = app
        self.default_requests = default_requests
        self.default_window = default_window
        self.skip_paths = skip_paths or ["/docs", "/redoc", "/openapi.json", "/health"]
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        # Skip rate limiting for certain paths
        if any(request.url.path.startswith(path) for path in self.skip_paths):
            await self.app(scope, receive, send)
            return
        
        # Extract endpoint identifier
        endpoint = f"{request.method}:{request.url.path}"
        
        # Get user ID from token if available
        user_id = None
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                from Services.AuthService import AuthService
                token = auth_header.split(" ")[1]
                payload = AuthService.decode_token_without_verification(token)
                if payload:
                    user_id = payload.get("sub")
            except Exception:
                pass  # Continue without user ID
        
        try:
            # Check rate limit
            rate_limit_info = RateLimitService.check_rate_limit(
                request, endpoint, user_id, self.default_requests, self.default_window
            )
            
            # Add rate limit headers to response
            async def send_with_headers(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    headers[b"x-ratelimit-limit"] = str(rate_limit_info["limit"]).encode()
                    headers[b"x-ratelimit-remaining"] = str(rate_limit_info["remaining"]).encode()
                    headers[b"x-ratelimit-reset"] = str(rate_limit_info["reset_time"]).encode()
                    message["headers"] = list(headers.items())
                await send(message)
            
            await self.app(scope, receive, send_with_headers)
            
        except HTTPException as e:
            # Rate limit exceeded, return error response
            response = JSONResponse(
                status_code=e.status_code,
                content={
                    "error": True,
                    "message": e.detail,
                    "code": "RATE_LIMIT_EXCEEDED",
                    "timestamp": time.time()
                },
                headers=e.headers
            )
            await response(scope, receive, send)

def create_rate_limit_decorator(
    max_requests: int = 100, 
    window_seconds: int = 3600,
    endpoint_name: Optional[str] = None
):
    """
    Create a rate limit decorator for specific endpoints
    
    Args:
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds
        endpoint_name: Custom endpoint name for rate limiting
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            # Extract request from function arguments
            request = None
            user_id = None
            
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            # Look for user_id in kwargs (common in authenticated endpoints)
            if "current_user_id" in kwargs:
                user_id = kwargs["current_user_id"]
            elif "user_id" in kwargs:
                user_id = kwargs["user_id"]
            
            if request:
                endpoint = endpoint_name or f"{request.method}:{request.url.path}"
                
                # Check rate limit
                RateLimitService.check_rate_limit(
                    request, endpoint, user_id, max_requests, window_seconds
                )
            
            # Call the original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# Common rate limit decorators
def rate_limit_auth(func: Callable):
    """Rate limit for authentication endpoints (stricter limits)"""
    return create_rate_limit_decorator(max_requests=10, window_seconds=300)(func)

def rate_limit_api(func: Callable):
    """Rate limit for general API endpoints"""
    return create_rate_limit_decorator(max_requests=100, window_seconds=3600)(func)

def rate_limit_upload(func: Callable):
    """Rate limit for file upload endpoints"""
    return create_rate_limit_decorator(max_requests=20, window_seconds=3600)(func)
import time
import redis
from typing import Dict, Optional
from fastapi import HTTPException, status, Request
from config import settings
import hashlib

class RateLimitService:
    """Rate limiting service with Redis backend and fallback to in-memory storage"""
    
    # In-memory fallback storage
    _memory_store: Dict[str, Dict] = {}
    _redis_client = None
    
    @classmethod
    def _get_redis_client(cls):
        """Get Redis client with fallback to in-memory storage"""
        if cls._redis_client is None:
            try:
                cls._redis_client = redis.from_url(settings.redis_url)
                # Test connection
                cls._redis_client.ping()
            except Exception:
                # Use in-memory storage as fallback
                cls._redis_client = "memory"
        return cls._redis_client
    
    @classmethod
    def _get_client_identifier(cls, request: Request, user_id: Optional[str] = None) -> str:
        """
        Generate unique client identifier for rate limiting
        
        Args:
            request: FastAPI request object
            user_id: Optional user ID for authenticated requests
            
        Returns:
            Unique client identifier
        """
        if user_id:
            return f"user:{user_id}"
        
        # Use IP address for anonymous requests
        client_ip = request.client.host if request.client else "unknown"
        
        # Include user agent for better uniqueness
        user_agent = request.headers.get("user-agent", "")
        identifier = f"ip:{client_ip}:{hashlib.md5(user_agent.encode()).hexdigest()[:8]}"
        
        return identifier
    
    @classmethod
    def check_rate_limit(
        cls, 
        request: Request, 
        endpoint: str, 
        user_id: Optional[str] = None,
        max_requests: Optional[int] = None,
        window_seconds: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Check if request is within rate limits
        
        Args:
            request: FastAPI request object
            endpoint: API endpoint identifier
            user_id: Optional user ID for authenticated requests
            max_requests: Maximum requests allowed (defaults to settings)
            window_seconds: Time window in seconds (defaults to settings)
            
        Returns:
            Dictionary with rate limit status and metadata
            
        Raises:
            HTTPException: If rate limit is exceeded
        """
        max_requests = max_requests or settings.rate_limit_requests
        window_seconds = window_seconds or settings.rate_limit_window
        
        client_id = cls._get_client_identifier(request, user_id)
        key = f"rate_limit:{endpoint}:{client_id}"
        
        current_time = int(time.time())
        window_start = current_time - window_seconds
        
        redis_client = cls._get_redis_client()
        
        if redis_client == "memory":
            # Use in-memory storage
            return cls._check_rate_limit_memory(
                key, current_time, window_start, max_requests, window_seconds
            )
        else:
            # Use Redis storage
            return cls._check_rate_limit_redis(
                redis_client, key, current_time, window_start, max_requests, window_seconds
            )
    
    @classmethod
    def _check_rate_limit_memory(
        cls, 
        key: str, 
        current_time: int, 
        window_start: int, 
        max_requests: int,
        window_seconds: int
    ) -> Dict[str, any]:
        """Check rate limit using in-memory storage"""
        if key not in cls._memory_store:
            cls._memory_store[key] = {"requests": [], "blocked_until": 0}
        
        data = cls._memory_store[key]
        
        # Check if currently blocked
        if data["blocked_until"] > current_time:
            remaining_block_time = data["blocked_until"] - current_time
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {remaining_block_time} seconds.",
                headers={
                    "Retry-After": str(remaining_block_time),
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(data["blocked_until"])
                }
            )
        
        # Clean old requests
        data["requests"] = [req_time for req_time in data["requests"] if req_time > window_start]
        
        # Check if limit exceeded
        if len(data["requests"]) >= max_requests:
            # Block for the remaining window time
            data["blocked_until"] = current_time + window_seconds
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.",
                headers={
                    "Retry-After": str(window_seconds),
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(data["blocked_until"])
                }
            )
        
        # Add current request
        data["requests"].append(current_time)
        
        remaining_requests = max_requests - len(data["requests"])
        reset_time = current_time + window_seconds
        
        return {
            "allowed": True,
            "limit": max_requests,
            "remaining": remaining_requests,
            "reset_time": reset_time,
            "retry_after": None
        }
    
    @classmethod
    def _check_rate_limit_redis(
        cls, 
        redis_client, 
        key: str, 
        current_time: int, 
        window_start: int, 
        max_requests: int,
        window_seconds: int
    ) -> Dict[str, any]:
        """Check rate limit using Redis storage"""
        try:
            # Use Redis pipeline for atomic operations
            pipe = redis_client.pipeline()
            
            # Remove old entries
            pipe.zremrangebyscore(key, 0, window_start)
            
            # Count current requests
            pipe.zcard(key)
            
            # Execute pipeline
            results = pipe.execute()
            current_requests = results[1]
            
            # Check if limit exceeded
            if current_requests >= max_requests:
                # Get the oldest request time to calculate retry-after
                oldest_request = redis_client.zrange(key, 0, 0, withscores=True)
                if oldest_request:
                    retry_after = int(oldest_request[0][1]) + window_seconds - current_time
                    retry_after = max(1, retry_after)  # At least 1 second
                else:
                    retry_after = window_seconds
                
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.",
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(max_requests),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(current_time + retry_after)
                    }
                )
            
            # Add current request
            redis_client.zadd(key, {str(current_time): current_time})
            redis_client.expire(key, window_seconds)
            
            remaining_requests = max_requests - current_requests - 1
            reset_time = current_time + window_seconds
            
            return {
                "allowed": True,
                "limit": max_requests,
                "remaining": remaining_requests,
                "reset_time": reset_time,
                "retry_after": None
            }
            
        except Exception as e:
            # Fallback to allowing request if Redis fails
            print(f"Redis rate limiting failed: {e}")
            return {
                "allowed": True,
                "limit": max_requests,
                "remaining": max_requests - 1,
                "reset_time": current_time + window_seconds,
                "retry_after": None
            }
    
    @classmethod
    def get_rate_limit_status(
        cls, 
        request: Request, 
        endpoint: str, 
        user_id: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Get current rate limit status without incrementing counter
        
        Args:
            request: FastAPI request object
            endpoint: API endpoint identifier
            user_id: Optional user ID for authenticated requests
            
        Returns:
            Dictionary with current rate limit status
        """
        client_id = cls._get_client_identifier(request, user_id)
        key = f"rate_limit:{endpoint}:{client_id}"
        
        current_time = int(time.time())
        window_start = current_time - settings.rate_limit_window
        
        redis_client = cls._get_redis_client()
        
        if redis_client == "memory":
            if key not in cls._memory_store:
                return {
                    "limit": settings.rate_limit_requests,
                    "remaining": settings.rate_limit_requests,
                    "reset_time": current_time + settings.rate_limit_window
                }
            
            data = cls._memory_store[key]
            # Clean old requests
            data["requests"] = [req_time for req_time in data["requests"] if req_time > window_start]
            
            remaining = settings.rate_limit_requests - len(data["requests"])
            return {
                "limit": settings.rate_limit_requests,
                "remaining": max(0, remaining),
                "reset_time": current_time + settings.rate_limit_window
            }
        else:
            try:
                # Clean old entries and count current requests
                redis_client.zremrangebyscore(key, 0, window_start)
                current_requests = redis_client.zcard(key)
                
                remaining = settings.rate_limit_requests - current_requests
                return {
                    "limit": settings.rate_limit_requests,
                    "remaining": max(0, remaining),
                    "reset_time": current_time + settings.rate_limit_window
                }
            except Exception:
                return {
                    "limit": settings.rate_limit_requests,
                    "remaining": settings.rate_limit_requests,
                    "reset_time": current_time + settings.rate_limit_window
                }
    
    @classmethod
    def reset_rate_limit(cls, request: Request, endpoint: str, user_id: Optional[str] = None) -> bool:
        """
        Reset rate limit for a specific client and endpoint
        
        Args:
            request: FastAPI request object
            endpoint: API endpoint identifier
            user_id: Optional user ID for authenticated requests
            
        Returns:
            True if reset was successful
        """
        client_id = cls._get_client_identifier(request, user_id)
        key = f"rate_limit:{endpoint}:{client_id}"
        
        redis_client = cls._get_redis_client()
        
        if redis_client == "memory":
            if key in cls._memory_store:
                del cls._memory_store[key]
            return True
        else:
            try:
                redis_client.delete(key)
                return True
            except Exception:
                return False
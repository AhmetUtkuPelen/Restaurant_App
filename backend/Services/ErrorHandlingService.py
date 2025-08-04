import logging
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ErrorResponse(BaseModel):
    """Standardized error response format"""
    error: bool = True
    message: str
    code: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    request_id: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class GlobalErrorHandler:
    """Global error handling service for consistent error responses"""
    
    @staticmethod
    def generate_request_id() -> str:
        """Generate unique request ID for tracking"""
        return str(uuid.uuid4())
    
    @staticmethod
    def log_error(
        error: Exception, 
        request: Optional[Request] = None, 
        request_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log error with context information
        
        Args:
            error: Exception that occurred
            request: FastAPI request object
            request_id: Unique request identifier
            user_id: User ID if available
        """
        error_data = {
            "request_id": request_id,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if request:
            error_data.update({
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
                "headers": dict(request.headers)
            })
        
        # Log stack trace for server errors
        if isinstance(error, (SQLAlchemyError, Exception)) and not isinstance(error, HTTPException):
            error_data["traceback"] = traceback.format_exc()
            logger.error(f"Server Error: {json.dumps(error_data, indent=2)}")
        else:
            logger.warning(f"Client Error: {json.dumps(error_data, indent=2)}")
    
    @staticmethod
    def handle_validation_error(
        error: ValidationError, 
        request: Optional[Request] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle Pydantic validation errors
        
        Args:
            error: ValidationError instance
            request: FastAPI request object
            request_id: Unique request identifier
            
        Returns:
            JSONResponse with validation error details
        """
        request_id = request_id or GlobalErrorHandler.generate_request_id()
        
        # Extract validation error details
        validation_errors = []
        for err in error.errors():
            validation_errors.append({
                "field": ".".join(str(x) for x in err["loc"]),
                "message": err["msg"],
                "type": err["type"],
                "input": err.get("input")
            })
        
        GlobalErrorHandler.log_error(error, request, request_id)
        
        error_response = ErrorResponse(
            message="Validation failed",
            code="VALIDATION_ERROR",
            details={"validation_errors": validation_errors},
            timestamp=datetime.utcnow(),
            request_id=request_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.dict()
        )
    
    @staticmethod
    def handle_authentication_error(
        error: HTTPException, 
        request: Optional[Request] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle authentication and authorization errors
        
        Args:
            error: HTTPException instance
            request: FastAPI request object
            request_id: Unique request identifier
            
        Returns:
            JSONResponse with authentication error details
        """
        request_id = request_id or GlobalErrorHandler.generate_request_id()
        
        GlobalErrorHandler.log_error(error, request, request_id)
        
        # Determine error code based on status
        if error.status_code == status.HTTP_401_UNAUTHORIZED:
            code = "AUTHENTICATION_FAILED"
        elif error.status_code == status.HTTP_403_FORBIDDEN:
            code = "AUTHORIZATION_FAILED"
        else:
            code = "AUTH_ERROR"
        
        error_response = ErrorResponse(
            message=error.detail,
            code=code,
            timestamp=datetime.utcnow(),
            request_id=request_id
        )
        
        headers = getattr(error, 'headers', None)
        
        return JSONResponse(
            status_code=error.status_code,
            content=error_response.dict(),
            headers=headers
        )
    
    @staticmethod
    def handle_database_error(
        error: SQLAlchemyError, 
        request: Optional[Request] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle database-related errors
        
        Args:
            error: SQLAlchemyError instance
            request: FastAPI request object
            request_id: Unique request identifier
            
        Returns:
            JSONResponse with database error details
        """
        request_id = request_id or GlobalErrorHandler.generate_request_id()
        
        GlobalErrorHandler.log_error(error, request, request_id)
        
        # Don't expose internal database errors to clients
        error_response = ErrorResponse(
            message="A database error occurred. Please try again later.",
            code="DATABASE_ERROR",
            timestamp=datetime.utcnow(),
            request_id=request_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.dict()
        )
    
    @staticmethod
    def handle_http_exception(
        error: HTTPException, 
        request: Optional[Request] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle HTTP exceptions
        
        Args:
            error: HTTPException instance
            request: FastAPI request object
            request_id: Unique request identifier
            
        Returns:
            JSONResponse with HTTP error details
        """
        request_id = request_id or GlobalErrorHandler.generate_request_id()
        
        # Handle authentication/authorization errors separately
        if error.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]:
            return GlobalErrorHandler.handle_authentication_error(error, request, request_id)
        
        GlobalErrorHandler.log_error(error, request, request_id)
        
        # Map status codes to error codes
        status_code_map = {
            400: "BAD_REQUEST",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            409: "CONFLICT",
            429: "RATE_LIMIT_EXCEEDED",
            500: "INTERNAL_SERVER_ERROR",
            502: "BAD_GATEWAY",
            503: "SERVICE_UNAVAILABLE"
        }
        
        code = status_code_map.get(error.status_code, "HTTP_ERROR")
        
        error_response = ErrorResponse(
            message=error.detail,
            code=code,
            timestamp=datetime.utcnow(),
            request_id=request_id
        )
        
        headers = getattr(error, 'headers', None)
        
        return JSONResponse(
            status_code=error.status_code,
            content=error_response.dict(),
            headers=headers
        )
    
    @staticmethod
    def handle_generic_error(
        error: Exception, 
        request: Optional[Request] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle unexpected errors
        
        Args:
            error: Exception instance
            request: FastAPI request object
            request_id: Unique request identifier
            
        Returns:
            JSONResponse with generic error details
        """
        request_id = request_id or GlobalErrorHandler.generate_request_id()
        
        GlobalErrorHandler.log_error(error, request, request_id)
        
        # Don't expose internal error details to clients
        error_response = ErrorResponse(
            message="An unexpected error occurred. Please try again later.",
            code="INTERNAL_SERVER_ERROR",
            timestamp=datetime.utcnow(),
            request_id=request_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.dict()
        )
    
    @staticmethod
    def handle_rate_limit_error(
        error: HTTPException, 
        request: Optional[Request] = None,
        request_id: Optional[str] = None
    ) -> JSONResponse:
        """
        Handle rate limiting errors
        
        Args:
            error: HTTPException instance for rate limiting
            request: FastAPI request object
            request_id: Unique request identifier
            
        Returns:
            JSONResponse with rate limit error details
        """
        request_id = request_id or GlobalErrorHandler.generate_request_id()
        
        GlobalErrorHandler.log_error(error, request, request_id)
        
        error_response = ErrorResponse(
            message=error.detail,
            code="RATE_LIMIT_EXCEEDED",
            details={
                "retry_after": error.headers.get("Retry-After") if hasattr(error, 'headers') else None
            },
            timestamp=datetime.utcnow(),
            request_id=request_id
        )
        
        headers = getattr(error, 'headers', None)
        
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content=error_response.dict(),
            headers=headers
        )

class ErrorHandlerMiddleware:
    """Middleware for global error handling"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        request_id = GlobalErrorHandler.generate_request_id()
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        try:
            await self.app(scope, receive, send)
        except Exception as error:
            # Handle different types of errors
            if isinstance(error, ValidationError):
                response = GlobalErrorHandler.handle_validation_error(error, request, request_id)
            elif isinstance(error, SQLAlchemyError):
                response = GlobalErrorHandler.handle_database_error(error, request, request_id)
            elif isinstance(error, HTTPException):
                if error.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                    response = GlobalErrorHandler.handle_rate_limit_error(error, request, request_id)
                else:
                    response = GlobalErrorHandler.handle_http_exception(error, request, request_id)
            else:
                response = GlobalErrorHandler.handle_generic_error(error, request, request_id)
            
            await response(scope, receive, send)
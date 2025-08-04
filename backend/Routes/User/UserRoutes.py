from fastapi import APIRouter, status, Query, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from sqlalchemy.orm import Session
from Controllers.User.UserController import UserController
from Schemas.User.UserSchemas import (
    UserCreate, UserUpdate, UserResponse, UserLogin, UserPublic, LoginResponse
)
from Models.User.UserModel import UserStatus
from database import get_db
from Services.AuthService import AuthService

# Create router
router = APIRouter(prefix="/users", tags=["users"])

# Initialize controller
user_controller = UserController()

# Security scheme
security = HTTPBearer()

# Dependency to get current user from JWT token
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> str:
    """Get current user ID from JWT token"""
    try:
        token = credentials.credentials
        user_id = AuthService.get_user_id_from_token(token)

        # Verify user exists in database
        user = await user_controller.get_user_by_id(db, user_id)
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post(
    "/register",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Create a new user account with email verification.",
    responses={
        201: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "user_123",
                            "username": "johndoe",
                            "email": "john@example.com",
                            "display_name": "John Doe",
                            "status": "offline",
                            "role": "user",
                            "is_active": True,
                            "created_at": "2024-01-01T12:00:00Z"
                        },
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "message": "User registered successfully"
                    }
                }
            }
        },
        400: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Username already exists"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    **Required Fields:**
    - username: 3-50 characters, unique
    - email: Valid email address, unique
    - password: Minimum 8 characters
    - display_name: Optional, 1-100 characters
    
    **Password Requirements:**
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    
    **Returns:**
    - User profile information
    - JWT authentication token
    - Success message
    
    **Security Features:**
    - Password hashing with bcrypt
    - Email validation
    - Username uniqueness check
    - Input sanitization
    """
    return await user_controller.create_user(db, user_data)

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User Login",
    description="Authenticate user and return JWT token.",
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "user_123",
                            "username": "johndoe",
                            "email": "john@example.com",
                            "display_name": "John Doe",
                            "status": "online",
                            "role": "user",
                            "is_active": True,
                            "last_seen": "2024-01-01T12:00:00Z"
                        },
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "message": "Login successful"
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid username or password"
                    }
                }
            }
        },
        429: {
            "description": "Too many failed attempts",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Account temporarily locked due to too many failed login attempts"
                    }
                }
            }
        }
    }
)
async def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    **Authentication Methods:**
    - Username and password
    - Email and password
    
    **Security Features:**
    - Rate limiting on failed attempts
    - Account lockout after 5 failed attempts
    - Secure password verification with bcrypt
    - JWT token with expiration
    
    **Token Usage:**
    Use the returned token in the Authorization header:
    ```
    Authorization: Bearer <token>
    ```
    
    **Account Lockout:**
    After 5 failed login attempts, the account is temporarily locked.
    Contact support or wait for the lockout period to expire.
    """
    return await user_controller.login_user(db, login_data)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User Profile",
    description="Retrieve the authenticated user's profile information.",
    responses={
        200: {
            "description": "User profile retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "user_123",
                        "username": "johndoe",
                        "email": "john@example.com",
                        "display_name": "John Doe",
                        "avatar_url": "https://example.com/avatar.jpg",
                        "bio": "Software developer and chat enthusiast",
                        "status": "online",
                        "role": "user",
                        "is_active": True,
                        "is_verified": True,
                        "created_at": "2024-01-01T12:00:00Z",
                        "last_seen": "2024-01-01T15:30:00Z"
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid authentication credentials"
                    }
                }
            }
        }
    }
)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get the authenticated user's profile information.
    
    **Authentication Required:** Bearer token in Authorization header.
    
    **Returns:**
    - Complete user profile including private information
    - Account status and verification status
    - Role and permissions
    - Activity timestamps
    
    **Use Cases:**
    - Profile page display
    - Account settings
    - User dashboard
    - Authentication verification
    """
    return await user_controller.get_user_by_id(db, current_user_id)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    return await user_controller.get_user_by_id(db, user_id)

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    return await user_controller.update_user(db, current_user_id, update_data)

@router.get("/", response_model=List[UserPublic])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all users (public info only)"""
    return await user_controller.get_all_users(db, skip, limit)

@router.get("/search/", response_model=List[UserPublic])
async def search_users(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search users by username or display name"""
    return await user_controller.search_users(db, q, limit)

@router.patch("/me/status", response_model=UserResponse)
async def update_user_status(
    status_data: UserStatus,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update user online status"""
    return await user_controller.update_user_status(db, current_user_id, status_data)

@router.delete("/me")
async def delete_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete current user account"""
    return await user_controller.delete_user(db, current_user_id)
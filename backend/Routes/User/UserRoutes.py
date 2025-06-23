from fastapi import APIRouter, status, Query, Depends
from typing import List
from sqlalchemy.orm import Session
from backend.Controllers.User.UserController import UserController
from backend.Schemas.User.UserSchemas import (
    UserCreate, UserUpdate, UserResponse, UserLogin, UserPublic
)
from backend.Models.User.UserModel import UserStatus
from backend.database import get_db

# Create router
router = APIRouter(prefix="/users", tags=["users"])

# Initialize controller
user_controller = UserController()

# Dependency to get current user (simplified - in real app use JWT)
async def get_current_user_id() -> str:
    # This is a placeholder - implement proper authentication
    return "current_user_id"

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return await user_controller.create_user(db, user_data)

@router.post("/login", response_model=UserResponse)
async def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    return await user_controller.login_user(db, login_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
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
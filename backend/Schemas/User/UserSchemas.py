from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from Models.User.UserModel import UserStatus, UserRole

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    display_name: Optional[str] = Field(None, max_length=100)

class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    status: Optional[UserStatus] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    display_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    status: UserStatus
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_seen: Optional[datetime]

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class UserPublic(BaseModel):
    """Public user info for chat display"""
    id: str
    username: str
    display_name: Optional[str]
    avatar_url: Optional[str]
    status: UserStatus
    last_seen: Optional[datetime]

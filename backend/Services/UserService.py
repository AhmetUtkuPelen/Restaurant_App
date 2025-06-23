from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from typing import List, Optional
import hashlib
from Models.database_models import UserDB
from Models.User.UserModel import UserStatus
from Schemas.User.UserSchemas import UserCreate, UserUpdate, UserResponse, UserLogin, UserPublic
from datetime import datetime

class UserService:
    def __init__(self):
        pass
    
    def _hash_password(self, password: str) -> str:
        """Simple password hashing - use proper hashing in production"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == hashed
    
    def _user_to_response(self, user: UserDB) -> UserResponse:
        """Convert UserDB to UserResponse"""
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            bio=user.bio,
            status=user.status,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_seen=user.last_seen
        )
    
    def _user_to_public(self, user: UserDB) -> UserPublic:
        """Convert UserDB to UserPublic"""
        return UserPublic(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            status=user.status,
            last_seen=user.last_seen
        )
    
    async def create_user(self, db: Session, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if username or email already exists
        existing_user = db.query(UserDB).filter(
            or_(UserDB.username == user_data.username.lower(),
                UserDB.email == str(user_data.email).lower())
        ).first()
        
        if existing_user:
            if existing_user.username == user_data.username.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
        
        # Create new user
        hashed_password = self._hash_password(user_data.password)
        
        db_user = UserDB(
            username=user_data.username.lower(),
            email=str(user_data.email).lower(),
            password_hash=hashed_password,
            display_name=user_data.display_name or user_data.username
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return self._user_to_response(db_user)
    
    async def login_user(self, db: Session, login_data: UserLogin) -> UserResponse:
        """Authenticate user login"""
        # Find user by username or email
        user = db.query(UserDB).filter(
            or_(UserDB.username == login_data.username_or_email.lower(),
                UserDB.email == login_data.username_or_email.lower())
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not self._verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Update last seen and status
        user.last_seen = datetime.utcnow()
        user.status = UserStatus.ONLINE
        db.commit()
        
        return self._user_to_response(user)
    
    async def get_user_by_id(self, db: Session, user_id: str) -> UserResponse:
        """Get user by ID"""
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return self._user_to_response(user)
    
    async def update_user(self, db: Session, user_id: str, update_data: UserUpdate) -> UserResponse:
        """Update user information"""
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields
        if update_data.display_name is not None:
            user.display_name = update_data.display_name
        if update_data.bio is not None:
            user.bio = update_data.bio
        if update_data.avatar_url is not None:
            user.avatar_url = update_data.avatar_url
        if update_data.status is not None:
            user.status = update_data.status
        
        user.updated_at = datetime.utcnow()
        db.commit()
        
        return self._user_to_response(user)
    
    async def get_all_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserPublic]:
        """Get all users (public info only)"""
        users = db.query(UserDB).offset(skip).limit(limit).all()
        return [self._user_to_public(user) for user in users]
    
    async def search_users(self, db: Session, query: str, limit: int = 20) -> List[UserPublic]:
        """Search users by username or display name"""
        query = f"%{query.lower()}%"
        users = db.query(UserDB).filter(
            or_(UserDB.username.ilike(query),
                UserDB.display_name.ilike(query))
        ).limit(limit).all()
        
        return [self._user_to_public(user) for user in users]
    
    async def update_user_status(self, db: Session, user_id: str, new_status: UserStatus) -> UserResponse:
        """Update user online status"""
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.status = new_status
        user.last_seen = datetime.utcnow()
        db.commit()
        
        return self._user_to_response(user)
    
    async def delete_user(self, db: Session, user_id: str) -> dict:
        """Delete a user"""
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        
        return {"message": "User deleted successfully"}

from sqlalchemy.orm import Session
from typing import List
from Services.UserService import UserService
from Models.User.UserModel import UserStatus
from Schemas.User.UserSchemas import UserCreate, UserUpdate, UserResponse, UserLogin, UserPublic, LoginResponse

class UserController:
    def __init__(self):
        self.user_service = UserService()

    async def create_user(self, db: Session, user_data: UserCreate) -> LoginResponse:
        """Create a new user"""
        return await self.user_service.create_user(db, user_data)

    async def login_user(self, db: Session, login_data: UserLogin) -> LoginResponse:
        """Authenticate user login"""
        return await self.user_service.login_user(db, login_data)

    async def get_user_by_id(self, db: Session, user_id: str) -> UserResponse:
        """Get user by ID"""
        return await self.user_service.get_user_by_id(db, user_id)

    async def update_user(self, db: Session, user_id: str, update_data: UserUpdate) -> UserResponse:
        """Update user information"""
        return await self.user_service.update_user(db, user_id, update_data)

    async def get_all_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserPublic]:
        """Get all users (public info only)"""
        return await self.user_service.get_all_users(db, skip, limit)

    async def search_users(self, db: Session, query: str, limit: int = 20) -> List[UserPublic]:
        """Search users by username or display name"""
        return await self.user_service.search_users(db, query, limit)

    async def update_user_status(self, db: Session, user_id: str, new_status: UserStatus) -> UserResponse:
        """Update user online status"""
        return await self.user_service.update_user_status(db, user_id, new_status)

    async def delete_user(self, db: Session, user_id: str) -> dict:
        """Delete a user"""
        return await self.user_service.delete_user(db, user_id)
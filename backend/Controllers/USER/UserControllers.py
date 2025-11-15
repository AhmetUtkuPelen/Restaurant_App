from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta

from Models.USER.UserModel import User
from Schemas.USER.UserSchemas import UserRegister,UserLogin,AdminCreateUser,AdminUpdateUser,UserProfileUpdate
from Utils.Auth.JWT import create_access_token,create_refresh_token,decode_access_token,decode_refresh_token,TokenExpiredError,TokenInvalidError
from Utils.Auth.HashPassword import get_password_hash,verify_password
from Utils.Enums.Enums import UserRole

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class UserControllers:
    #################
    # AUTHENTICATION && USER CONTROLLERS
    #################

    @staticmethod
    async def register_user(user_data: UserRegister, db: AsyncSession) -> Dict[str, Any]:
        """
        Register a new user.
        """
        try:
            # Check if username already exists
            stmt = select(User).where(User.username == user_data.username)
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
            
            # Check if email already exists
            stmt = select(User).where(User.email == user_data.email)
            result = await db.execute(stmt)
            existing_email = result.scalar_one_or_none()
            
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            # Hash password
            hashed_password = get_password_hash(user_data.password)
            
            # Create new user
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password,
                image_url=user_data.image_url,
                phone=user_data.phone,
                address=user_data.address,
                role=UserRole.USER,
                is_active=True
            )
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            return {
                "message": "User registered successfully",
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "email": new_user.email
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )

    @staticmethod
    async def login_user(credentials: UserLogin, db: AsyncSession) -> Dict[str, Any]:
        """
        Authenticate user and return tokens.
        """
        try:
            # Find user by username
            stmt = select(User).where(User.username == credentials.username)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password"
                )

            # Verify password
            if not verify_password(credentials.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password"
                )
            
            # Check if user is active
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is deactivated"
                )
            
            # Create tokens
            token_data = {
                "sub": user.username,
                "role": user.role.value
            }
            
            access_token = create_access_token(data=token_data)
            refresh_token = create_refresh_token(data=token_data)
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role.value
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {str(e)}"
            )

    @staticmethod
    async def logout_user() -> Dict[str, str]:
        """
        Logout user (client-side token deletion).
        For token blacklisting, implement Redis/DB storage.
        """
        return {"message": "Logged out successfully. Please delete your tokens."}

    @staticmethod
    async def refresh_token(refresh_token: str, db: AsyncSession) -> Dict[str, Any]:
        """
        Generate new access token using refresh token.
        """
        try:
            # Decode refresh token
            payload = await decode_refresh_token(refresh_token)
            username = payload.get("sub")
            
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )

            # Verify user still exists and is active
            stmt = select(User).where(User.username == username)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive"
                )
            
            # Create new access token
            token_data = {
                "sub": user.username,
                "role": user.role.value
            }
            
            new_access_token = create_access_token(data=token_data)
            
            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }
            
        except TokenExpiredError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired. Please login again."
            )
        except TokenInvalidError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token refresh failed: {str(e)}"
            )

    @staticmethod
    async def get_current_user(token: str, db: AsyncSession) -> User:
        """
        Dependency to get current authenticated user from token.
        Use this i
n route dependencies: Depends(UserControllers.get_current_user)
        """
        try:
            # Decode token
            payload = await decode_access_token(token)
            username = payload.get("sub")
            
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
            
            # Get user from database
            stmt = select(User).where(User.username == username)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Inactive user"
                )
            
            return user
            
        except TokenExpiredError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except TokenInvalidError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {str(e)}"
            )

    @staticmethod
    async def get_user_profile(current_user: User) -> Dict[str, Any]:
        """
        Get authenticated user's profile.
        """
        return current_user.user_profile

    @staticmethod
    async def update_user_profile(
        current_user: User,
        update_data: UserProfileUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Update authenticated user's profile.
        """
        try:
            # Check if username is being changed and if it's already taken
            if update_data.username and update_data.username != current_user.username:
                stmt = select(User).where(User.username == update_data.username)
                result = await db.execute(stmt)
                existing = result.scalar_one_or_none()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already taken"
                    )

            # Check if email is being changed and if it's already taken
            if update_data.email and update_data.email != current_user.email:
                stmt = select(User).where(User.email == update_data.email)
                result = await db.execute(stmt)
                existing = result.scalar_one_or_none()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already taken"
                    )
            
            # Use the model's update_profile method
            update_dict = update_data.model_dump(exclude_unset=True)
            updated = current_user.update_profile(update_dict)
            
            if updated:
                await db.commit()
                await db.refresh(current_user)
                return {
                    "message": "Profile updated successfully",
                    "user": current_user.user_profile
                }
            else:
                return {
                    "message": "No changes made",
                    "user": current_user.user_profile
                }
                
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Profile update failed: {str(e)}"
            )

    @staticmethod
    async def change_password(
        current_user: User,
        current_password: str,
        new_password: str,
        db: AsyncSession
    ) -> Dict[str, str]:
        """
        Change authenticated user's password.
        Note: Password validation is handled by Pydantic schemas in the route layer.
        """
        try:
            # Verify current password
            if not verify_password(current_password, current_user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )
            
            # Hash and update password
            current_user.hashed_password = get_password_hash(new_password)
            await db.commit()
            
            return {"message": "Password changed successfully"}
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Password change failed: {str(e)}"
            )

    #################
    # ADMIN CONTROLLERS
    #################

    @staticmethod
    async def get_single_user_by_id(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Get single user by ID with all relationships.
        """
        try:
            stmt = select(User).options(
                selectinload(User.orders),
                selectinload(User.comments),
                selectinload(User.cart),
                selectinload(User.reservations),
                selectinload(User.payments)
            ).where(User.id == user_id)
            
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return user.to_dict()
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user: {str(e)}"
            )


    @staticmethod
    async def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """
        Admin: Get all users with pagination.
        """
        try:
            # Get total count
            count_stmt = select(func.count(User.id))
            total_result = await db.execute(count_stmt)
            total = total_result.scalar()
            
            # Get users with pagination
            stmt = select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
            result = await db.execute(stmt)
            users = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "users": [user.to_dict() for user in users]
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch users: {str(e)}"
            )

    @staticmethod
    async def get_users_by_role(role: UserRole, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Admin: Get all users with specific role.
        """
        try:
            stmt = select(User).where(User.role == role).order_by(User.created_at.desc())
            result = await db.execute(stmt)
            users = result.scalars().all()
            
            return [user.to_dict() for user in users]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch users by role: {str(e)}"
            )

    @staticmethod
    async def change_user_role(
        user_id: int,
        new_role: UserRole,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Admin: Change user's role.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            old_role = user.role
            user.role = new_role
            await db.commit()
            await db.refresh(user)
            
            return {
                "message": f"User role changed from {old_role.value} to {new_role.value}",
                "user": user.to_dict()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to change user role: {str(e)}"
            )

    @staticmethod
    async def activate_user_by_id(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Activate user account.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user.is_active = True
            user.deleted_at = None
            await db.commit()
            await db.refresh(user)
            
            return {
                "message": "User activated successfully",
                "user": user.to_dict()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to activate user: {str(e)}"
            )


    @staticmethod
    async def deactivate_user_by_id(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Deactivate user account (soft delete).
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user.is_active = False
            user.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(user)
            
            return {
                "message": "User deactivated successfully",
                "user": user.to_dict()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate user: {str(e)}"
            )

    @staticmethod
    async def get_users_by_status(is_active: bool, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Admin: Get users by active/inactive status.
        """
        try:
            stmt = select(User).where(User.is_active == is_active).order_by(User.created_at.desc())
            result = await db.execute(stmt)
            users = result.scalars().all()
            
            return [user.to_dict() for user in users]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch users by status: {str(e)}"
            )

    @staticmethod
    async def get_user_statistics(db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Get user statistics for dashboard.
        """
        try:
            # Total users
            total_stmt = select(func.count(User.id))
            total_result = await db.execute(total_stmt)
            total_users = total_result.scalar()
            
            # Active users
            active_stmt = select(func.count(User.id)).where(User.is_active == True)
            active_result = await db.execute(active_stmt)
            active_users = active_result.scalar()
            
            # Inactive users
            inactive_users = total_users - active_users
            
            # Users by role
            admin_stmt = select(func.count(User.id)).where(User.role == UserRole.ADMIN)
            admin_result = await db.execute(admin_stmt)
            admin_count = admin_result.scalar()
            
            staff_stmt = select(func.count(User.id)).where(User.role == UserRole.STAFF)
            staff_result = await db.execute(staff_stmt)
            staff_count = staff_result.scalar()
            
            user_stmt = select(func.count(User.id)).where(User.role == UserRole.USER)
            user_result = await db.execute(user_stmt)
            user_count = user_result.scalar()
            
            # New registrations (last 30 days)
            thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
            new_stmt = select(func.count(User.id)).where(User.created_at >= thirty_days_ago)
            new_result = await db.execute(new_stmt)
            new_registrations = new_result.scalar()
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": inactive_users,
                "users_by_role": {
                    "admin": admin_count,
                    "staff": staff_count,
                    "user": user_count
                },
                "new_registrations_last_30_days": new_registrations
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch statistics: {str(e)}"
            )


    @staticmethod
    async def update_user_by_id(
        user_id: int,
        update_data: AdminUpdateUser,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Admin: Update any user's information.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Check username uniqueness if being changed
            if update_data.username and update_data.username != user.username:
                check_stmt = select(User).where(User.username == update_data.username)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already taken"
                    )
            
            # Check email uniqueness if being changed
            if update_data.email and update_data.email != user.email:
                check_stmt = select(User).where(User.email == update_data.email)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already taken"
                    )
            
            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                if key == "password":
                    user.hashed_password = get_password_hash(value)
                else:
                    setattr(user, key, value)
            
            await db.commit()
            await db.refresh(user)
            
            return {
                "message": "User updated successfully",
                "user": user.to_dict()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update user: {str(e)}"
            )

    @staticmethod
    async def create_new_user(
        user_data: AdminCreateUser,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Admin: Create a new user with any role.
        """
        try:
            # Check username uniqueness
            stmt = select(User).where(User.username == user_data.username)
            result = await db.execute(stmt)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )
            
            # Check email uniqueness
            stmt = select(User).where(User.email == user_data.email)
            result = await db.execute(stmt)
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            
            # Create user
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=get_password_hash(user_data.password),
                role=user_data.role,
                image_url=user_data.image_url,
                phone=user_data.phone,
                address=user_data.address,
                is_active=user_data.is_active
            )
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            return {
                "message": "User created successfully",
                "user": new_user.to_dict()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {str(e)}"
            )


    @staticmethod
    async def hard_delete_user_by_id(user_id: int, db: AsyncSession) -> Dict[str, str]:
        """
        Admin: Permanently delete user and all related data.
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            await db.delete(user)
            await db.commit()
            
            return {"message": f"User {user.username} permanently deleted"}
            
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete user: {str(e)}"
            )

    @staticmethod
    async def soft_delete_user_by_id(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Soft delete user (same as deactivate).
        """
        return await UserControllers.deactivate_user_by_id(user_id, db)

    @staticmethod
    async def search_user_by_values(
        search: str,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Admin: Search users by username, email, or phone.
        """
        try:
            stmt = select(User).where(
                or_(
                    User.username.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                    User.phone.ilike(f"%{search}%") if search else False
                )
            ).order_by(User.created_at.desc())
            
            result = await db.execute(stmt)
            users = result.scalars().all()
            
            return [user.to_dict() for user in users]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Search failed: {str(e)}"
            )

    @staticmethod
    async def get_user_activity_log(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Get user activity summary.
        """
        try:
            stmt = select(User).options(
                selectinload(User.orders),
                selectinload(User.comments),
                selectinload(User.reservations),
                selectinload(User.payments)
            ).where(User.id == user_id)
            
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return {
                "user_id": user.id,
                "username": user.username,
                "total_orders": len(user.orders),
                "total_comments": len(user.comments),
                "total_reservations": len(user.reservations),
                "total_payments": len(user.payments),
                "account_created": user.created_at.isoformat() if user.created_at else None,
                "last_updated": user.updated_at.isoformat() if user.updated_at else None
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch activity log: {str(e)}"
            )

    @staticmethod
    async def get_user_orders(user_id: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Admin: Get all orders for a specific user.
        """
        try:
            stmt = select(User).options(selectinload(User.orders)).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return [order.to_dict() for order in user.orders]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user orders: {str(e)}"
            )

    @staticmethod
    async def get_user_comments(user_id: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Admin: Get all comments for a specific user.
        """
        try:
            stmt = select(User).options(selectinload(User.comments)).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return [comment.to_dict() for comment in user.comments]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user comments: {str(e)}"
            )

    @staticmethod
    async def get_user_favourite_products(user_id: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Admin: Get all favourite products for a specific user.
        """
        try:
            stmt = select(User).options(selectinload(User.favourite_products)).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return [fav.to_dict() for fav in user.favourite_products]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch favourite products: {str(e)}"
            )

    @staticmethod
    async def get_user_cart(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Get cart for a specific user.
        """
        try:
            stmt = select(User).options(selectinload(User.cart)).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            if not user.cart:
                return {"message": "User has no cart"}
            
            return user.cart.to_dict()
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user cart: {str(e)}"
            )

    @staticmethod
    async def get_user_reservations(user_id: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Admin: Get all reservations for a specific user.
        """
        try:
            stmt = select(User).options(selectinload(User.reservations)).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return [reservation.to_dict() for reservation in user.reservations]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user reservations: {str(e)}"
            )

    @staticmethod
    async def get_user_payments(user_id: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Admin: Get all payments for a specific user.
        """
        try:
            stmt = select(User).options(selectinload(User.payments)).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return [payment.to_dict() for payment in user.payments]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user payments: {str(e)}"
            )

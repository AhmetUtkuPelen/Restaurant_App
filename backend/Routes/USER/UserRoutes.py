from fastapi import APIRouter, HTTPException, status, Depends, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from Controllers.USER.UserControllers import UserControllers, oauth2_scheme
from Schemas.USER.UserSchemas import (
    UserRegister, 
    UserLogin, 
    UserProfileUpdate,
    AdminCreateUser,
    AdminUpdateUser,
    Token,
    UserProfileRead
)
from Models.USER.UserModel import User
from Database.Database import get_db
from Utils.Enums.Enums import UserRole
from Utils.SlowApi.SlowApi import limiter

UserRouter = APIRouter(prefix="/users", tags=["Users"])


#########################
# DEPENDENCY FUNCTIONS #
########################

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """ For getting currently authenticated user """
    return await UserControllers.get_current_user(token, db)


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """ To make sure user is active """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """ require admin role """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_staff_or_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """ require staff or admin role """
    if current_user.role not in [UserRole.ADMIN, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff or Admin access required"
        )
    return current_user


#########################
# AUTHENTICATION ROUTES #
########################

@UserRouter.post("/register", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
@limiter.limit("5/minute")
async def register(
    request: Request,
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    
    - **username**: Unique username (3-20 characters)
    - **email**: Valid email address
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit, special char)
    - 5 requests per minute for security
    """
    return await UserControllers.register_user(user_data, db)


@UserRouter.post("/login", response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def login(
    request: Request,
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with username and password.
    Returns access token and refresh token.
    10 requests per minute for security.
    """
    return await UserControllers.login_user(credentials, db)


@UserRouter.post("/logout", response_model=Dict[str, str])
async def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout current user.
    Front End handles the Log Out functionality . Make Sure to Delete Tokens
    """
    return await UserControllers.logout_user()


@UserRouter.post("/refresh", response_model=Dict[str, Any])
@limiter.limit("20/minute")
async def refresh_access_token(
    request: Request,
    refresh_token: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Get new access token using refresh token.
    
    - **refresh_token**: Valid refresh token from login
    20 requests per minute for security.
    """
    return await UserControllers.refresh_token(refresh_token, db)


#######################
# USER PROFILE ROUTES #
#######################

@UserRouter.get("/me", response_model=UserProfileRead)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's profile information.
    """
    return await UserControllers.get_user_profile(current_user, db)


@UserRouter.put("/me", response_model=Dict[str, Any])
async def update_my_profile(
    update_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile.
    
    All fields are optional. Only provided fields will be updated.
    """
    return await UserControllers.update_user_profile(current_user, update_data, db)


@UserRouter.post("/me/change-password", response_model=Dict[str, str])
async def change_my_password(
    current_password: str = Body(...),
    new_password: str = Body(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change current user's password.
    
    - **current_password**: Current password for verification
    - **new_password**: New password (must meet strength requirements as well)
    """
    return await UserControllers.change_password(current_user, current_password, new_password, db)


#################################
# ADMIN USER MANAGEMENT ROUTES #
#################################

@UserRouter.get("/admin/all", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all users with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return await UserControllers.get_all_users(skip, limit, db)


@UserRouter.get("/admin/{user_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Get single user by ID with all relationships.
    """
    return await UserControllers.get_single_user_by_id(user_id, db)


@UserRouter.post("/admin/create", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def create_user(
    user_data: AdminCreateUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Create a new user with a role.
    """
    return await UserControllers.create_new_user(user_data, db)


@UserRouter.put("/admin/{user_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def update_user(
    user_id: int,
    update_data: AdminUpdateUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update any user's informations.
    """
    return await UserControllers.update_user_by_id(user_id, update_data, db)


@UserRouter.delete("/admin/{user_id}/hard", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def hard_delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Permanently delete user and all related data.
    """
    return await UserControllers.hard_delete_user_by_id(user_id, db)


@UserRouter.post("/admin/{user_id}/deactivate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Deactivate user account , is_active (soft delete).
    """
    return await UserControllers.deactivate_user_by_id(user_id, db)


@UserRouter.post("/admin/{user_id}/activate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Activate user account.
    """
    return await UserControllers.activate_user_by_id(user_id, db)


@UserRouter.post("/admin/{user_id}/role", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def change_user_role(
    user_id: int,
    new_role: UserRole = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Change user's role.
    
    - **new_role**: New role (USER, STAFF, or ADMIN)
    """
    return await UserControllers.change_user_role(user_id, new_role, db)


#######################
# ADMIN QUERY ROUTES #
#######################

@UserRouter.get("/admin/role/{role}", response_model=List[Dict[str, Any]], dependencies=[Depends(require_admin)])
async def get_users_by_role(
    role: UserRole,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Get all users with specific role.
    """
    return await UserControllers.get_users_by_role(role, db)


@UserRouter.get("/admin/status/{is_active}", response_model=List[Dict[str, Any]], dependencies=[Depends(require_admin)])
async def get_users_by_status(
    is_active: bool,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Get users by active/inactive status.
    """
    return await UserControllers.get_users_by_status(is_active, db)


@UserRouter.get("/admin/search/{search}", response_model=List[Dict[str, Any]], dependencies=[Depends(require_admin)])
async def search_users(
    search: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Search users by username, email, or phone.
    """
    return await UserControllers.search_user_by_values(search, db)


@UserRouter.get("/admin/statistics", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def get_user_statistics(db: AsyncSession = Depends(get_db)):
    """
    Admin: Get user statistics for dashboard.
    
    Total users, active/inactive counts, role distribution, and new registrations.
    """
    return await UserControllers.get_user_statistics(db)


###############################
# ADMIN USER ACTIVITY ROUTES #
##############################

@UserRouter.get("/admin/{user_id}/activity", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_user_activity(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get user activity summary.
    """
    return await UserControllers.get_user_activity_log(user_id, db)


@UserRouter.get("/admin/{user_id}/orders", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_user_orders(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all orders for a specific user.
    """
    return await UserControllers.get_user_orders(user_id, db)


@UserRouter.get("/admin/{user_id}/comments", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_user_comments(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all comments for a specific user.
    """
    return await UserControllers.get_user_comments(user_id, db)


@UserRouter.get("/admin/{user_id}/favourites", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_user_favourites(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all favourite products for a specific user.
    """
    return await UserControllers.get_user_favourite_products(user_id, db)


@UserRouter.get("/admin/{user_id}/cart", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_user_cart(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get cart for a specific user.
    """
    return await UserControllers.get_user_cart(user_id, db)


@UserRouter.get("/admin/{user_id}/reservations", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_user_reservations(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all reservations for a specific user.
    """
    return await UserControllers.get_user_reservations(user_id, db)


@UserRouter.get("/admin/{user_id}/payments", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_user_payments(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all payments for a specific user.
    """
    return await UserControllers.get_user_payments(user_id, db)
from fastapi import APIRouter, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from Controllers.COMMENT.CommentControllers import CommentControllers
from Schemas.COMMENT.CommentSchemas import CommentCreate, CommentUpdate
from Models.USER.UserModel import User
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import get_current_active_user, require_admin, require_staff_or_admin

CommentRouter = APIRouter(prefix="/comments", tags=["Comments"])


# ============================================
# PUBLIC ROUTES
# ============================================

@CommentRouter.get("/product/{product_id}", response_model=Dict[str, Any])
async def get_product_comments(
    product_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all active comments for a specific product.
    
    - **product_id**: ID of the product
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    
    Returns comments with average rating and total count.
    Public endpoint - no authentication required.
    """
    return await CommentControllers.get_comments_by_product_id(product_id, skip, limit, db)


@CommentRouter.get("/{comment_id}", response_model=Dict[str, Any])
async def get_comment_by_id(
    comment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single comment by ID.
    
    Public endpoint - no authentication required.
    """
    return await CommentControllers.get_single_comment(comment_id, db)


# ============================================
# USER ROUTES
# ============================================

@CommentRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def create_comment(
    request: Request,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Create a comment on a product.
    
    - **product_id**: ID of the product to comment on
    - **content**: Comment text (1-1000 characters)
    - **rating**: Optional rating (1-5 stars)
    
    Rate limited to 10 comments per minute.
    """
    return await CommentControllers.create_comment(current_user, comment_data, db)


@CommentRouter.get("/my-comments/all", response_model=List[Dict[str, Any]])
async def get_my_comments(
    include_inactive: bool = Query(False, description="Include deleted comments"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get all your own comments.
    
    - **include_inactive**: Include deleted comments (default: false)
    """
    return await CommentControllers.get_user_own_comments(current_user, include_inactive, db)


@CommentRouter.put("/{comment_id}", response_model=Dict[str, Any])
async def update_comment(
    comment_id: int,
    update_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Update your own comment.
    
    - **content**: Updated comment text (optional)
    - **rating**: Updated rating (optional, 1-5 stars)
    
    You can only update your own active comments.
    """
    return await CommentControllers.update_comment(current_user, comment_id, update_data, db)


@CommentRouter.delete("/{comment_id}", response_model=Dict[str, str])
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Soft delete your own comment.
    
    Sets the comment as inactive but keeps it in the database.
    You can only delete your own comments.
    """
    return await CommentControllers.delete_comment(current_user, comment_id, db)


@CommentRouter.delete("/{comment_id}/permanent", response_model=Dict[str, str])
async def permanently_delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Permanently delete your own comment.
    
    WARNING: This action cannot be undone!
    Completely removes the comment from the database.
    You can only permanently delete your own comments.
    """
    return await CommentControllers.hard_delete_own_comment(current_user, comment_id, db)


# ============================================
# ADMIN/STAFF ROUTES
# ============================================

@CommentRouter.get("/admin/all", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_all_comments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    include_inactive: bool = Query(False, description="Include deleted comments"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin/Staff: Get all comments with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **include_inactive**: Include deleted comments (default: false)
    """
    return await CommentControllers.get_all_comments(skip, limit, include_inactive, db)


@CommentRouter.get("/admin/user/{user_id}", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_user_comments(
    user_id: int,
    include_inactive: bool = Query(False, description="Include deleted comments"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin/Staff: Get all comments by a specific user.
    
    - **user_id**: ID of the user
    - **include_inactive**: Include deleted comments (default: false)
    """
    return await CommentControllers.get_all_comments_by_user_id(user_id, include_inactive, db)


@CommentRouter.get("/admin/statistics", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_comment_statistics(db: AsyncSession = Depends(get_db)):
    """
    Admin/Staff: Get comment statistics for dashboard.
    
    Returns:
    - Total/active/inactive comment counts
    - Comments with ratings count
    - Average rating across all comments
    - Top 10 most commented products
    """
    return await CommentControllers.get_comment_statistics(db)


@CommentRouter.post("/{comment_id}/deactivate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def deactivate_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Soft delete any comment.
    
    Sets the comment as inactive but keeps it in the database.
    """
    return await CommentControllers.soft_delete_comment_by_admin(comment_id, db)


@CommentRouter.delete("/admin/{comment_id}/permanent", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def admin_delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Permanently delete any comment.
    
    WARNING: This action cannot be undone!
    Completely removes the comment from the database.
    """
    return await CommentControllers.hard_delete_comment(comment_id, db)
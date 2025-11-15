from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timezone

from Models.COMMENT.CommentModel import Comment
from Models.PRODUCT.BaseProduct.BaseProductModel import Product
from Models.USER.UserModel import User
from Schemas.COMMENT.CommentSchemas import CommentCreate, CommentUpdate


class CommentControllers:
    
    # ============================================
    # USER FUNCTIONS
    # ============================================

    @staticmethod
    async def create_comment(
        current_user: User,
        comment_data: CommentCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User: Create a comment on a product."""
        try:
            # Check if product exists
            product_stmt = select(Product).where(Product.id == comment_data.product_id)
            product_result = await db.execute(product_stmt)
            product = product_result.scalar_one_or_none()
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            
            # Check if product is active
            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot comment on inactive product"
                )
            
            # Create comment
            new_comment = Comment(
                user_id=current_user.id,
                product_id=comment_data.product_id,
                content=comment_data.content,
                rating=comment_data.rating,
                is_active=True
            )
            
            db.add(new_comment)
            await db.commit()
            await db.refresh(new_comment)
            
            return {
                "message": "Comment created successfully",
                "comment": {
                    **new_comment.to_dict(),
                    "username": current_user.username,
                    "product_name": product.name
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create comment: {str(e)}"
            )

    @staticmethod
    async def update_comment(
        current_user: User,
        comment_id: int,
        update_data: CommentUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User: Update their own comment."""
        try:
            stmt = select(Comment).where(Comment.id == comment_id)
            result = await db.execute(stmt)
            comment = result.scalar_one_or_none()
            
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            
            # Check ownership
            if comment.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update your own comments"
                )
            
            # Check if comment is active
            if not comment.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot update inactive comment"
                )
            
            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(comment, key, value)
            
            await db.commit()
            await db.refresh(comment)
            
            return {
                "message": "Comment updated successfully",
                "comment": comment.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update comment: {str(e)}"
            )

    @staticmethod
    async def delete_comment(
        current_user: User,
        comment_id: int,
        db: AsyncSession
    ) -> Dict[str, str]:
        """User: Soft delete their own comment."""
        try:
            stmt = select(Comment).where(Comment.id == comment_id)
            result = await db.execute(stmt)
            comment = result.scalar_one_or_none()
            
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            
            # Check ownership
            if comment.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only delete your own comments"
                )
            
            # Soft delete
            comment.is_active = False
            comment.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            
            return {"message": "Comment deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete comment: {str(e)}"
            )

    @staticmethod
    async def hard_delete_own_comment(
        current_user: User,
        comment_id: int,
        db: AsyncSession
    ) -> Dict[str, str]:
        """User: Permanently delete their own comment."""
        try:
            stmt = select(Comment).where(Comment.id == comment_id)
            result = await db.execute(stmt)
            comment = result.scalar_one_or_none()
            
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            
            # Check ownership
            if comment.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only permanently delete your own comments"
                )
            
            await db.delete(comment)
            await db.commit()
            
            return {"message": "Comment permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to permanently delete comment: {str(e)}"
            )

    @staticmethod
    async def get_user_own_comments(
        current_user: User,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """User: Get all their own comments."""
        try:
            conditions = [Comment.user_id == current_user.id]
            
            if not include_inactive:
                conditions.append(Comment.is_active == True)
            
            stmt = select(Comment).where(and_(*conditions)).order_by(Comment.created_at.desc())
            result = await db.execute(stmt)
            comments = result.scalars().all()
            
            return [
                {
                    **comment.to_dict(),
                    "product_name": comment.product.name if comment.product else None
                }
                for comment in comments
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch comments: {str(e)}"
            )

    @staticmethod
    async def get_single_comment(
        comment_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Public: Get a single comment by ID."""
        try:
            stmt = select(Comment).where(
                and_(
                    Comment.id == comment_id,
                    Comment.is_active == True
                )
            )
            result = await db.execute(stmt)
            comment = result.scalar_one_or_none()
            
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            
            return {
                **comment.to_dict(),
                "username": comment.user.username if comment.user else None,
                "product_name": comment.product.name if comment.product else None
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch comment: {str(e)}"
            )

    # ============================================
    # PUBLIC FUNCTIONS
    # ============================================

    @staticmethod
    async def get_comments_by_product_id(
        product_id: int,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Public: Get all active comments for a product with pagination."""
        try:
            # Check if product exists
            product_stmt = select(Product).where(Product.id == product_id)
            product_result = await db.execute(product_stmt)
            product = product_result.scalar_one_or_none()
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            
            # Get total count
            count_stmt = select(func.count(Comment.id)).where(
                and_(
                    Comment.product_id == product_id,
                    Comment.is_active == True
                )
            )
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            # Get comments
            stmt = select(Comment).where(
                and_(
                    Comment.product_id == product_id,
                    Comment.is_active == True
                )
            ).offset(skip).limit(limit).order_by(Comment.created_at.desc())
            
            result = await db.execute(stmt)
            comments = result.scalars().all()
            
            # Calculate average rating
            avg_rating = None
            if comments:
                ratings = [c.rating for c in comments if c.rating is not None]
                if ratings:
                    avg_rating = sum(ratings) / len(ratings)
            
            return {
                "product_id": product_id,
                "product_name": product.name,
                "total_comments": total,
                "average_rating": round(avg_rating, 2) if avg_rating else None,
                "skip": skip,
                "limit": limit,
                "comments": [
                    {
                        **comment.to_dict(),
                        "username": comment.user.username if comment.user else None
                    }
                    for comment in comments
                ]
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch product comments: {str(e)}"
            )

    # ============================================
    # ADMIN FUNCTIONS
    # ============================================

    @staticmethod
    async def get_all_comments_by_user_id(
        user_id: int,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Admin: Get all comments by a specific user."""
        try:
            # Check if user exists
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            conditions = [Comment.user_id == user_id]
            
            if not include_inactive:
                conditions.append(Comment.is_active == True)
            
            stmt = select(Comment).where(and_(*conditions)).order_by(Comment.created_at.desc())
            result = await db.execute(stmt)
            comments = result.scalars().all()
            
            return [
                {
                    **comment.to_dict(),
                    "username": user.username,
                    "product_name": comment.product.name if comment.product else None
                }
                for comment in comments
            ]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user comments: {str(e)}"
            )

    @staticmethod
    async def hard_delete_comment(
        comment_id: int,
        db: AsyncSession
    ) -> Dict[str, str]:
        """Admin: Permanently delete a comment."""
        try:
            stmt = select(Comment).where(Comment.id == comment_id)
            result = await db.execute(stmt)
            comment = result.scalar_one_or_none()
            
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            
            await db.delete(comment)
            await db.commit()
            
            return {"message": "Comment permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete comment: {str(e)}"
            )

    @staticmethod
    async def get_all_comments(
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Admin: Get all comments with pagination."""
        try:
            conditions = []
            if not include_inactive:
                conditions.append(Comment.is_active == True)
            
            # Get total count
            count_stmt = select(func.count(Comment.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            # Get comments
            stmt = select(Comment).offset(skip).limit(limit).order_by(Comment.created_at.desc())
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            comments = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "comments": [
                    {
                        **comment.to_dict(),
                        "username": comment.user.username if comment.user else None,
                        "product_name": comment.product.name if comment.product else None
                    }
                    for comment in comments
                ]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch comments: {str(e)}"
            )

    @staticmethod
    async def get_comment_statistics(db: AsyncSession) -> Dict[str, Any]:
        """Admin: Get comment statistics."""
        try:
            # Total comments
            total_stmt = select(func.count(Comment.id))
            total_result = await db.execute(total_stmt)
            total_comments = total_result.scalar()
            
            # Active comments
            active_stmt = select(func.count(Comment.id)).where(Comment.is_active == True)
            active_result = await db.execute(active_stmt)
            active_comments = active_result.scalar()
            
            # Inactive comments
            inactive_comments = total_comments - active_comments
            
            # Comments with ratings
            rated_stmt = select(func.count(Comment.id)).where(Comment.rating.isnot(None))
            rated_result = await db.execute(rated_stmt)
            comments_with_ratings = rated_result.scalar()
            
            # Average rating
            avg_rating_stmt = select(func.avg(Comment.rating)).where(Comment.rating.isnot(None))
            avg_rating_result = await db.execute(avg_rating_stmt)
            avg_rating = avg_rating_result.scalar()
            
            # Most commented products (top 10)
            most_commented_stmt = select(
                Comment.product_id,
                func.count(Comment.id).label('count')
            ).where(Comment.is_active == True).group_by(Comment.product_id).order_by(func.count(Comment.id).desc()).limit(10)
            
            most_commented_result = await db.execute(most_commented_stmt)
            most_commented_raw = most_commented_result.all()
            
            # Get product details
            most_commented = []
            for product_id, count in most_commented_raw:
                product_stmt = select(Product).where(Product.id == product_id)
                product_result = await db.execute(product_stmt)
                product = product_result.scalar_one_or_none()
                
                if product:
                    most_commented.append({
                        "product_id": product_id,
                        "product_name": product.name,
                        "comment_count": count
                    })
            
            return {
                "total_comments": total_comments,
                "active_comments": active_comments,
                "inactive_comments": inactive_comments,
                "comments_with_ratings": comments_with_ratings,
                "average_rating": round(float(avg_rating), 2) if avg_rating else None,
                "most_commented_products": most_commented
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch comment statistics: {str(e)}"
            )

    @staticmethod
    async def soft_delete_comment_by_admin(
        comment_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin: Soft delete any comment."""
        try:
            stmt = select(Comment).where(Comment.id == comment_id)
            result = await db.execute(stmt)
            comment = result.scalar_one_or_none()
            
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            
            comment.is_active = False
            comment.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(comment)
            
            return {
                "message": "Comment deactivated successfully",
                "comment": comment.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate comment: {str(e)}"
            )
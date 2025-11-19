from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import List, Dict, Any

from Models.PRODUCT.FavouriteProduct.FavouriteProductModel import FavouriteProduct
from Models.PRODUCT.BaseProduct.BaseProductModel import Product
from Models.USER.UserModel import User
from Schemas.PRODUCT.FavouriteProduct.FavouriteProductSchemas import FavouriteProductCreate


class FavouriteProductControllers:
    
    @staticmethod
    async def user_get_all_favourite_products(
        current_user: User,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """A User gets his/her own favourite products"""
        try:
            #### Load favourites with product relationship ####
            stmt = select(FavouriteProduct).options(
                selectinload(FavouriteProduct.product)
            ).where(
                FavouriteProduct.user_id == current_user.id
            ).order_by(FavouriteProduct.created_at.desc())
            
            result = await db.execute(stmt)
            favourites = result.scalars().all()
            
            return [
                {
                    "id": fav.id,
                    "user_id": fav.user_id,
                    "product_id": fav.product_id,
                    "created_at": fav.created_at.isoformat() if fav.created_at else None,
                    "product": {
                        "id": fav.product.id,
                        "name": fav.product.name,
                        "price": str(fav.product.price),
                        "final_price": str(fav.product.final_price),
                        "image_url": fav.product.image_url,
                        "category": fav.product.category,
                        "description": fav.product.description if fav.product.description else ""
                    } if fav.product else None
                }
                for fav in favourites if fav.product is not None
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch favourite products: {str(e)}"
            )

    @staticmethod
    async def create_favourite_product(
        current_user: User,
        favourite_data: FavouriteProductCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """A User picks a product as his/her favourite product."""
        try:
            #### Check if product exists or not ####
            product_stmt = select(Product).where(Product.id == favourite_data.product_id)
            product_result = await db.execute(product_stmt)
            product = product_result.scalar_one_or_none()
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            
            #### Check if product was already favourited ####
            check_stmt = select(FavouriteProduct).where(
                and_(
                    FavouriteProduct.user_id == current_user.id,
                    FavouriteProduct.product_id == favourite_data.product_id
                )
            )
            check_result = await db.execute(check_stmt)
            existing = check_result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product is already in your favourites"
                )
            
            #### Create favourite ####
            new_favourite = FavouriteProduct(
                user_id=current_user.id,
                product_id=favourite_data.product_id
            )
            
            db.add(new_favourite)
            await db.commit()
            await db.refresh(new_favourite)
            
            return {
                "message": "Product added to favourites",
                "favourite": {
                    "id": new_favourite.id,
                    "product_id": new_favourite.product_id,
                    "product_name": product.name,
                    "created_at": new_favourite.created_at.isoformat() if new_favourite.created_at else None
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add favourite product: {str(e)}"
            )

    @staticmethod
    async def remove_single_favourite_product(
        current_user: User,
        favourite_id: int,
        db: AsyncSession
    ) -> Dict[str, str]:
        """A User removes a single favourite product from his/her favourite products"""
        try:
            stmt = select(FavouriteProduct).where(
                and_(
                    FavouriteProduct.id == favourite_id,
                    FavouriteProduct.user_id == current_user.id
                )
            )
            result = await db.execute(stmt)
            favourite = result.scalar_one_or_none()
            
            if not favourite:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Favourite product not found"
                )
            
            await db.delete(favourite)
            await db.commit()
            
            return {"message": "Product removed from favourites"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove favourite product: {str(e)}"
            )

    @staticmethod
    async def remove_all_favourite_products(
        current_user: User,
        db: AsyncSession
    ) -> Dict[str, str]:
        """A User removes all favourite products from his/her favourite products"""
        try:
            stmt = delete(FavouriteProduct).where(
                FavouriteProduct.user_id == current_user.id
            )
            result = await db.execute(stmt)
            await db.commit()
            
            deleted_count = result.rowcount
            
            return {
                "message": f"Removed {deleted_count} product(s) from favourites"
            }
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove all favourite products: {str(e)}"
            )

    ##############################
        # ADMIN ENDPOINT #
    ##############################
    @staticmethod
    async def admin_gets_user_favourite_products(
        user_id: int,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Admin user gets a user's favourite products"""
        try:
            #### Check if user exists or not ####
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            stmt = select(FavouriteProduct).where(
                FavouriteProduct.user_id == user_id
            ).order_by(FavouriteProduct.created_at.desc())
            
            result = await db.execute(stmt)
            favourites = result.scalars().all()
            
            return [
                {
                    "id": fav.id,
                    "user_id": fav.user_id,
                    "username": user.username,
                    "product_id": fav.product_id,
                    "product_name": fav.product.name if fav.product else None,
                    "created_at": fav.created_at.isoformat() if fav.created_at else None
                }
                for fav in favourites
            ]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user's favourite products: {str(e)}"
            )

    @staticmethod
    async def admin_gets_favourite_products_statistics(
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin user gets favourite products statistics"""
        try:
            #### Total favourites ####
            total_stmt = select(func.count(FavouriteProduct.id))
            total_result = await db.execute(total_stmt)
            total_favourites = total_result.scalar()
            
            #### Unique users with favourites ####
            unique_users_stmt = select(func.count(func.distinct(FavouriteProduct.user_id)))
            unique_users_result = await db.execute(unique_users_stmt)
            unique_users = unique_users_result.scalar()
            
            #### Unique products favourited ####
            unique_products_stmt = select(func.count(func.distinct(FavouriteProduct.product_id)))
            unique_products_result = await db.execute(unique_products_stmt)
            unique_products = unique_products_result.scalar()
            
            #### Most favourited products (top 10) ####
            most_favourited_stmt = select(
                FavouriteProduct.product_id,
                func.count(FavouriteProduct.id).label('count')
            ).group_by(FavouriteProduct.product_id).order_by(func.count(FavouriteProduct.id).desc()).limit(10)
            
            most_favourited_result = await db.execute(most_favourited_stmt)
            most_favourited_raw = most_favourited_result.all()
            
            #### Get product details for most favourited ####
            most_favourited = []
            for product_id, count in most_favourited_raw:
                product_stmt = select(Product).where(Product.id == product_id)
                product_result = await db.execute(product_stmt)
                product = product_result.scalar_one_or_none()
                
                if product:
                    most_favourited.append({
                        "product_id": product_id,
                        "product_name": product.name,
                        "favourite_count": count
                    })
            
            return {
                "total_favourites": total_favourites,
                "unique_users_with_favourites": unique_users,
                "unique_products_favourited": unique_products,
                "most_favourited_products": most_favourited
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch favourite products statistics: {str(e)}"
            )
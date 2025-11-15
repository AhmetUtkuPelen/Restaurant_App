from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timezone

from Models.PRODUCT.Drink.DrinkModel import Drink
from Schemas.PRODUCT.Drink.DrinkSchemas import DrinkCreate, DrinkUpdate


class DrinkControllers:

    @staticmethod
    async def get_all_drinks(
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Get all drinks with pagination."""
        try:
            conditions = []
            if not include_inactive:
                conditions.append(Drink.is_active == True)
            
            count_stmt = select(func.count(Drink.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            stmt = select(Drink).offset(skip).limit(limit).order_by(Drink.created_at.desc())
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            drinks = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "drinks": [drink.to_dict() for drink in drinks]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch drinks: {str(e)}"
            )

    @staticmethod
    async def get_single_drink(drink_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get a single drink by ID."""
        try:
            stmt = select(Drink).where(Drink.id == drink_id)
            result = await db.execute(stmt)
            drink = result.scalar_one_or_none()
            
            if not drink:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Drink not found"
                )
            
            return drink.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch drink: {str(e)}"
            )

    ####
    # ADMIN RELATED ENDPOINTS - REQUIRES ADMIN USER
    ####

    @staticmethod
    async def create_new_drink(drink_data: DrinkCreate, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Create a new drink."""
        try:
            stmt = select(Drink).where(Drink.name == drink_data.name)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Drink with this name already exists"
                )
            
            new_drink = Drink(
                name=drink_data.name,
                description=drink_data.description,
                category=drink_data.category,
                tags=drink_data.tags,
                price=drink_data.price,
                discount_percentage=drink_data.discount_percentage,
                image_url=drink_data.image_url,
                is_active=drink_data.is_active,
                is_front_page=drink_data.is_front_page,
                size=drink_data.size,
                is_acidic=drink_data.is_acidic
            )
            
            db.add(new_drink)
            await db.commit()
            await db.refresh(new_drink)
            
            return {
                "message": "Drink created successfully",
                "drink": new_drink.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create drink: {str(e)}"
            )

    @staticmethod
    async def update_existing_drink(
        drink_id: int,
        update_data: DrinkUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin: Update existing drink."""
        try:
            stmt = select(Drink).where(Drink.id == drink_id)
            result = await db.execute(stmt)
            drink = result.scalar_one_or_none()
            
            if not drink:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Drink not found"
                )
            
            if update_data.name and update_data.name != drink.name:
                check_stmt = select(Drink).where(Drink.name == update_data.name)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Drink with this name already exists"
                    )
            
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(drink, key, value)
            
            await db.commit()
            await db.refresh(drink)
            
            return {
                "message": "Drink updated successfully",
                "drink": drink.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update drink: {str(e)}"
            )

    @staticmethod
    async def hard_delete_drink(drink_id: int, db: AsyncSession) -> Dict[str, str]:
        """Admin: Permanently delete drink."""
        try:
            stmt = select(Drink).where(Drink.id == drink_id)
            result = await db.execute(stmt)
            drink = result.scalar_one_or_none()
            
            if not drink:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Drink not found"
                )
            
            await db.delete(drink)
            await db.commit()
            
            return {"message": f"Drink '{drink.name}' permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete drink: {str(e)}"
            )

    @staticmethod
    async def soft_delete_drink(drink_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Soft delete drink (deactivate)."""
        try:
            stmt = select(Drink).where(Drink.id == drink_id)
            result = await db.execute(stmt)
            drink = result.scalar_one_or_none()
            
            if not drink:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Drink not found"
                )
            
            drink.is_active = False
            drink.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(drink)
            
            return {
                "message": "Drink deactivated successfully",
                "drink": drink.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate drink: {str(e)}"
            )
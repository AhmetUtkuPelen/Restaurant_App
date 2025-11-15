from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timezone

from Models.PRODUCT.Dessert.DessertModel import Dessert
from Schemas.PRODUCT.Dessert.DessertSchemas import DessertCreate, DessertUpdate


class DessertControllers:
    
    @staticmethod
    async def get_all_desserts(
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Get all desserts with pagination."""
        try:
            conditions = []
            if not include_inactive:
                conditions.append(Dessert.is_active == True)
            
            # Get total count
            count_stmt = select(func.count(Dessert.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            # Get desserts
            stmt = select(Dessert).offset(skip).limit(limit).order_by(Dessert.created_at.desc())
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            desserts = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "desserts": [dessert.to_dict() for dessert in desserts]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch desserts: {str(e)}"
            )

    @staticmethod
    async def get_single_dessert(dessert_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get a single dessert by ID."""
        try:
            stmt = select(Dessert).where(Dessert.id == dessert_id)
            result = await db.execute(stmt)
            dessert = result.scalar_one_or_none()
            
            if not dessert:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dessert not found"
                )
            
            return dessert.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch dessert: {str(e)}"
            )

    ####
    # ADMIN RELATED ENDPOINTS - REQUIRES ADMIN USER
    ####

    @staticmethod
    async def create_new_dessert(dessert_data: DessertCreate, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Create a new dessert."""
        try:
            # Check if name already exists
            stmt = select(Dessert).where(Dessert.name == dessert_data.name)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Dessert with this name already exists"
                )
            
            # Create new dessert
            new_dessert = Dessert(
                name=dessert_data.name,
                description=dessert_data.description,
                category=dessert_data.category,
                tags=dessert_data.tags,
                price=dessert_data.price,
                discount_percentage=dessert_data.discount_percentage,
                image_url=dessert_data.image_url,
                is_active=dessert_data.is_active,
                is_front_page=dessert_data.is_front_page,
                is_vegan=dessert_data.is_vegan,
                is_alergic=dessert_data.is_alergic,
                dessert_type=dessert_data.dessert_type,
                calories=dessert_data.calories
            )
            
            db.add(new_dessert)
            await db.commit()
            await db.refresh(new_dessert)
            
            return {
                "message": "Dessert created successfully",
                "dessert": new_dessert.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create dessert: {str(e)}"
            )

    @staticmethod
    async def update_existing_dessert(
        dessert_id: int,
        update_data: DessertUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin: Update existing dessert."""
        try:
            stmt = select(Dessert).where(Dessert.id == dessert_id)
            result = await db.execute(stmt)
            dessert = result.scalar_one_or_none()
            
            if not dessert:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dessert not found"
                )
            
            # Check name uniqueness if being changed
            if update_data.name and update_data.name != dessert.name:
                check_stmt = select(Dessert).where(Dessert.name == update_data.name)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Dessert with this name already exists"
                    )
            
            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(dessert, key, value)
            
            await db.commit()
            await db.refresh(dessert)
            
            return {
                "message": "Dessert updated successfully",
                "dessert": dessert.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update dessert: {str(e)}"
            )

    @staticmethod
    async def hard_delete_dessert(dessert_id: int, db: AsyncSession) -> Dict[str, str]:
        """Admin: Permanently delete dessert."""
        try:
            stmt = select(Dessert).where(Dessert.id == dessert_id)
            result = await db.execute(stmt)
            dessert = result.scalar_one_or_none()
            
            if not dessert:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dessert not found"
                )
            
            await db.delete(dessert)
            await db.commit()
            
            return {"message": f"Dessert '{dessert.name}' permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete dessert: {str(e)}"
            )

    @staticmethod
    async def soft_delete_dessert(dessert_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Soft delete dessert (deactivate)."""
        try:
            stmt = select(Dessert).where(Dessert.id == dessert_id)
            result = await db.execute(stmt)
            dessert = result.scalar_one_or_none()
            
            if not dessert:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Dessert not found"
                )
            
            dessert.is_active = False
            dessert.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(dessert)
            
            return {
                "message": "Dessert deactivated successfully",
                "dessert": dessert.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate dessert: {str(e)}"
            )
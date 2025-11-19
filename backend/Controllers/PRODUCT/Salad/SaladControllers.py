from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timezone

from Models.PRODUCT.Salad.SaladModel import Salad
from Schemas.PRODUCT.Salad.SaladSchemas import SaladCreate, SaladUpdate


class SaladControllers:

    @staticmethod
    async def get_all_salads(
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Get all salads with pagination"""
        try:
            conditions = []
            if not include_inactive:
                conditions.append(Salad.is_active == True)
            
            count_stmt = select(func.count(Salad.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            stmt = select(Salad).offset(skip).limit(limit).order_by(Salad.created_at.desc())
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            salads = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "salads": [salad.to_dict() for salad in salads]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch salads: {str(e)}"
            )

    @staticmethod
    async def get_single_salad(salad_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get a single salad by ID"""
        try:
            stmt = select(Salad).where(Salad.id == salad_id)
            result = await db.execute(stmt)
            salad = result.scalar_one_or_none()
            
            if not salad:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Salad not found"
                )
            
            return salad.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch salad: {str(e)}"
            )

    ##################################################
    # ADMIN RELATED ENDPOINTS - REQUIRES ADMIN USER #
    ##################################################

    @staticmethod
    async def create_new_salad(salad_data: SaladCreate, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Create a new salad."""
        try:
            stmt = select(Salad).where(Salad.name == salad_data.name)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Salad with this name already exists"
                )
            
            new_salad = Salad(
                name=salad_data.name,
                description=salad_data.description,
                category=salad_data.category,
                tags=salad_data.tags,
                price=salad_data.price,
                discount_percentage=salad_data.discount_percentage,
                image_url=salad_data.image_url,
                is_active=salad_data.is_active,
                is_front_page=salad_data.is_front_page,
                is_vegan=salad_data.is_vegan,
                is_alergic=salad_data.is_alergic,
                calories=salad_data.calories
            )
            
            db.add(new_salad)
            await db.commit()
            await db.refresh(new_salad)
            
            return {
                "message": "Salad created successfully",
                "salad": new_salad.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create salad: {str(e)}"
            )

    @staticmethod
    async def update_existing_salad(
        salad_id: int,
        update_data: SaladUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin : Update existing salad"""
        try:
            stmt = select(Salad).where(Salad.id == salad_id)
            result = await db.execute(stmt)
            salad = result.scalar_one_or_none()
            
            if not salad:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Salad not found"
                )
            
            if update_data.name and update_data.name != salad.name:
                check_stmt = select(Salad).where(Salad.name == update_data.name)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Salad with this name already exists"
                    )
            
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(salad, key, value)
            
            await db.commit()
            await db.refresh(salad)
            
            return {
                "message": "Salad updated successfully",
                "salad": salad.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update salad: {str(e)}"
            )

    @staticmethod
    async def hard_delete_salad(salad_id: int, db: AsyncSession) -> Dict[str, str]:
        """Admin : Permanently delete salad"""
        try:
            stmt = select(Salad).where(Salad.id == salad_id)
            result = await db.execute(stmt)
            salad = result.scalar_one_or_none()
            
            if not salad:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Salad not found"
                )
            
            await db.delete(salad)
            await db.commit()
            
            return {"message": f"Salad '{salad.name}' permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete salad: {str(e)}"
            )

    @staticmethod
    async def soft_delete_salad(salad_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin : Soft delete salad (deactivate)"""
        try:
            stmt = select(Salad).where(Salad.id == salad_id)
            result = await db.execute(stmt)
            salad = result.scalar_one_or_none()
            
            if not salad:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Salad not found"
                )
            
            salad.is_active = False
            salad.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(salad)
            
            return {
                "message": "Salad deactivated successfully",
                "salad": salad.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate salad: {str(e)}"
            )
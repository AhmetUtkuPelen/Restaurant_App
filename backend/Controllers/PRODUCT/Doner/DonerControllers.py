from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timezone

from Models.PRODUCT.Doner.DonerModel import Doner
from Schemas.PRODUCT.Doner.DonerSchemas import DonerCreate, DonerUpdate


class DonerControllers:
    
    @staticmethod
    async def get_all_doners(
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Get all doners with pagination """
        try:
            conditions = []
            if not include_inactive:
                conditions.append(Doner.is_active == True)
            
            count_stmt = select(func.count(Doner.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            stmt = select(Doner).offset(skip).limit(limit).order_by(Doner.created_at.desc())
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            doners = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "doners": [doner.to_dict() for doner in doners]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch doners: {str(e)}"
            )

    @staticmethod
    async def get_single_doner(doner_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get a single doner by ID"""
        try:
            stmt = select(Doner).where(Doner.id == doner_id)
            result = await db.execute(stmt)
            doner = result.scalar_one_or_none()
            
            if not doner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doner not found"
                )
            
            return doner.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch doner: {str(e)}"
            )

    #################################################
    # ADMIN RELATED ENDPOINTS - REQUIRES ADMIN USER #
    #################################################

    @staticmethod
    async def create_new_doner(doner_data: DonerCreate, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Create a new doner"""
        try:
            stmt = select(Doner).where(Doner.name == doner_data.name)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Doner with this name already exists"
                )
            
            new_doner = Doner(
                name=doner_data.name,
                description=doner_data.description,
                category=doner_data.category,
                tags=doner_data.tags,
                price=doner_data.price,
                discount_percentage=doner_data.discount_percentage,
                image_url=doner_data.image_url,
                is_active=doner_data.is_active,
                is_front_page=doner_data.is_front_page,
                size=doner_data.size,
                meat_type=doner_data.meat_type,
                spice_level=doner_data.spice_level,
                is_vegan=doner_data.is_vegan,
                is_alergic=doner_data.is_alergic
            )
            
            db.add(new_doner)
            await db.commit()
            await db.refresh(new_doner)
            
            return {
                "message": "Doner created successfully",
                "doner": new_doner.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create doner: {str(e)}"
            )

    @staticmethod
    async def update_existing_doner(
        doner_id: int,
        update_data: DonerUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin: Update existing doner"""
        try:
            stmt = select(Doner).where(Doner.id == doner_id)
            result = await db.execute(stmt)
            doner = result.scalar_one_or_none()
            
            if not doner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doner not found"
                )
            
            if update_data.name and update_data.name != doner.name:
                check_stmt = select(Doner).where(Doner.name == update_data.name)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Doner with this name already exists"
                    )
            
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(doner, key, value)
            
            await db.commit()
            await db.refresh(doner)
            
            return {
                "message": "Doner updated successfully",
                "doner": doner.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update doner: {str(e)}"
            )

    @staticmethod
    async def hard_delete_doner(doner_id: int, db: AsyncSession) -> Dict[str, str]:
        """Admin : Permanently delete doner"""
        try:
            stmt = select(Doner).where(Doner.id == doner_id)
            result = await db.execute(stmt)
            doner = result.scalar_one_or_none()
            
            if not doner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doner not found"
                )
            
            await db.delete(doner)
            await db.commit()
            
            return {"message": f"Doner '{doner.name}' permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete doner: {str(e)}"
            )

    @staticmethod
    async def soft_delete_doner(doner_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin : Soft delete doner (deactivate)"""
        try:
            stmt = select(Doner).where(Doner.id == doner_id)
            result = await db.execute(stmt)
            doner = result.scalar_one_or_none()
            
            if not doner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doner not found"
                )
            
            doner.is_active = False
            doner.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(doner)
            
            return {
                "message": "Doner deactivated successfully",
                "doner": doner.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate doner: {str(e)}"
            )
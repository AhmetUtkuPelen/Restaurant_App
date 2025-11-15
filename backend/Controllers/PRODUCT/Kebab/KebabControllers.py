from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timezone

from Models.PRODUCT.Kebab.KebabModel import Kebab
from Schemas.PRODUCT.Kebab.KebabSchemas import KebabCreate, KebabUpdate


class KebabControllers:

    @staticmethod
    async def get_all_kebabs(
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Get all kebabs with pagination."""
        try:
            conditions = []
            if not include_inactive:
                conditions.append(Kebab.is_active == True)
            
            count_stmt = select(func.count(Kebab.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            stmt = select(Kebab).offset(skip).limit(limit).order_by(Kebab.created_at.desc())
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            kebabs = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "kebabs": [kebab.to_dict() for kebab in kebabs]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch kebabs: {str(e)}"
            )

    @staticmethod
    async def get_single_kebab(kebab_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Get a single kebab by ID."""
        try:
            stmt = select(Kebab).where(Kebab.id == kebab_id)
            result = await db.execute(stmt)
            kebab = result.scalar_one_or_none()
            
            if not kebab:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kebab not found"
                )
            
            return kebab.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch kebab: {str(e)}"
            )

    ####
    # ADMIN RELATED ENDPOINTS - REQUIRES ADMIN USER
    ####

    @staticmethod
    async def create_new_kebab(kebab_data: KebabCreate, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Create a new kebab."""
        try:
            stmt = select(Kebab).where(Kebab.name == kebab_data.name)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Kebab with this name already exists"
                )
            
            new_kebab = Kebab(
                name=kebab_data.name,
                description=kebab_data.description,
                category=kebab_data.category,
                tags=kebab_data.tags,
                price=kebab_data.price,
                discount_percentage=kebab_data.discount_percentage,
                image_url=kebab_data.image_url,
                is_active=kebab_data.is_active,
                is_front_page=kebab_data.is_front_page,
                size=kebab_data.size,
                meat_type=kebab_data.meat_type,
                spice_level=kebab_data.spice_level,
                is_vegan=kebab_data.is_vegan,
                is_alergic=kebab_data.is_alergic
            )
            
            db.add(new_kebab)
            await db.commit()
            await db.refresh(new_kebab)
            
            return {
                "message": "Kebab created successfully",
                "kebab": new_kebab.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create kebab: {str(e)}"
            )

    @staticmethod
    async def update_existing_kebab(
        kebab_id: int,
        update_data: KebabUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin: Update existing kebab."""
        try:
            stmt = select(Kebab).where(Kebab.id == kebab_id)
            result = await db.execute(stmt)
            kebab = result.scalar_one_or_none()
            
            if not kebab:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kebab not found"
                )
            
            if update_data.name and update_data.name != kebab.name:
                check_stmt = select(Kebab).where(Kebab.name == update_data.name)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Kebab with this name already exists"
                    )
            
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(kebab, key, value)
            
            await db.commit()
            await db.refresh(kebab)
            
            return {
                "message": "Kebab updated successfully",
                "kebab": kebab.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update kebab: {str(e)}"
            )

    @staticmethod
    async def hard_delete_kebab(kebab_id: int, db: AsyncSession) -> Dict[str, str]:
        """Admin: Permanently delete kebab."""
        try:
            stmt = select(Kebab).where(Kebab.id == kebab_id)
            result = await db.execute(stmt)
            kebab = result.scalar_one_or_none()
            
            if not kebab:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kebab not found"
                )
            
            await db.delete(kebab)
            await db.commit()
            
            return {"message": f"Kebab '{kebab.name}' permanently deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete kebab: {str(e)}"
            )

    @staticmethod
    async def soft_delete_kebab(kebab_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin: Soft delete kebab (deactivate)."""
        try:
            stmt = select(Kebab).where(Kebab.id == kebab_id)
            result = await db.execute(stmt)
            kebab = result.scalar_one_or_none()
            
            if not kebab:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kebab not found"
                )
            
            kebab.is_active = False
            kebab.deleted_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(kebab)
            
            return {
                "message": "Kebab deactivated successfully",
                "kebab": kebab.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to deactivate kebab: {str(e)}"
            )
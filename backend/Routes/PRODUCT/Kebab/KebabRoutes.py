from fastapi import APIRouter, HTTPException, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from Controllers.PRODUCT.Kebab.KebabControllers import KebabControllers
from Schemas.PRODUCT.Kebab.KebabSchemas import KebabCreate, KebabUpdate
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import require_admin

KebabRouter = APIRouter(prefix="/kebabs", tags=["Kebabs"])


# ============================================ #
            # PUBLIC ROUTES #
# ============================================ #

@KebabRouter.get("/", response_model=Dict[str, Any])
async def get_all_kebabs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    include_inactive: bool = Query(False, description="Include inactive kebabs"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all kebabs with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **include_inactive**: Include inactive kebabs (default: false)
    """
    return await KebabControllers.get_all_kebabs(skip, limit, include_inactive, db)


@KebabRouter.get("/{kebab_id}", response_model=Dict[str, Any])
async def get_kebab_by_id(
    kebab_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single kebab by ID.
    """
    return await KebabControllers.get_single_kebab(kebab_id, db)


# ============================================ #
            # ADMIN ROUTES #
# ============================================ #

@KebabRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
@limiter.limit("10/minute")
async def create_kebab(
    request: Request,
    kebab_data: KebabCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Create a new kebab.
    
    - **name**: Unique kebab name
    - **description**: Kebab description
    - **price**: Price (must be >= 0)
    - **size**: small, medium, or large
    - **meat_type**: chicken, beef, or lamb
    - **spice_level**: mild, medium, or hot
    - **is_vegan**: Whether kebab is vegan
    - **is_alergic**: Whether kebab contains allergens
    - 10 requests per minute for security.
    """
    return await KebabControllers.create_new_kebab(kebab_data, db)


@KebabRouter.put("/{kebab_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def update_kebab(
    kebab_id: int,
    update_data: KebabUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update existing kebab.
    
    All fields are optional. Only provided fields will be updated.
    """
    return await KebabControllers.update_existing_kebab(kebab_id, update_data, db)


@KebabRouter.delete("/{kebab_id}", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def delete_kebab(
    kebab_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Permanently delete kebab.
    """
    return await KebabControllers.hard_delete_kebab(kebab_id, db)


@KebabRouter.post("/{kebab_id}/deactivate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def deactivate_kebab(
    kebab_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Soft delete kebab , is_active (deactivate).
    """
    return await KebabControllers.soft_delete_kebab(kebab_id, db)
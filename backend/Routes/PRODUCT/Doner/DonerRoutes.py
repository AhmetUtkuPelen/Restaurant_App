from fastapi import APIRouter, HTTPException, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from Controllers.PRODUCT.Doner.DonerControllers import DonerControllers
from Schemas.PRODUCT.Doner.DonerSchemas import DonerCreate, DonerUpdate
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import require_admin

DonerRouter = APIRouter(prefix="/doners", tags=["Doners"])


# ============================================
# PUBLIC ROUTES
# ============================================

@DonerRouter.get("/", response_model=Dict[str, Any])
async def get_all_doners(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    include_inactive: bool = Query(False, description="Include inactive doners"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all doners with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **include_inactive**: Include inactive doners (default: false)
    """
    return await DonerControllers.get_all_doners(skip, limit, include_inactive, db)


@DonerRouter.get("/{doner_id}", response_model=Dict[str, Any])
async def get_doner_by_id(
    doner_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single doner by ID.
    """
    return await DonerControllers.get_single_doner(doner_id, db)


# ============================================
# ADMIN ROUTES
# ============================================

@DonerRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
@limiter.limit("10/minute")
async def create_doner(
    request: Request,
    doner_data: DonerCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Create a new doner.
    
    - **name**: Unique doner name
    - **description**: Doner description
    - **price**: Price (must be >= 0)
    - **size**: small, medium, or large
    - **meat_type**: chicken, beef, or lamb
    - **spice_level**: mild, medium, or hot
    - **is_vegan**: Whether doner is vegan
    - **is_alergic**: Whether doner contains allergens
    """
    return await DonerControllers.create_new_doner(doner_data, db)


@DonerRouter.put("/{doner_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def update_doner(
    doner_id: int,
    update_data: DonerUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update existing doner.
    
    All fields are optional. Only provided fields will be updated.
    """
    return await DonerControllers.update_existing_doner(doner_id, update_data, db)


@DonerRouter.delete("/{doner_id}", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def delete_doner(
    doner_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Permanently delete doner.
    
    WARNING: This action cannot be undone!
    """
    return await DonerControllers.hard_delete_doner(doner_id, db)


@DonerRouter.post("/{doner_id}/deactivate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def deactivate_doner(
    doner_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Soft delete doner (deactivate).
    
    Sets is_active to false and records deletion timestamp.
    """
    return await DonerControllers.soft_delete_doner(doner_id, db)
from fastapi import APIRouter, HTTPException, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from Controllers.PRODUCT.Salad.SaladControllers import SaladControllers
from Schemas.PRODUCT.Salad.SaladSchemas import SaladCreate, SaladUpdate
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import require_admin

SaladRouter = APIRouter(prefix="/salads", tags=["Salads"])


# ============================================ #
            # PUBLIC ROUTES #
# ============================================ #

@SaladRouter.get("/", response_model=Dict[str, Any])
async def get_all_salads(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    include_inactive: bool = Query(False, description="Include inactive salads"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all salads with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **include_inactive**: Include inactive salads (default: false)
    """
    return await SaladControllers.get_all_salads(skip, limit, include_inactive, db)


@SaladRouter.get("/{salad_id}", response_model=Dict[str, Any])
async def get_salad_by_id(
    salad_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single salad by ID.
    """
    return await SaladControllers.get_single_salad(salad_id, db)


# ============================================ #
            # ADMIN ROUTES #
# ============================================ #

@SaladRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
@limiter.limit("10/minute")
async def create_salad(
    request: Request,
    salad_data: SaladCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Create a new salad.
    
    - **name**: Unique salad name
    - **description**: Salad description
    - **price**: Price (must be >= 0)
    - **is_vegan**: Whether salad is vegan
    - **is_alergic**: Whether salad contains allergens
    - **calories**: Calorie count
    - 10 requests per minute for security.
    """
    return await SaladControllers.create_new_salad(salad_data, db)


@SaladRouter.put("/{salad_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def update_salad(
    salad_id: int,
    update_data: SaladUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update existing salad.
    
    All fields are optional. Only provided fields will be updated.
    """
    return await SaladControllers.update_existing_salad(salad_id, update_data, db)


@SaladRouter.delete("/{salad_id}", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def delete_salad(
    salad_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Permanently delete salad.
    """
    return await SaladControllers.hard_delete_salad(salad_id, db)


@SaladRouter.post("/{salad_id}/deactivate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def deactivate_salad(
    salad_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Soft delete salad , is_active (deactivate).
    """
    return await SaladControllers.soft_delete_salad(salad_id, db)
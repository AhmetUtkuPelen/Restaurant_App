from fastapi import APIRouter, HTTPException, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from Controllers.PRODUCT.Drink.DrinkControllers import DrinkControllers
from Schemas.PRODUCT.Drink.DrinkSchemas import DrinkCreate, DrinkUpdate
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import require_admin

DrinkRouter = APIRouter(prefix="/drinks", tags=["Drinks"])


# ============================================
# PUBLIC ROUTES
# ============================================

@DrinkRouter.get("/", response_model=Dict[str, Any])
async def get_all_drinks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    include_inactive: bool = Query(False, description="Include inactive drinks"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all drinks with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **include_inactive**: Include inactive drinks (default: false)
    """
    return await DrinkControllers.get_all_drinks(skip, limit, include_inactive, db)


@DrinkRouter.get("/{drink_id}", response_model=Dict[str, Any])
async def get_drink_by_id(
    drink_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single drink by ID.
    """
    return await DrinkControllers.get_single_drink(drink_id, db)


# ============================================
# ADMIN ROUTES
# ============================================

@DrinkRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
@limiter.limit("10/minute")
async def create_drink(
    request: Request,
    drink_data: DrinkCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Create a new drink.
    
    - **name**: Unique drink name
    - **description**: Drink description
    - **price**: Price (must be >= 0)
    - **size**: small, medium, or large
    - **is_acidic**: Whether drink is acidic
    """
    return await DrinkControllers.create_new_drink(drink_data, db)


@DrinkRouter.put("/{drink_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def update_drink(
    drink_id: int,
    update_data: DrinkUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update existing drink.
    
    All fields are optional. Only provided fields will be updated.
    """
    return await DrinkControllers.update_existing_drink(drink_id, update_data, db)


@DrinkRouter.delete("/{drink_id}", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def delete_drink(
    drink_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Permanently delete drink.
    
    WARNING: This action cannot be undone!
    """
    return await DrinkControllers.hard_delete_drink(drink_id, db)


@DrinkRouter.post("/{drink_id}/deactivate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def deactivate_drink(
    drink_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Soft delete drink (deactivate).
    
    Sets is_active to false and records deletion timestamp.
    """
    return await DrinkControllers.soft_delete_drink(drink_id, db)
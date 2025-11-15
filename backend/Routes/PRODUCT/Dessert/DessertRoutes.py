from fastapi import APIRouter, HTTPException, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from Controllers.PRODUCT.Dessert.DessertControllers import DessertControllers
from Schemas.PRODUCT.Dessert.DessertSchemas import DessertCreate, DessertUpdate
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import require_admin

DessertRouter = APIRouter(prefix="/desserts", tags=["Desserts"])


# ============================================
# PUBLIC ROUTES
# ============================================

@DessertRouter.get("/", response_model=Dict[str, Any])
async def get_all_desserts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    include_inactive: bool = Query(False, description="Include inactive desserts"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all desserts with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **include_inactive**: Include inactive desserts (default: false)
    """
    return await DessertControllers.get_all_desserts(skip, limit, include_inactive, db)


@DessertRouter.get("/{dessert_id}", response_model=Dict[str, Any])
async def get_dessert_by_id(
    dessert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single dessert by ID.
    """
    return await DessertControllers.get_single_dessert(dessert_id, db)


# ============================================
# ADMIN ROUTES
# ============================================

@DessertRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
@limiter.limit("10/minute")
async def create_dessert(
    request: Request,
    dessert_data: DessertCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Create a new dessert.
    
    - **name**: Unique dessert name
    - **description**: Dessert description
    - **price**: Price (must be >= 0)
    - **discount_percentage**: Discount (0-100)
    - **is_vegan**: Whether dessert is vegan
    - **is_alergic**: Whether dessert contains allergens
    - **dessert_type**: Type (cake, pastry, ice_cream, pudding, baklava, kunefe, brownie, tiramisu)
    - **calories**: Calorie count
    """
    return await DessertControllers.create_new_dessert(dessert_data, db)


@DessertRouter.put("/{dessert_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def update_dessert(
    dessert_id: int,
    update_data: DessertUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update existing dessert.
    
    All fields are optional. Only provided fields will be updated.
    """
    return await DessertControllers.update_existing_dessert(dessert_id, update_data, db)


@DessertRouter.delete("/{dessert_id}", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def delete_dessert(
    dessert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Permanently delete dessert.
    
    WARNING: This action cannot be undone!
    """
    return await DessertControllers.hard_delete_dessert(dessert_id, db)


@DessertRouter.post("/{dessert_id}/deactivate", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def deactivate_dessert(
    dessert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Soft delete dessert (deactivate).
    
    Sets is_active to false and records deletion timestamp.
    """
    return await DessertControllers.soft_delete_dessert(dessert_id, db)
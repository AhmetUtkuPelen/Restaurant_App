from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime

from Models.RESERVATION.TableModel import Table
from Models.USER.UserModel import User
from Schemas.RESERVATION.TableSchemas import TableCreate, TableUpdate, TableRead
from Controllers.RESERVATION.TableControllers import TableControllers
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Utils.Enums.Enums import UserRole

# Import auth dependencies from UserRoutes
from Routes.USER.UserRoutes import get_current_active_user, require_admin, require_staff_or_admin


TableRouter = APIRouter(prefix="/tables", tags=["Tables"])


# ============================================ #
            # PUBLIC ROUTES #
# ============================================ #

@TableRouter.get("/", response_model=List[Dict[str, Any]])
async def get_all_tables(db: AsyncSession = Depends(get_db)):
    """
    Get all tables in the restaurant.
    
    Public endpoint.
    """
    return await TableControllers.get_all_tables(db)


@TableRouter.get("/{table_id}", response_model=Dict[str, Any])
async def get_table_by_id(
    table_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single table by ID with active reservation count.
    
    Public endpoint.
    """
    return await TableControllers.get_single_table_by_id(table_id, db)


@TableRouter.get("/available/search", response_model=List[Dict[str, Any]])
async def get_available_tables(
    date_time: Optional[datetime] = None,
    min_capacity: Optional[int] = None,
    location: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get available tables with optional filters.
    
    - **date_time**: Check availability at specific datetime (ISO format)
    - **min_capacity**: Minimum table capacity required
    - **location**: Filter by location (window, patio, main_dining_room)
    
    Public endpoint.
    """
    return await TableControllers.get_available_tables(
        date_time=date_time,
        min_capacity=min_capacity,
        location=location,
        db=db
    )


@TableRouter.get("/location/{location}", response_model=List[Dict[str, Any]])
async def get_tables_by_location(
    location: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all tables in a specific location.
    
    - **location**: window, patio, or main_dining_room
    
    Public endpoint.
    """
    return await TableControllers.get_tables_by_location(location, db)


# ============================================ #
            # ADMIN ROUTES #
# ============================================ #

@TableRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
@limiter.limit("10/minute")
async def create_table(
    request: Request,
    table_data: TableCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Create a new table.
    
    - **table_number**: Unique table identifier
    - **capacity**: Number of guests the table can accommodate
    - **location**: window, patio, or main_dining_room
    - **is_available**: Whether the table is available for reservations
    """
    return await TableControllers.add_new_table(table_data, db)


@TableRouter.put("/{table_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def update_table(
    table_id: int,
    update_data: TableUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Update existing table information.
    
    All fields are optional. Only provided fields will be updated.
    """
    return await TableControllers.update_existing_table(table_id, update_data, db)


@TableRouter.delete("/{table_id}", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def delete_table(
    table_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Delete a table.
    
    Only allowed if no active reservations exist for this table.
    """
    return await TableControllers.delete_table(table_id, db)


@TableRouter.post("/{table_id}/toggle-availability", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def toggle_table_availability(
    table_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Toggle table availability status.
    
    Switches Table availability status between available and unavailable.
    """
    return await TableControllers.toggle_table_availability(table_id, db)
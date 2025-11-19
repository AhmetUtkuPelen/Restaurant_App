from fastapi import APIRouter, HTTPException, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime

from Controllers.RESERVATION.ReservationControllers import ReservationControllers
from Schemas.RESERVATION.ReservationSchemas import ReservationCreate, ReservationUpdate, ReservationRead
from Models.USER.UserModel import User
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Utils.Enums.Enums import ReservationStatus

# Import auth dependencies from UserRoutes
from Routes.USER.UserRoutes import get_current_active_user, require_admin, require_staff_or_admin


ReservationRouter = APIRouter(prefix="/reservations", tags=["Reservations"])


# ============================================ #
            # USER ROUTES #
# ============================================ #

@ReservationRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
@limiter.limit("5/minute")
async def create_reservation(
    request: Request,
    reservation_data: ReservationCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User : Create a new reservation.
    
    - **table_id**: ID of the table to reserve
    - **reservation_time**: Datetime for the reservation (must be in future)
    - **number_of_guests**: Number of guests (1-20)
    - **special_requests**: Optional special requests or notes (can be null in front end)

    - Rate limited to 5 reservations per minute for security.
    
    The system checks:
    - Table exists and if is available
    - Table capacity is sufficient
    - Time slot is available (2-hour time window)
    """
    return await ReservationControllers.create_new_reservation(
        current_user, reservation_data, db
    )


@ReservationRouter.get("/my-reservations", response_model=List[Dict[str, Any]])
async def get_my_reservations(
    include_cancelled: bool = Query(False, description="Include cancelled reservations"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User : Get all your own reservations.
    
    - **include_cancelled**: Set to true to include cancelled reservations
    """
    return await ReservationControllers.get_users_all_reservations(
        current_user, include_cancelled, db
    )


@ReservationRouter.get("/my-reservations/{reservation_id}", response_model=Dict[str, Any])
async def get_my_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User : Get a single reservation by ID.
    
    You can only view your own reservations.
    """
    return await ReservationControllers.get_user_single_reservation_by_id(
        current_user, reservation_id, db
    )


@ReservationRouter.put("/{reservation_id}", response_model=Dict[str, Any])
async def update_reservation(
    reservation_id: int,
    update_data: ReservationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Update your own reservation.
    
    All fields are optional. Only provided fields will be updated.
    
    You can only update your own reservations.
    Cant update cancelled reservations.
    """
    return await ReservationControllers.update_existing_reservation(
        current_user, reservation_id, update_data, db
    )


@ReservationRouter.post("/{reservation_id}/cancel", response_model=Dict[str, str])
async def cancel_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User : Cancel your own reservation.
    
    You can only cancel your own reservations.
    """
    return await ReservationControllers.cancel_existing_reservation(
        current_user, reservation_id, db
    )


# ============================================ #
        # ADMIN/STAFF ROUTES #
# ============================================ #

@ReservationRouter.get("/admin/all", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_all_reservations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    status_filter: Optional[ReservationStatus] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all reservations with pagination and filtering.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 500)
    - **status_filter**: Filter by status (pending, confirmed, cancelled)
    """
    return await ReservationControllers.get_all_reservations(
        skip, limit, status_filter, db
    )


@ReservationRouter.post("/{reservation_id}/confirm", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def confirm_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Confirm a pending reservation.
    
    Changes status from PENDING to CONFIRMED.
    """
    return await ReservationControllers.confirm_reservation(reservation_id, db)


@ReservationRouter.get("/admin/by-date", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_reservations_by_date(
    date: datetime = Query(..., description="Date to filter reservations (ISO format)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all reservations for a specific date.
    """
    return await ReservationControllers.get_reservations_by_date(date, db)


@ReservationRouter.get("/admin/upcoming", response_model=List[Dict[str, Any]], dependencies=[Depends(require_staff_or_admin)])
async def get_upcoming_reservations(
    days: int = Query(7, ge=1, le=90, description="Number of days to look ahead"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get upcoming reservations for the next X days.
    
    - **days**: Number of days to look ahead (default: 7, max: 90)
    
    Only includes PENDING and CONFIRMED reservations.
    """
    return await ReservationControllers.get_upcoming_reservations(days, db)


@ReservationRouter.get("/admin/statistics", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_reservation_statistics(db: AsyncSession = Depends(get_db)):
    """
    Admin : Get reservation statistics for dashboard.
    
    - Total reservations
    - Count by status (pending, confirmed, cancelled)
    - Upcoming reservations (next 7 days)
    - Today's reservations
    """
    return await ReservationControllers.get_reservation_statistics(db)
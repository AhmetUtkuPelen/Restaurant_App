from fastapi import APIRouter, Depends, status, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional

from Controllers.PAYMENT.PaymentControllers import PaymentControllers
from Schemas.PAYMENT.PaymentSchemas import PaymentCreate, PaymentUpdate
from Models.USER.UserModel import User
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Utils.Enums.Enums import PaymentStatus
from Routes.USER.UserRoutes import get_current_active_user, require_admin, require_staff_or_admin

PaymentRouter = APIRouter(prefix="/payments", tags=["Payments"])


# ============================================
# USER ROUTES
# ============================================

@PaymentRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
@limiter.limit("5/minute")
async def create_payment(
    request: Request,
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Create a payment for orders or reservation.
    
    - **order_ids**: List of order IDs to pay for (optional)
    - **reservation_id**: Reservation ID to pay for (optional)
    - **amount**: Payment amount (must match calculated total)
    - **currency**: Currency code (default: TRY)
    - **installment**: Number of installments (1-12, default: 1)
    - **ip_address**: User's IP address (required by Iyzico)
    - **metadata**: Optional metadata
    
    Must provide either order_ids or reservation_id.
    Rate limited to 5 payments per minute.
    
    NOTE: This is a test implementation. In production, you would be redirected to Iyzico payment page.
    """
    return await PaymentControllers.create_payment(current_user, payment_data, db)


@PaymentRouter.get("/my-payments", response_model=Dict[str, Any])
async def get_my_payments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    status_filter: Optional[PaymentStatus] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get all your own payments.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **status_filter**: Filter by payment status (pending, completed, failed, refunded)
    """
    return await PaymentControllers.get_user_payments(current_user, skip, limit, status_filter, db)


@PaymentRouter.get("/my-payments/{payment_id}", response_model=Dict[str, Any])
async def get_my_payment(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get a single payment by ID.
    
    You can only view your own payments.
    """
    return await PaymentControllers.get_payment_by_id(current_user, payment_id, db)


@PaymentRouter.post("/{payment_id}/complete-test", response_model=Dict[str, Any])
async def simulate_payment_completion(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Simulate payment completion (TEST MODE ONLY).
    
    This endpoint simulates a successful payment completion for testing purposes.
    In production, payment completion would be handled by Iyzico callback.
    
    - Marks payment as completed
    - Updates related orders to completed
    - Confirms related reservations
    """
    return await PaymentControllers.simulate_payment_completion(current_user, payment_id, db)


# ============================================
# ADMIN/STAFF ROUTES
# ============================================

@PaymentRouter.get("/admin/all", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_all_payments(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    status_filter: Optional[PaymentStatus] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin/Staff: Get all payments with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **status_filter**: Filter by payment status
    """
    return await PaymentControllers.admin_get_all_payments(skip, limit, status_filter, db)


@PaymentRouter.get("/admin/{payment_id}", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_payment_by_id(
    payment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin/Staff: Get any payment by ID.
    
    Returns detailed payment information including user details.
    """
    return await PaymentControllers.admin_get_payment_by_id(payment_id, db)


@PaymentRouter.put("/admin/{payment_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def admin_update_payment(
    payment_id: int,
    update_data: PaymentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update payment status and details.
    
    - **status**: Update payment status
    - **provider_payment_id**: Iyzico payment ID
    - **fraud_status**: Fraud detection status
    - **card_info**: Card information
    """
    return await PaymentControllers.admin_update_payment(payment_id, update_data, db)


@PaymentRouter.get("/admin/statistics", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_payment_statistics(db: AsyncSession = Depends(get_db)):
    """
    Admin/Staff: Get payment statistics.
    
    Returns:
    - Total payments count
    - Payments by status (pending, completed, failed)
    - Revenue statistics (total, average payment)
    """
    return await PaymentControllers.admin_get_payment_statistics(db)


@PaymentRouter.get("/admin/user/{user_id}", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_user_payments(
    user_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin/Staff: Get all payments for a specific user.
    
    - **user_id**: ID of the user
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    """
    return await PaymentControllers.admin_get_user_payments(user_id, skip, limit, db)
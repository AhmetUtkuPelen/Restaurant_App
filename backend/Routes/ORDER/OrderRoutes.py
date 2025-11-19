from fastapi import APIRouter, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from datetime import datetime

from Controllers.ORDER.OrderControllers import OrderControllers
from Schemas.ORDER.OrderSchemas import OrderCreate, OrderUpdate
from Models.USER.UserModel import User
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Utils.Enums.Enums import OrderStatus
from Routes.USER.UserRoutes import get_current_active_user, require_admin, require_staff_or_admin

OrderRouter = APIRouter(prefix="/orders", tags=["Orders"])


# ============================================ #
            # USER ROUTES #
# ============================================ #

@OrderRouter.get("/my-orders", response_model=Dict[str, Any])
async def get_my_orders(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    status_filter: Optional[OrderStatus] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get all your own orders.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **status_filter**: Filter by order status (pending, completed, cancelled)
    """
    return await OrderControllers.user_get_all_orders(current_user, skip, limit, status_filter, db)


@OrderRouter.get("/my-orders/{order_id}", response_model=Dict[str, Any])
async def get_my_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get a single order by ID.
    
    You can only view your own orders.
    Detailed order information including all items.
    """
    return await OrderControllers.user_get_order_by_id(current_user, order_id, db)


@OrderRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def create_order(
    request: Request,
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Create a new order from cart items.
    
    - **delivery_address**: Delivery address (uses user's address if not provided)
    - **special_instructions**: Special instructions for the order (optional , can be null in front end)
    
    Creates order from all items currently in your cart.
    Cart will be cleared out after successful order creation.
    Rate limited to 10 orders per minute for security.
    """
    return await OrderControllers.user_create_new_order(current_user, order_data, db)


@OrderRouter.put("/{order_id}", response_model=Dict[str, Any])
async def update_my_order(
    order_id: int,
    update_data: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Update your own order.
    
    - **delivery_address**: Updated delivery address (optional)
    - **special_instructions**: Updated special instructions (optional)
    
    You can only update:
    - Your own orders
    - Orders with PENDING status
    - Delivery address and special instructions only
    """
    return await OrderControllers.user_update_order(current_user, order_id, update_data, db)


@OrderRouter.post("/{order_id}/cancel", response_model=Dict[str, str])
async def cancel_my_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Cancel your own order.
    
    You can only cancel:
    - Your own orders
    - Orders with PENDING status
    """
    return await OrderControllers.user_cancels_order(current_user, order_id, db)


# ============================================ #
            # ADMIN/STAFF ROUTES #
# ============================================ #

@OrderRouter.get("/admin/all", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_all_orders(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    status_filter: Optional[OrderStatus] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all orders with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    - **status_filter**: Filter by order status (pending, completed, cancelled)
    """
    return await OrderControllers.admin_get_all_orders(skip, limit, status_filter, db)


@OrderRouter.get("/admin/{order_id}", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_order_by_id(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get any order by ID.
    
    Detailed order information including all items and user details.
    """
    return await OrderControllers.admin_get_order_by_id(order_id, db)


@OrderRouter.get("/admin/user/{user_id}", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_user_orders(
    user_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all orders for a specific user.
    
    - **user_id**: ID of the user
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    """
    return await OrderControllers.admin_get_single_user_all_orders(user_id, skip, limit, db)


@OrderRouter.put("/admin/{order_id}", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def admin_update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Update any order.
    
    - **status**: Update order status (pending, completed, cancelled)
    - **delivery_address**: Update delivery address (optional)
    - **special_instructions**: Update special instructions (optional)
    
    Admin can update all fields including status.
    """
    return await OrderControllers.admin_update_order(order_id, update_data, db)


@OrderRouter.post("/admin/{order_id}/cancel", response_model=Dict[str, str], dependencies=[Depends(require_admin)])
async def admin_cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Cancel any order.
    
    Cant cancel orders that are completed status.
    """
    return await OrderControllers.admin_cancels_order(order_id, db)


@OrderRouter.get("/admin/statistics/overview", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_order_statistics(db: AsyncSession = Depends(get_db)):
    """
    Admin : Get comprehensive order statistics.
    
    - Total orders count
    - Orders by status (pending, completed, cancelled)
    - Revenue statistics (total, average order value)
    - Recent orders (today , this month)
    """
    return await OrderControllers.admin_get_order_statistics(db)


@OrderRouter.get("/admin/statistics/product/{product_id}", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_product_order_statistics(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get order statistics for a specific product.
    
    - **product_id**: ID of the product
    
    - Times ordered
    - Total quantity sold
    - Total revenue from this product
    """
    return await OrderControllers.admin_get_order_statistics_by_product_id(product_id, db)


@OrderRouter.get("/admin/statistics/user/{user_id}", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_user_order_statistics(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get order statistics for a specific user.
    
    - **user_id**: ID of the user
    
    - Total orders
    - Completed orders
    - Total spent
    - Average order value
    """
    return await OrderControllers.admin_get_order_statistics_by_user_id(user_id, db)


@OrderRouter.get("/admin/statistics/date-range", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_date_range_statistics(
    start_date: datetime = Query(..., description="Start date (ISO format)"),
    end_date: datetime = Query(..., description="End date (ISO format)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get order statistics for a date range.
    
    - **start_date**: Start date in ISO format (e.g., 2024-01-01T00:00:00)
    - **end_date**: End date in ISO format (e.g., 2024-12-31T23:59:59)
    
    - Total orders in range
    - Completed orders in range
    - Total revenue in range
    """
    return await OrderControllers.admin_get_order_statistics_by_date(start_date, end_date, db)
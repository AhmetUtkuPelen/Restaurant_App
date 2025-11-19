from fastapi import APIRouter, HTTPException, status, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from Controllers.CART.CartControllers import CartControllers
from Schemas.CART.CartSchemas import CartItemCreate, CartItemUpdate
from Models.USER.UserModel import User
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import get_current_active_user, require_admin, require_staff_or_admin

CartRouter = APIRouter(prefix="/cart", tags=["Cart"])


# ============================================ #
            # USER ROUTES #
# ============================================ #

@CartRouter.get("/", response_model=Dict[str, Any])
async def get_my_cart(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get your cart with all items and totals.
    
    - Cart details with all items
    - Product information for each item
    - Calculated subtotals and total price
    - Total item count
    """
    return await CartControllers.get_user_cart(current_user, db)


@CartRouter.get("/summary", response_model=Dict[str, Any])
async def get_cart_summary(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get cart summary.
    Returns only total product number without detailed item information.
    For displaying cart badge in front end.
    """
    return await CartControllers.get_cart_summary(current_user, db)


@CartRouter.post("/items", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
@limiter.limit("30/minute")
async def add_item_to_cart(
    request: Request,
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User : Add item to cart.
    
    - **product_id** : ID of the product to add
    - **quantity**: Quantity to add (default: 1, minimum: 1)
    
    If the product already exists in cart, the quantity gets to be increased.
    Rate limited to 30 requests per minute for security.
    """
    return await CartControllers.add_item_to_cart(current_user, item_data, db)


@CartRouter.put("/items/{item_id}", response_model=Dict[str, Any])
async def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Update cart item quantity
    
    - **item_id** : ID of the cart item to update
    - **quantity** : New quantity (minimum: 1)
    
    You can only update items in your own cart
    """
    return await CartControllers.update_cart_item(current_user, item_id, item_data, db)


@CartRouter.delete("/items/{item_id}", response_model=Dict[str, str])
async def remove_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User : Remove item from cart
    
    - **item_id**: ID of the cart item to remove
    
    You can only remove items from your own cart.
    """
    return await CartControllers.remove_cart_item(current_user, item_id, db)


@CartRouter.delete("/clear", response_model=Dict[str, str])
async def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Clear all items from your cart
    Remove all Items from your Cart
    """
    return await CartControllers.clear_cart(current_user, db)


# ============================================ #
            # ADMIN ROUTES #
# ============================================ #

@CartRouter.get("/admin/user/{user_id}", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_user_cart_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get cart for a specific user.
    
    - **user_id**: ID of the user
    
    Returns the user's cart with all items and totals.
    """
    return await CartControllers.get_single_cart_for_user_by_id(user_id, db)


@CartRouter.get("/admin/active", response_model=Dict[str, Any], dependencies=[Depends(require_staff_or_admin)])
async def get_all_active_carts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin : Get all carts that have items.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 500)
    
    Returns only carts with at least one item.
    For monitoring abandoned carts by User.
    """
    return await CartControllers.get_all_active_carts(skip, limit, db)
from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from Controllers.PRODUCT.FavouriteProduct.FavouriteProductControllers import FavouriteProductControllers
from Schemas.PRODUCT.FavouriteProduct.FavouriteProductSchemas import FavouriteProductCreate
from Models.USER.UserModel import User
from Database.Database import get_db
from Utils.SlowApi.SlowApi import limiter
from Routes.USER.UserRoutes import get_current_active_user, require_admin

FavouriteProductRouter = APIRouter(prefix="/favourites", tags=["Favourites"])


# ============================================ #
            # USER ROUTES #
# ============================================ #

@FavouriteProductRouter.get("/my-favourites", response_model=List[Dict[str, Any]])
async def get_my_favourite_products(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Get all your favourite products.
    
    Returns list of favourites with product details including:
    - Product ID, name, price, final price, image
    - Date added to favourites
    """
    return await FavouriteProductControllers.user_get_all_favourite_products(current_user, db)


@FavouriteProductRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
@limiter.limit("20/minute")
async def add_favourite_product(
    request: Request,
    favourite_data: FavouriteProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Add a product to your favourites.
    
    - **product_id**: ID of the product to add to favourites
    
    Cannot add the same product twice.
    Rate limited to 20 requests per minute for security.
    """
    return await FavouriteProductControllers.create_favourite_product(
        current_user, favourite_data, db
    )


@FavouriteProductRouter.delete("/{favourite_id}", response_model=Dict[str, str])
async def remove_favourite_product(
    favourite_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Remove a product from your favourites.
    
    You can only remove your own favourites.
    """
    return await FavouriteProductControllers.remove_single_favourite_product(
        current_user, favourite_id, db
    )


@FavouriteProductRouter.delete("/", response_model=Dict[str, str])
async def clear_all_favourites(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    User: Remove all products from your favourites.
    """
    return await FavouriteProductControllers.remove_all_favourite_products(current_user, db)


# ============================================ #
            # ADMIN ROUTES #
# ============================================ #

@FavouriteProductRouter.get("/admin/user/{user_id}", response_model=List[Dict[str, Any]], dependencies=[Depends(require_admin)])
async def get_user_favourites(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Get a specific user's favourite products.
    
    List of user's favourites with product details.
    """
    return await FavouriteProductControllers.admin_gets_user_favourite_products(user_id, db)


@FavouriteProductRouter.get("/admin/statistics", response_model=Dict[str, Any], dependencies=[Depends(require_admin)])
async def get_favourites_statistics(db: AsyncSession = Depends(get_db)):
    """
    Admin: Get favourite products statistics.

    - Total favourites count
    - Unique users with favourites
    - Unique products favourited
    - Top 10 most favourited products
    """
    return await FavouriteProductControllers.admin_gets_favourite_products_statistics(db)
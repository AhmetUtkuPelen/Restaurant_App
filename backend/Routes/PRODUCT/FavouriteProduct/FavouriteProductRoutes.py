from fastapi import APIRouter, HTTPException, status
from Controllers.PRODUCT.FavouriteProduct.FavouriteProductControllers import FavouriteProductControllers
from Schemas.PRODUCT.FavouriteProduct.FavouriteProductSchemas import FavouriteProductCreate

from Utils.SlowApi.SlowApi import limiter

FAvouriteProductRouter = APIRouter(prefix="/favourites", tags=["Favourites"])
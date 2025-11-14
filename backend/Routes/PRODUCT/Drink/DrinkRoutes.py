from fastapi import APIRouter, HTTPException, status
from Controllers.PRODUCT.Drink.DrinkControllers import DrinkControllers
from Schemas.PRODUCT.Drink.DrinkSchemas import DrinkCreate, DrinkUpdate

from Utils.SlowApi.SlowApi import limiter

DrinkRouter = APIRouter(prefix="/drinks", tags=["Drinks"])
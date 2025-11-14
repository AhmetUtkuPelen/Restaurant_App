from fastapi import APIRouter, HTTPException, status
from Controllers.PRODUCT.Doner.DonerControllers import DonerControllers
from Schemas.PRODUCT.Doner.DonerSchemas import DonerCreate, DonerUpdate
from Schemas.PRODUCT.Doner.DonerIngredientSchemas import DonerIngredientCreate, DonerIngredientUpdate

from Utils.SlowApi.SlowApi import limiter

DonerRouter = APIRouter(prefix="/doners", tags=["Doners"])
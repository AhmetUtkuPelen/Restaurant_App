from fastapi import APIRouter, HTTPException, status
from Controllers.PRODUCT.Salad.SaladControllers import SaladControllers
from Schemas.PRODUCT.Salad.SaladSchemas import SaladCreate, SaladUpdate

from Utils.SlowApi.SlowApi import limiter

SaladRouter = APIRouter(prefix="/salads", tags=["Salads"])
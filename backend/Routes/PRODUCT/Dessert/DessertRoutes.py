from fastapi import APIRouter, HTTPException, status, Request
from Controllers.PRODUCT.Dessert.DessertControllers import DessertControllers
from Schemas.PRODUCT.Dessert.DessertSchemas import DessertCreate, DessertUpdate
from Utils.SlowApi.SlowApi import limiter

DessertRouter = APIRouter(prefix="/desserts", tags=["Desserts"])
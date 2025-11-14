from fastapi import APIRouter, HTTPException, status
from Controllers.ORDER.OrderControllers import OrderControllers
from Schemas.ORDER.OrderSchemas import OrderCreate
from datetime import datetime

OrderRouter = APIRouter(prefix="/orders", tags=["Orders"])
from fastapi import APIRouter, HTTPException, status
from Controllers.CART.CartControllers import CartControllers
from Schemas.CART.CartSchemas import CartItemCreate

CartRouter = APIRouter(prefix="/cart", tags=["Cart"])
from fastapi import APIRouter, HTTPException, status
from Controllers.PRODUCT.Kebab.KebabControllers import KebabControllers
from Schemas.PRODUCT.Kebab.KebabSchemas import KebabCreate, KebabUpdate

from Utils.SlowApi.SlowApi import limiter

KebabRouter = APIRouter(prefix="/kebabs", tags=["Kebabs"])
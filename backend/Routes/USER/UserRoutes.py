from fastapi import APIRouter, HTTPException, status
from Controllers.USER.UserControllers import UserControllers
from Schemas.USER.UserSchemas import UserRegister, UserLogin, UserProfileUpdate

from Utils.SlowApi.SlowApi import limiter

UserRouter = APIRouter(prefix="/users", tags=["Users"])
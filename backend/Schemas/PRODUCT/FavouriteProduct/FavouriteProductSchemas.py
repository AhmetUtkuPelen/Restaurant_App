from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

model_conf = ConfigDict(from_attributes=True, orm_mode=True)


class FavouriteProductBase(BaseModel):
    model_config = model_conf
    user_id: int
    product_id: int


class FavouriteProductCreate(BaseModel):
    model_config = model_conf
    product_id: int  # user_id will come from authenticated user


class FavouriteProductRead(FavouriteProductBase):
    model_config = model_conf
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class FavouriteProductInDB(FavouriteProductRead):
    model_config = model_conf
    deleted_at: Optional[datetime] = None
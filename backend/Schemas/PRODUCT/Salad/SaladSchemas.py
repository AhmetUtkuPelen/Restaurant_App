from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from Schemas.PRODUCT.BaseProduct.BaseProductSchemas import ProductBase, ProductBaseCreate, ProductBaseUpdate, ProductBaseRead

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


### SALAD BASE SCHEMA ###
class SaladBase(BaseModel):
    model_config = model_conf
    is_vegan: bool = False
    is_alergic: bool = False
    calories: int = Field(default=0, ge=0)


### SALAD CREATE SCHEMA ###
class SaladCreate(ProductBaseCreate, SaladBase):
    model_config = model_conf
    category: str = "salad"


### SALAD UPDATE SCHEMA ###
class SaladUpdate(ProductBaseUpdate):
    model_config = model_conf
    is_vegan: Optional[bool] = None
    is_alergic: Optional[bool] = None
    calories: Optional[int] = Field(None, ge=0)


### SALAD READ SCHEMA ###
class SaladRead(ProductBaseRead, SaladBase):
    model_config = model_conf
    pass


### SALAD IN DB SCHEMA ###
class SaladInDB(SaladRead):
    model_config = model_conf
    pass
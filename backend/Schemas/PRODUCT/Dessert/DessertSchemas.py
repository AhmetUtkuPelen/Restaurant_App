from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from decimal import Decimal
from Schemas.PRODUCT.BaseProduct.BaseProductSchemas import ProductBase, ProductBaseCreate, ProductBaseUpdate, ProductBaseRead
from Utils.Enums.Enums import DessertType

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


### DESSERT BASE SCHEMA ###
class DessertBase(BaseModel):
    model_config = model_conf
    is_vegan: bool
    is_alergic: bool
    dessert_type: DessertType
    calories: int = Field(..., ge=0)


### DESSERT CREATE SCHEMA ###
class DessertCreate(ProductBaseCreate, DessertBase):
    model_config = model_conf
    category: str = "dessert"


### DESSERT UPDATE SCHEMA ###
class DessertUpdate(ProductBaseUpdate):
    model_config = model_conf
    is_vegan: Optional[bool] = None
    is_alergic: Optional[bool] = None
    dessert_type: Optional[DessertType] = None
    calories: Optional[int] = Field(None, ge=0)


### DESSERT READ SCHEMA ###
class DessertRead(ProductBaseRead, DessertBase):
    model_config = model_conf
    pass


### DESSERT IN DB SCHEMA ###
class DessertInDB(DessertRead):
    model_config = model_conf
    pass
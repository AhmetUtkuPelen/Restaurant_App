from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from Schemas.PRODUCT.BaseProduct.BaseProductSchemas import ProductBase, ProductBaseCreate, ProductBaseUpdate, ProductBaseRead
from Utils.Enums.Enums import DonerSize, MeatType, SpiceLevel
from decimal import Decimal

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


### DONER BASE SCHEMA ###
class DonerBase(BaseModel):
    model_config = model_conf
    size: DonerSize = DonerSize.MEDIUM
    meat_type: MeatType
    spice_level: SpiceLevel = SpiceLevel.MEDIUM
    is_vegan: bool = False
    is_alergic: bool = False


### DONER CREATE SCHEMA ###
class DonerCreate(ProductBaseCreate, DonerBase):
    model_config = model_conf
    category: str = "doner"


### DONER UPDATE SCHEMA ###
class DonerUpdate(ProductBaseUpdate):
    model_config = model_conf
    size: Optional[DonerSize] = None
    meat_type: Optional[MeatType] = None
    spice_level: Optional[SpiceLevel] = None
    is_vegan: Optional[bool] = None
    is_alergic: Optional[bool] = None


### DONER READ SCHEMA ###
class DonerRead(ProductBaseRead, DonerBase):
    model_config = model_conf
    pass


### DONER IN DB SCHEMA ###
class DonerInDB(DonerRead):
    model_config = model_conf
    pass
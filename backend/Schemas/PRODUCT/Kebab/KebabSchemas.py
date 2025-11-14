from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from Schemas.PRODUCT.BaseProduct.BaseProductSchemas import ProductBase, ProductBaseCreate, ProductBaseUpdate, ProductBaseRead
from Utils.Enums.Enums import MeatType, SpiceLevel, KebabSize
from decimal import Decimal

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


### KEBAB BASE SCHEMA ###
class KebabBase(BaseModel):
    model_config = model_conf
    size: KebabSize = KebabSize.MEDIUM
    meat_type: MeatType
    spice_level: SpiceLevel = SpiceLevel.MEDIUM
    is_vegan: bool = False
    is_alergic: bool = False


### KEBAB CREATE SCHEMA ###
class KebabCreate(ProductBaseCreate, KebabBase):
    model_config = model_conf
    category: str = "kebab"


### KEBAB UPDATE SCHEMA ###
class KebabUpdate(ProductBaseUpdate):
    model_config = model_conf
    size: Optional[KebabSize] = None
    meat_type: Optional[MeatType] = None
    spice_level: Optional[SpiceLevel] = None
    is_vegan: Optional[bool] = None
    is_alergic: Optional[bool] = None


### KEBAB READ SCHEMA ###
class KebabRead(ProductBaseRead, KebabBase):
    model_config = model_conf
    pass


### KEBAB IN DB SCHEMA ###
class KebabInDB(KebabRead):
    model_config = model_conf
    pass
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from Schemas.PRODUCT.BaseProduct.BaseProductSchemas import ProductBase, ProductBaseCreate, ProductBaseUpdate, ProductBaseRead
from Utils.Enums.Enums import DrinkSize

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


### DRINK BASE SCHEMA ###
class DrinkBase(BaseModel):
    model_config = model_conf
    size: DrinkSize = DrinkSize.MEDIUM
    is_acidic: bool = False


### DRINK CREATE SCHEMA ###
class DrinkCreate(ProductBaseCreate, DrinkBase):
    model_config = model_conf
    category: str = "drink"


### DRINK UPDATE SCHEMA ###
class DrinkUpdate(ProductBaseUpdate):
    model_config = model_conf
    size: Optional[DrinkSize] = None
    is_acidic: Optional[bool] = None


### DRINK READ SCHEMA ###
class DrinkRead(ProductBaseRead, DrinkBase):
    model_config = model_conf
    pass


### DRINK IN DB SCHEMA ###
class DrinkInDB(DrinkRead):
    model_config = model_conf
    pass
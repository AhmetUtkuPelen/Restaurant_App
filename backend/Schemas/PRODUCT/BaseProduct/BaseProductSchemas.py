from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


### BASE PRODUCT SCHEMA ###
class ProductBase(BaseModel):
    model_config = model_conf
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: str
    tags: Optional[List[str]] = Field(default_factory=list)
    price: Decimal = Field(..., ge=0)
    discount_percentage: Optional[Decimal] = Field(default=Decimal('0.00'), ge=0, le=100)
    image_url: str
    is_active: Optional[bool] = True
    is_front_page: Optional[bool] = False

    @field_validator('price', 'discount_percentage', mode='before')
    def convert_to_decimal(cls, v):
        if v is None:
            return Decimal('0.00')
        return Decimal(str(v)) if not isinstance(v, Decimal) else v


### BASE PRODUCT CREATE SCHEMA ###
class ProductBaseCreate(ProductBase):
    model_config = model_conf
    pass


### BASE PRODUCT UPDATE SCHEMA ###
class ProductBaseUpdate(BaseModel):
    model_config = model_conf
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    price: Optional[Decimal] = Field(None, ge=0)
    discount_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_front_page: Optional[bool] = None

    @field_validator('price', 'discount_percentage', mode='before')
    def convert_to_decimal(cls, v):
        if v is None:
            return None
        return Decimal(str(v)) if not isinstance(v, Decimal) else v


### BASE PRODUCT READ SCHEMA ###
class ProductBaseRead(ProductBase):
    model_config = model_conf
    id: int
    final_price: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    favourited_product: List[int] = Field(default_factory=list)
    comments: List[int] = Field(default_factory=list)


### BASE PRODUCT IN DB SCHEMA ###
class ProductBaseInDb(ProductBaseRead):
    model_config = model_conf
    pass
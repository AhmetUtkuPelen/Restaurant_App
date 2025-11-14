from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


class CartItemBase(BaseModel):
    model_config = model_conf
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemCreate(CartItemBase):
    model_config = model_conf
    pass


class CartItemUpdate(BaseModel):
    model_config = model_conf
    quantity: int = Field(..., ge=1)


class CartItemRead(CartItemBase):
    model_config = model_conf
    id: int
    cart_id: int
    created_at: datetime


class CartBase(BaseModel):
    model_config = model_conf
    user_id: int


class CartCreate(BaseModel):
    model_config = model_conf
    pass  # Cart is auto-created for user


class CartRead(CartBase):
    model_config = model_conf
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    cart_items: List[CartItemRead] = Field(default_factory=list)
    total_items: int = 0
    total_price: Decimal = Decimal('0.00')


class CartInDB(CartRead):
    model_config = model_conf
    pass
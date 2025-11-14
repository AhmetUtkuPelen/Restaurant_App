from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from Utils.Enums.Enums import OrderStatus

model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


class OrderItemBase(BaseModel):
    model_config = model_conf
    product_id: int
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., ge=0)
    subtotal: Decimal = Field(..., ge=0)


class OrderItemCreate(BaseModel):
    model_config = model_conf
    product_id: int
    quantity: int = Field(..., ge=1)
    # unit_price and subtotal will be calculated from product


class OrderItemRead(OrderItemBase):
    model_config = model_conf
    id: int
    order_id: int
    created_at: datetime


class OrderBase(BaseModel):
    model_config = model_conf
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None


class OrderCreate(OrderBase):
    model_config = model_conf
    # Order will be created from cart items or explicit items
    items: Optional[List[OrderItemCreate]] = None  # If None, use cart items


class OrderUpdate(BaseModel):
    model_config = model_conf
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None


class OrderRead(OrderBase):
    model_config = model_conf
    id: int
    user_id: int
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    order_items: List[OrderItemRead] = Field(default_factory=list)


class OrderInDB(OrderRead):
    model_config = model_conf
    pass
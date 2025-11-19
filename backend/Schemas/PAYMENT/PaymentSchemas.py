from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, List, Dict
from decimal import Decimal
from datetime import datetime
from Utils.Enums.Enums import PaymentStatus


model_conf = ConfigDict(from_attributes=True, orm_mode=True, json_encoders={Decimal: lambda v: str(v)})


class CardInfo(BaseModel):
    model_config = model_conf
    last_four: Optional[str] = None
    family: Optional[str] = None
    association: Optional[str] = None
    type: Optional[str] = None


class PaymentCreate(BaseModel):
    model_config = model_conf
    # Payment for orders
    order_ids: Optional[List[int]] = Field(default_factory=list)
    # Payment for reservation
    reservation_id: Optional[int] = None
    # Payment details
    amount: Decimal = Field(..., gt=0)
    currency: str = Field(default="TRY")
    installment: int = Field(default=1, ge=1, le=12)
    # User IP (required by Iyzico)
    ip_address: str
    # Optional metadata
    metadata: Optional[Dict] = None


class PaymentUpdate(BaseModel):
    model_config = model_conf
    status: Optional[PaymentStatus] = None
    provider_payment_id: Optional[str] = None
    provider_payment_token: Optional[str] = None
    fraud_status: Optional[int] = None
    card_last_four: Optional[str] = None
    card_family: Optional[str] = None
    card_association: Optional[str] = None
    card_type: Optional[str] = None


class PaymentRead(BaseModel):
    model_config = model_conf
    id: int
    user_id: int
    reservation_id: Optional[int] = None
    amount: Decimal
    currency: str
    status: PaymentStatus
    provider: Optional[str] = None
    provider_payment_id: Optional[str] = None
    conversation_id: Optional[str] = None
    installment: int
    fraud_status: Optional[int] = None
    card_info: Optional[CardInfo] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_ids: List[int] = Field(default_factory=list)


class PaymentInDB(PaymentRead):
    model_config = model_conf
    provider_payment_token: Optional[str] = None
    payment_group: Optional[str] = None
    ip_address: Optional[str] = None
    basket_id: Optional[str] = None
    metadata: Optional[Dict] = None

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime, timezone
from Utils.Enums.Enums import ReservationStatus

model_conf = ConfigDict(from_attributes=True, orm_mode=True)


class ReservationBase(BaseModel):
    model_config = model_conf
    table_id: int
    reservation_time: datetime
    number_of_guests: int = Field(..., ge=1, le=20)
    special_requests: Optional[str] = Field(None, max_length=500)

    @field_validator('reservation_time')
    def validate_future_time(cls, v):
        # Make both datetimes timezone-aware for comparison
        now = datetime.now(timezone.utc)
        reservation_time = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        
        if reservation_time < now:
            raise ValueError('Reservation time must be in the future')
        return v


class ReservationCreate(ReservationBase):
    model_config = model_conf
    pass


class ReservationUpdate(BaseModel):
    model_config = model_conf
    table_id: Optional[int] = None
    reservation_time: Optional[datetime] = None
    number_of_guests: Optional[int] = Field(None, ge=1, le=20)
    status: Optional[ReservationStatus] = None
    special_requests: Optional[str] = Field(None, max_length=500)


class ReservationRead(ReservationBase):
    model_config = model_conf
    id: int
    user_id: int
    status: ReservationStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    payments: List[int] = Field(default_factory=list)


class ReservationInDB(ReservationRead):
    model_config = model_conf
    deleted_at: Optional[datetime] = None
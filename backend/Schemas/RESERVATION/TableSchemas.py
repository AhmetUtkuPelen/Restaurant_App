from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from Utils.Enums.Enums import TableLocation

model_conf = ConfigDict(from_attributes=True, orm_mode=True)


class TableBase(BaseModel):
    model_config = model_conf
    table_number: str = Field(..., min_length=1, max_length=10)
    capacity: int = Field(..., ge=1, le=20)
    location: TableLocation = TableLocation.MAIN_DINING_ROOM
    is_available: bool = True


class TableCreate(TableBase):
    model_config = model_conf
    pass


class TableUpdate(BaseModel):
    model_config = model_conf
    table_number: Optional[str] = Field(None, min_length=1, max_length=10)
    capacity: Optional[int] = Field(None, ge=1, le=20)
    location: Optional[TableLocation] = None
    is_available: Optional[bool] = None


class TableRead(TableBase):
    model_config = model_conf
    id: int


class TableInDB(TableRead):
    model_config = model_conf
    pass
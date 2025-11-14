from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

model_conf = ConfigDict(from_attributes=True, orm_mode=True)


class CommentBase(BaseModel):
    model_config = model_conf
    product_id: int
    content: str = Field(..., min_length=1, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)


class CommentCreate(BaseModel):
    model_config = model_conf
    product_id: int
    content: str = Field(..., min_length=1, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)


class CommentUpdate(BaseModel):
    model_config = model_conf
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)


class CommentRead(CommentBase):
    model_config = model_conf
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool


class CommentInDB(CommentRead):
    model_config = model_conf
    deleted_at: Optional[datetime] = None
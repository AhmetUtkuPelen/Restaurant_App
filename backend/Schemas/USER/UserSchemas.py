from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field
from typing import Optional, List
from datetime import datetime
import re

from Utils.Enums.Enums import UserRole as Role
from Utils.Auth.HashPassword import is_password_strong

# Pydantic v2 config
model_conf = ConfigDict(from_attributes=True, orm_mode=True)

# ---------------------------#
# Password Validation Helper #
# -------------------------- #
def validate_password_strength(password: str) -> str:

    strength = is_password_strong(password)
    
    if not strength["valid"]:
        errors = []
        if not strength["length"]:
            errors.append("at least 8 characters")
        if not strength["uppercase"]:
            errors.append("one uppercase letter")
        if not strength["lowercase"]:
            errors.append("one lowercase letter")
        if not strength["digit"]:
            errors.append("one digit")
        if not strength["special"]:
            errors.append("one special character")
        
        raise ValueError(f"Password must contain: {', '.join(errors)}")
    
    return password

# ------------------- #
    # Token Schemas #
# ------------------- #


class Token(BaseModel):
    model_config = model_conf
    access_token: str
    token_type: str = "bearer"



class TokenData(BaseModel):
    model_config = model_conf
    username: Optional[str] = None

# ------------------- #
 # Base User Schemas #
# ------------------- #
class UserBase(BaseModel):
    model_config = model_conf
    email: EmailStr
    username: str
    image_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    role: Optional[Role] = Role.USER

    @field_validator("username")
    def username_alphanumeric(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("username cannot be empty")
        v2 = v.strip()
        if not re.match(r"^[A-Za-z0-9._-]{3,20}$", v2):
            raise ValueError("Username must be 3-20 chars and contain only letters, digits, ., _, -")
        return v2
    
    @field_validator("email", mode="before")
    def email_lower(cls, v: str) -> str:
        return v.lower() if isinstance(v, str) else v

    @field_validator('email')
    def email_format(cls, v):
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format!')
        return v
    
    @field_validator('phone')
    def phone_format(cls, v):
        if not v:
            return None
        pattern = r'^(\+90\d{10}|\d{10})$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number format! Use 10 digits or +90XXXXXXXXXX')
        return v
    
    @field_validator('address')
    def address_format(cls, v):
        if not v:
            return None
        if len(v) < 5:
            raise ValueError('Address must be at least 5 characters long!')
        return v

# ---------------------------- #
# Schemas for Specific Actions #
# ---------------------------- #

class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    model_config = model_conf
    username: str
    password: str

class UserRegister(UserBase):
    """
    Schema for user registration.
    """
    model_config = model_conf
    username: str
    email: EmailStr
    password: str
    image_url : Optional[str] = None

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserUpdate(BaseModel):
    """
    Schema for User to update user information of himself / herself .
    """
    model_config = model_conf
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    image_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class AdminCreateUser(BaseModel):
    """
    Schema for admin to create a new user.
    """
    model_config = model_conf
    username: str
    email: EmailStr
    password: str
    role: Optional[Role] = Role.USER
    image_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = True
    
    @field_validator("username")
    def username_alphanumeric(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("username cannot be empty")
        v2 = v.strip()
        if not re.match(r"^[A-Za-z0-9._-]{3,20}$", v2):
            raise ValueError("Username must be 3-20 chars and contain only letters, digits, ., _, -")
        return v2

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class AdminUpdateUser(BaseModel):
    """
    Schema for admin to update user information.
    """
    model_config = model_conf
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
    image_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class AdminHardDeleteUser(BaseModel):
    """
    Schema for admin to delete a user.
    """
    model_config = model_conf
    id: int

class AdminSoftDeleteUser(BaseModel):
    """
    Schema for admin to soft delete a user.
    """
    model_config = model_conf
    id: int
    is_active: bool = False

# -------------------------------------- #
# Schemas for Database and API Responses #
# -------------------------------------- #
class UserInDbBase(UserBase):
    """
    Base schema for user data as it is in the database.
    """
    model_config = model_conf
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    image_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    role: Role

    favourite_products: List[int] = Field(default_factory=list)
    orders: List[int] = Field(default_factory=list)
    comments: List[int] = Field(default_factory=list)
    cart: Optional[dict] = None
    reservations: List[int] = Field(default_factory=list)
    payments: List[int] = Field(default_factory=list)

class User(UserInDbBase):
    """
    Schema for representing a user in API responses.
    """
    model_config = model_conf
    pass

class UserInDb(UserInDbBase):
    """
    Schema for user data including the hashed password.
    """
    model_config = model_conf
    hashed_password: str


### User Profile Schemas
class UserProfileRead(BaseModel):
    """Read-only profile view for users (what they see when fetching their profile)."""
    model_config = model_conf
    id: int
    username: str
    email: EmailStr
    image_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    favourite_products: List[int] = Field(default_factory=list)
    orders: List[int] = Field(default_factory=list)
    comments: List[int] = Field(default_factory=list)
    cart: Optional[dict] = None
    reservations: List[int] = Field(default_factory=list)
    payments: List[int] = Field(default_factory=list)


class UserProfileUpdate(BaseModel):
    """Payload for updating the profile. Password is optional and will be hashed."""
    model_config = model_conf
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    image_url: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v
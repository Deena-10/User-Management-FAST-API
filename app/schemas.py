from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models import UserRole

# User Registration Schema
class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, description="Name must be at least 3 characters")
    email: EmailStr
    phone: str = Field(..., description="Phone number")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    address: Optional[str] = Field(None, max_length=150)
    state: str = Field(..., description="State is required")
    city: str = Field(..., description="City is required")
    country: str = Field(..., description="Country is required")
    pincode: str = Field(..., description="Pincode is required")
    profile_image: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only alphabets')
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('Phone must contain only digits')
        if not (10 <= len(v) <= 15):
            raise ValueError('Phone must be between 10 and 15 digits')
        return v

    @validator('pincode')
    def validate_pincode(cls, v):
        if not v.isdigit():
            raise ValueError('Pincode must contain only digits')
        if not (4 <= len(v) <= 10):
            raise ValueError('Pincode must be between 4 and 10 digits')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        return v

# User Login Schema
class UserLogin(BaseModel):
    email_or_phone: str = Field(..., description="Email or phone number")
    password: str

# Token Response Schema
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Refresh Token Schema
class RefreshToken(BaseModel):
    refresh_token: str

# User Response Schema (without sensitive data)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    profile_image: Optional[str] = None
    address: Optional[str] = None
    state: str
    city: str
    country: str
    pincode: str
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# User Update Schema
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = Field(None, max_length=150)
    state: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None

    @validator('name', allow_reuse=True)
    def validate_name(cls, v):
        if v and not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only alphabets')
        return v

    @validator('phone', allow_reuse=True)
    def validate_phone(cls, v):
        if v:
            if not v.isdigit():
                raise ValueError('Phone must contain only digits')
            if not (10 <= len(v) <= 15):
                raise ValueError('Phone must be between 10 and 15 digits')
        return v

    @validator('pincode', allow_reuse=True)
    def validate_pincode(cls, v):
        if v:
            if not v.isdigit():
                raise ValueError('Pincode must contain only digits')
            if not (4 <= len(v) <= 10):
                raise ValueError('Pincode must be between 4 and 10 digits')
        return v

# Pagination Schema
class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: list[UserResponse]


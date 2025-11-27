from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Hashed password
    profile_image = Column(String(255), nullable=True)
    address = Column(String(150), nullable=True)
    state = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    pincode = Column(String(10), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


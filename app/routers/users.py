from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from math import ceil
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserUpdate, PaginatedResponse
from app.auth import get_current_user, get_current_admin_user
import os
import aiofiles

router = APIRouter()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

async def save_uploaded_file(file: UploadFile, user_id: int) -> str:
    """Save uploaded file and return the file path"""
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG and PNG files are allowed"
        )
    
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 2MB"
        )
    
    filename = f"user_{user_id}_{file.filename}"
    filepath = os.path.join("uploads", filename)
    
    async with aiofiles.open(filepath, 'wb') as f:
        await f.write(content)
    
    return f"/uploads/{filename}"

@router.get("", response_model=PaginatedResponse)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name, email, state, or city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    city: Optional[str] = Query(None, description="Filter by city"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all users with pagination and filtering (Admin only)"""
    query = db.query(User)
    
    # Apply search filter
    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.state.ilike(f"%{search}%"),
                User.city.ilike(f"%{search}%")
            )
        )
    
    # Apply state filter
    if state:
        query = query.filter(User.state.ilike(f"%{state}%"))
    
    # Apply city filter
    if city:
        query = query.filter(User.city.ilike(f"%{city}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    skip = (page - 1) * page_size
    users = query.offset(skip).limit(page_size).all()
    
    total_pages = ceil(total / page_size) if total > 0 else 0
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": users
    }

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single user by ID"""
    # Users can only view their own profile unless they are admin
    if current_user.role.value != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: Request,
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    pincode: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a user (Users can update their own profile, Admins can update any)
    Supports both form data (for file uploads) and JSON (for API calls without files)
    """
    
    # Users can only update their own profile unless they are admin
    if current_user.role.value != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check content type - if JSON, parse from body, otherwise use form data
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        # Handle JSON request
        body = await request.json()
        update_data = {k: v for k, v in body.items() if k != "profile_image" and v is not None}
    else:
        # Handle form data
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if email is not None:
            update_data["email"] = email
        if phone is not None:
            update_data["phone"] = phone
        if address is not None:
            update_data["address"] = address
        if state is not None:
            update_data["state"] = state
        if city is not None:
            update_data["city"] = city
        if country is not None:
            update_data["country"] = country
        if pincode is not None:
            update_data["pincode"] = pincode
    
    # Validate update data using Pydantic schema
    if update_data:
        user_update = UserUpdate(**update_data)
        update_data = user_update.dict(exclude_unset=True)
    
    # Check email uniqueness if updating email
    if "email" in update_data and update_data["email"] != user.email:
        existing_user = db.query(User).filter(User.email == update_data["email"]).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check phone uniqueness if updating phone
    if "phone" in update_data and update_data["phone"] != user.phone:
        existing_phone = db.query(User).filter(User.phone == update_data["phone"]).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
    
    # Update user fields
    for field, value in update_data.items():
        setattr(user, field, value)
    
    # Handle profile image upload
    if profile_image:
        try:
            # Delete old image if exists
            if user.profile_image:
                old_path = user.profile_image.lstrip("/")
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            image_path = await save_uploaded_file(profile_image, user.id)
            user.profile_image = image_path
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error uploading image: {str(e)}"
            )
    
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete profile image if exists
    if user.profile_image:
        image_path = user.profile_image.lstrip("/")
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.delete(user)
    db.commit()
    
    return None


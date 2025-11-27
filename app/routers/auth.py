from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserRegister, UserLogin, TokenResponse, RefreshToken, UserResponse
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user
)
from typing import Optional, Union
import os
import aiofiles

router = APIRouter()

# Allowed image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

async def save_uploaded_file(file: UploadFile, user_id: int) -> str:
    """Save uploaded file and return the file path"""
    # Get file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG and PNG files are allowed"
        )
    
    # Read file content
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 2MB"
        )
    
    # Generate filename
    filename = f"user_{user_id}_{file.filename}"
    filepath = os.path.join("uploads", filename)
    
    # Save file
    async with aiofiles.open(filepath, 'wb') as f:
        await f.write(content)
    
    return f"/uploads/{filename}"

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    pincode: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Register a new user - Supports both JSON and multipart/form-data"""
    
    # Check content type - if JSON, parse from body, otherwise use form data
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        # Handle JSON request (when no file upload)
        try:
            body = await request.json()
            user_data = UserRegister(**body)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid JSON data: {str(e)}"
            )
    else:
        # Handle form data (multipart/form-data)
        # Check if required fields are provided
        if not all([name, email, phone, password, state, city, country, pincode]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Missing required fields: name, email, phone, password, state, city, country, pincode"
            )
        
        # Create UserRegister object from form data
        try:
            user_data = UserRegister(
                name=name,
                email=email,
                phone=phone,
                password=password,
                address=address,
                state=state,
                city=city,
                country=country,
                pincode=pincode
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Validation error: {str(e)}"
            )
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if phone already exists
    existing_phone = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_password,
        address=user_data.address,
        state=user_data.state,
        city=user_data.city,
        country=user_data.country,
        pincode=user_data.pincode,
        role=UserRole.USER
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Handle profile image upload
    if profile_image:
        try:
            image_path = await save_uploaded_file(profile_image, db_user.id)
            db_user.profile_image = image_path
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            # If image upload fails, user is still created
            pass
    
    return db_user

@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    """Login user with email/phone and password - Supports both OAuth2 form and JSON
    
    For OAuth2 (Swagger UI): Use 'username' field with email or phone
    For JSON API: Use 'email_or_phone' field
    """
    
    email_or_phone = None
    password = None
    
    # Check content type to determine which format to use
    content_type = request.headers.get("content-type", "")
    
    # Try OAuth2 form data first (for Swagger UI OAuth2 flow)
    if "application/x-www-form-urlencoded" in content_type:
        try:
            form_data = await request.form()
            # OAuth2 uses 'username' field - can contain email or phone
            email_or_phone = form_data.get("username")
            password = form_data.get("password")
        except Exception:
            pass
    
    # If not OAuth2 form, try JSON
    if not email_or_phone:
        try:
            body = await request.json()
            email_or_phone = body.get("email_or_phone")
            password = body.get("password")
        except Exception:
            pass
    
    # Validate we have credentials
    if not email_or_phone or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing credentials. For OAuth2: use 'username' field with email/phone. For JSON: use 'email_or_phone' field."
        )
    
    # Find user by email or phone
    user = db.query(User).filter(
        (User.email == email_or_phone) |
        (User.phone == email_or_phone)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/phone or password"
        )
    
    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/phone or password"
        )
    
    # Create tokens (sub must be string for python-jose)
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    # Verify refresh token
    payload = verify_token(refresh_data.refresh_token, is_refresh=True)
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    # Convert string back to int (python-jose requires sub to be string)
    user_id = int(user_id_str)
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Create new access token (sub must be string for python-jose)
    access_token = create_access_token(data={"sub": str(user.id)})

    # Optionally create new refresh token (refresh token rotation)
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information"""
    return current_user


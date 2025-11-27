from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users
import os

# Create necessary directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management System API",
    description="A comprehensive User Management System with JWT authentication, CRUD operations, and Admin Panel",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

# Admin panel routes
@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users_page(request: Request):
    return templates.TemplateResponse("admin_users.html", {"request": request})

@app.get("/admin/users/{user_id}", response_class=HTMLResponse)
async def admin_user_detail(request: Request, user_id: int):
    return templates.TemplateResponse("admin_user_detail.html", {"request": request, "user_id": user_id})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "User Management System API is running"}


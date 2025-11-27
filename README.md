# User Management System

A comprehensive User Management System built with FastAPI, featuring JWT authentication, CRUD operations, and an Admin Panel.

## Features

- User Registration with validation
- JWT Access & Refresh Token Authentication
- Full CRUD Operations for Users
- Admin Panel (Web-based Dashboard)
- Image Upload (local folder)
- REST API Integration
- Input Validation & Error Handling
- Role-based Access Control (Admin/User)
- Pagination for list API
- Search & Filter functionality
- Swagger/OpenAPI Documentation

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **JWT** - JSON Web Tokens for authentication
- **OAuth2PasswordBearer** - OAuth2 password flow
- **Bcrypt** - Password hashing
- **Jinja2** - Template engine for admin panel
- **SQLite** - Database (can be changed to PostgreSQL)

## Project Structure

```
User management/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       └── users.py         # User CRUD routes
├── templates/               # Jinja2 templates
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_users.html
│   └── admin_user_detail.html
├── static/                 # Static files
├── uploads/                # User uploaded images
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or navigate to the project directory**

```bash
cd "User management"
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Create necessary directories**

```bash
mkdir uploads
mkdir static
```

## Database Setup

The project uses SQLite by default. The database file (`user_management.db`) will be created automatically when you run the application.

### To use PostgreSQL instead:

1. Install PostgreSQL and create a database
2. Update `app/database.py`:
```python
DATABASE_URL = "postgresql://username:password@localhost/dbname"
```
3. Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

## Running the Application

1. **Start the FastAPI server**

```bash
uvicorn app.main:app --reload
```

2. **Access the application**

- **API Documentation (Swagger):** http://localhost:8000/docs
- **ReDoc Documentation:** http://localhost:8000/redoc
- **Admin Login:** http://localhost:8000/admin/login
- **Admin Dashboard:** http://localhost:8000/
- **Admin Users Panel:** http://localhost:8000/admin/users

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Users (Protected)

- `GET /api/users` - List all users (Admin only, with pagination & filtering)
- `GET /api/users/{id}` - Get single user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user (Admin only)

## Usage Examples

### Register a User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "password": "password123",
    "state": "California",
    "city": "Los Angeles",
    "country": "USA",
    "pincode": "90001"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_phone": "john@example.com",
    "password": "password123"
  }'
```

### Get Users (with authentication)

```bash
curl -X GET "http://localhost:8000/api/users?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Validation Rules

### User Registration

- **name**: Minimum 3 characters, alphabets only
- **email**: Valid email format, unique
- **phone**: Numeric, 10-15 digits, unique
- **address**: Optional, maximum 150 characters
- **state**: Required
- **city**: Required
- **country**: Required
- **pincode**: Numeric, 4-10 digits
- **profile_image**: JPG/PNG only, maximum 2MB
- **password**: Minimum 6 characters, at least 1 number

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Access token expiration (1 hour)
- Refresh token expiration (7 days)
- Role-based access control
- Input validation with Pydantic
- CORS enabled
- No sensitive data in responses

## Admin Panel

The admin panel provides a web-based interface for managing users:

1. **Login** - Access at `/admin/login`
2. **Dashboard** - View statistics at `/`
3. **Users Management** - Full CRUD operations at `/admin/users`
4. **User Details** - View individual user details

### Creating an Admin User

To create an admin user, you can either:

1. **Manually update the database:**
   - Register a user normally
   - Update the `role` field in the database to `admin`

2. **Use Python script:**
```python
from app.database import SessionLocal
from app.models import User, UserRole
from app.auth import get_password_hash

db = SessionLocal()
admin = User(
    name="Admin User",
    email="admin@example.com",
    phone="9999999999",
    password=get_password_hash("admin123"),
    state="State",
    city="City",
    country="Country",
    pincode="12345",
    role=UserRole.ADMIN
)
db.add(admin)
db.commit()
```

## Environment Variables (Optional)

For production, set these environment variables:

```bash
DATABASE_URL=sqlite:///./user_management.db
SECRET_KEY=your-secret-key-here
REFRESH_SECRET_KEY=your-refresh-secret-key-here
```

Update `app/auth.py` to use environment variables:

```python
import os
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your-refresh-secret-key-change-this-in-production")
```

## Database Schema

### User Model

```
- id: Integer (Primary Key)
- name: String(100)
- email: String(100, Unique)
- phone: String(15, Unique)
- password: String(255) [Hashed]
- profile_image: String(255) [Optional]
- address: String(150) [Optional]
- state: String(50)
- city: String(50)
- country: String(50)
- pincode: String(10)
- role: Enum(user/admin)
- created_at: DateTime
- updated_at: DateTime
```

## ER Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ name            │
│ email (UNIQUE)  │
│ phone (UNIQUE)  │
│ password        │
│ profile_image   │
│ address         │
│ state           │
│ city            │
│ country         │
│ pincode         │
│ role            │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## Testing

### Quick Testing

1. **Automated Test Script** (Recommended)
   ```bash
   python test_api.py
   ```
   This will automatically test all endpoints and show results.

2. **Swagger UI** - Interactive API documentation at `/docs`
   - Open http://localhost:8000/docs
   - Click "Try it out" on any endpoint
   - Fill in the form and execute

3. **Postman** - Import the OpenAPI schema
   ```bash
   python export_openapi.py
   ```
   Then import `openapi.json` into Postman

4. **cURL** - Command-line tool (examples in TESTING_GUIDE.md)

### Detailed Testing Guide

See **TESTING_GUIDE.md** for comprehensive testing instructions including:
- Step-by-step endpoint testing
- Validation testing
- Admin panel testing
- Edge case testing
- Troubleshooting

## Troubleshooting

### Common Issues

1. **Module not found error**
   - Make sure you've activated the virtual environment
   - Run `pip install -r requirements.txt` again

2. **Database errors**
   - Delete `user_management.db` and restart the server
   - Check database permissions

3. **Image upload fails**
   - Ensure `uploads/` directory exists
   - Check file permissions

4. **Authentication errors**
   - Verify token is included in Authorization header
   - Check token expiration
   - Use refresh token to get new access token


 

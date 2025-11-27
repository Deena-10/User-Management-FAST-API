# Quick Start Guide - User Management System

## Quick Setup & Run Commands

### Step 1: Install Dependencies
```powershell
python.exe -m pip install -r requirements.txt
```

### Step 2: Create Admin User (Optional - for admin panel)
```powershell
python.exe create_admin.py
```

### Step 3: Run the Server
```powershell
python.exe -m uvicorn app.main:app --reload
```

The server will start at: **http://localhost:8000**

---

## Important URLs

Once the server is running, access:

- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **ReDoc Documentation:** http://localhost:8000/redoc
- **Admin Login Page:** http://localhost:8000/admin/login
- **Admin Dashboard:** http://localhost:8000/
- **Admin Users Panel:** http://localhost:8000/admin/users
- **Health Check:** http://localhost:8000/health

---

## Testing the Project

### Method 1: Swagger UI (Easiest - Recommended)
1. Open browser: http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in the form and click "Execute"
4. See the response immediately

### Method 2: Automated Test Script
```powershell
python.exe test_api.py
```

### Method 3: Manual Testing with cURL

**1. Register a User:**
```powershell
curl -X POST "http://localhost:8000/api/auth/register" -H "Content-Type: application/json" -d "{\"name\": \"Test User\", \"email\": \"test@example.com\", \"phone\": \"1234567890\", \"password\": \"test123\", \"state\": \"California\", \"city\": \"San Francisco\", \"country\": \"USA\", \"pincode\": \"94102\"}"
```

**2. Login:**
```powershell
curl -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/json" -d "{\"email_or_phone\": \"test@example.com\", \"password\": \"test123\"}"
```

**3. Get Current User (replace YOUR_TOKEN with token from login):**
```powershell
curl -X GET "http://localhost:8000/api/auth/me" -H "Authorization: Bearer YOUR_TOKEN"
```

**4. Get All Users (Admin only):**
```powershell
curl -X GET "http://localhost:8000/api/users?page=1&page_size=10" -H "Authorization: Bearer ADMIN_TOKEN"
```

---

## Admin Panel Access

**Default Admin Credentials (if created with create_admin.py):**
- Email: `admin@example.com`
- Password: `admin123`

**To create admin user:**
```powershell
python.exe create_admin.py
```

---

## Common Commands

### Start Server (Development Mode)
```powershell
python.exe -m uvicorn app.main:app --reload
```

### Start Server (Production Mode)
```powershell
python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Check Installed Packages
```powershell
python.exe -m pip list
```

### Update Packages
```powershell
python.exe -m pip install --upgrade -r requirements.txt
```

---

## Troubleshooting

### Issue: "uvicorn is not recognized"
**Solution:** Use `python.exe -m uvicorn` instead of just `uvicorn`

### Issue: "Module not found"
**Solution:** Run `python.exe -m pip install -r requirements.txt`

### Issue: "Database locked"
**Solution:** Close other connections and restart the server

### Issue: "Port already in use"
**Solution:** Change port: `python.exe -m uvicorn app.main:app --reload --port 8001`

---

## More Information

- **Full Testing Guide:** See `TESTING_GUIDE.md`
- **Project README:** See `README.md`
- **API Documentation:** http://localhost:8000/docs (when server is running)

---

## Quick Test Checklist

- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Can register a new user via Swagger UI
- [ ] Can login and get access token
- [ ] Can access admin panel at /admin/login
- [ ] Can view users list (as admin)
- [ ] Health check returns {"status": "healthy"}

---

**Happy Testing!**

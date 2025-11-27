# Testing Guide - User Management System

This guide provides step-by-step instructions to test all features of the User Management System.

## Prerequisites

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The server will run on `http://localhost:8000`

3. **Create Admin User** (Optional - for admin panel testing)
   ```bash
   python create_admin.py
   ```

## Testing Methods

### Method 1: Using Swagger UI (Easiest)

1. Open browser and go to: **http://localhost:8000/docs**
2. You'll see all API endpoints with interactive forms
3. Click "Try it out" on any endpoint
4. Fill in the required fields
5. Click "Execute" to test

**Advantages:**
- No need to write code
- Automatic authentication handling
- See request/response examples
- Test all endpoints easily

### Method 2: Using Python Test Script

Run the automated test script:
```bash
python test_api.py
```

This will test all endpoints automatically.

### Method 3: Using cURL (Command Line)

See examples below for each endpoint.

### Method 4: Using Postman

1. Export OpenAPI schema:
   ```bash
   python export_openapi.py
   ```
2. Import `openapi.json` into Postman
3. All endpoints will be available with proper structure

## Step-by-Step Testing

### 1. Test User Registration

**Using Swagger UI:**
- Go to `/docs`
- Find `POST /api/auth/register`
- Click "Try it out"
- Fill in the form with test data
- Execute

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "password": "test123",
    "state": "California",
    "city": "San Francisco",
    "country": "USA",
    "pincode": "94102"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "name": "Test User",
  "email": "test@example.com",
  "phone": "1234567890",
  ...
}
```

### 2. Test User Login

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_phone": "test@example.com",
    "password": "test123"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

**Save the access_token for next steps!**

### 3. Test Get Current User

**Using cURL:**
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Replace `YOUR_ACCESS_TOKEN` with the token from login.

### 4. Test Refresh Token

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

### 5. Test Get All Users (Admin Only)

**Using cURL:**
```bash
curl -X GET "http://localhost:8000/api/users?page=1&page_size=10" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**With Search/Filter:**
```bash
curl -X GET "http://localhost:8000/api/users?page=1&page_size=10&search=test&state=California" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### 6. Test Get Single User

**Using cURL:**
```bash
curl -X GET "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Test Update User

**Using cURL (JSON):**
```bash
curl -X PUT "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "city": "New York"
  }'
```

**Using cURL (Form Data with Image):**
```bash
curl -X PUT "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "name=Updated Name" \
  -F "city=New York" \
  -F "profile_image=@/path/to/image.jpg"
```

### 8. Test Delete User (Admin Only)

**Using cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

### 9. Test Image Upload

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "name=User With Image" \
  -F "email=image@example.com" \
  -F "phone=9876543210" \
  -F "password=test123" \
  -F "state=Texas" \
  -F "city=Houston" \
  -F "country=USA" \
  -F "pincode=77001" \
  -F "profile_image=@/path/to/image.jpg"
```

## Testing Admin Panel

### 1. Access Admin Login
- Open browser: **http://localhost:8000/admin/login**
- Login with admin credentials:
  - Email: `admin@example.com`
  - Password: `admin123`

### 2. Test Admin Dashboard
- After login, you'll see the dashboard at **http://localhost:8000/**
- Check statistics display correctly

### 3. Test Users Management
- Go to **http://localhost:8000/admin/users**
- Test features:
  - View all users in table
  - Search users (try searching by name, email, state, city)
  - Filter by state and city
  - Pagination (click page numbers)
  - View user details (click "View" button)
  - Edit user (click "Edit" button, modify, save)
  - Delete user (click "Delete" button, confirm)

### 4. Test User Details Page
- Click "View" on any user
- Verify all user information displays correctly
- Test edit and delete from detail page

## Validation Testing

### Test Registration Validations

1. **Name Validation:**
   ```json
   {"name": "Ab"}  // Should fail (min 3 chars)
   {"name": "123"} // Should fail (alphabets only)
   ```

2. **Email Validation:**
   ```json
   {"email": "invalid-email"} // Should fail
   {"email": "existing@example.com"} // Should fail if exists
   ```

3. **Phone Validation:**
   ```json
   {"phone": "123"} // Should fail (10-15 digits)
   {"phone": "abc123"} // Should fail (numeric only)
   ```

4. **Password Validation:**
   ```json
   {"password": "123"} // Should fail (min 6 chars)
   {"password": "password"} // Should fail (needs number)
   ```

5. **Pincode Validation:**
   ```json
   {"pincode": "12"} // Should fail (4-10 digits)
   ```

### Test Authentication

1. **Invalid Credentials:**
   ```bash
   curl -X POST "http://localhost:8000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email_or_phone": "wrong@example.com", "password": "wrong"}'
   ```
   Should return 401 Unauthorized

2. **Missing Token:**
   ```bash
   curl -X GET "http://localhost:8000/api/users"
   ```
   Should return 401 Unauthorized

3. **Invalid Token:**
   ```bash
   curl -X GET "http://localhost:8000/api/users" \
     -H "Authorization: Bearer invalid_token"
   ```
   Should return 401 Unauthorized

4. **Non-Admin Access:**
   ```bash
   # Login as regular user, then try to access admin endpoints
   curl -X GET "http://localhost:8000/api/users" \
     -H "Authorization: Bearer REGULAR_USER_TOKEN"
   ```
   Should return 403 Forbidden

## Testing Edge Cases

1. **Empty Search Results:**
   - Search for non-existent user
   - Verify empty state displays correctly

2. **Pagination:**
   - Create multiple users
   - Test pagination with different page sizes
   - Test edge cases (first page, last page)

3. **Image Upload:**
   - Test with valid image (JPG, PNG)
   - Test with invalid format (GIF, PDF)
   - Test with large file (>2MB)
   - Verify image displays correctly after upload

4. **Concurrent Updates:**
   - Try updating same user from different sessions
   - Verify data consistency

## Expected Test Results

### Successful Tests Should Show:
- 200 OK for GET requests
- 201 Created for POST requests
- 204 No Content for DELETE requests
- Proper JSON responses
- Correct data in database
- Images saved in `/uploads/` folder

### Failed Tests Should Show:
- 400 Bad Request for validation errors
- 401 Unauthorized for authentication errors
- 403 Forbidden for permission errors
- 404 Not Found for missing resources
- Clear error messages

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated and dependencies are installed

### Issue: "Database locked"
**Solution:** Close other database connections, restart server

### Issue: "Image upload fails"
**Solution:** Check `uploads/` folder exists and has write permissions

### Issue: "401 Unauthorized"
**Solution:** 
- Check token is valid and not expired
- Verify token is in Authorization header: `Bearer TOKEN`
- Try refreshing token

### Issue: "403 Forbidden"
**Solution:** 
- Verify user has admin role
- Check user is trying to access their own resource (for non-admins)

## Test Checklist

- [ ] User registration with valid data
- [ ] User registration with invalid data (validation)
- [ ] User login with email
- [ ] User login with phone
- [ ] User login with wrong credentials
- [ ] Get current user info
- [ ] Refresh access token
- [ ] Get all users (admin)
- [ ] Get all users (non-admin - should fail)
- [ ] Search users
- [ ] Filter users by state/city
- [ ] Pagination
- [ ] Get single user
- [ ] Update user (own profile)
- [ ] Update user (admin updating others)
- [ ] Update user (non-admin updating others - should fail)
- [ ] Delete user (admin)
- [ ] Delete user (non-admin - should fail)
- [ ] Image upload (valid)
- [ ] Image upload (invalid format)
- [ ] Image upload (too large)
- [ ] Admin panel login
- [ ] Admin panel dashboard
- [ ] Admin panel user management
- [ ] Admin panel search/filter
- [ ] Admin panel edit user
- [ ] Admin panel delete user

## Quick Test Command

Run all automated tests:
```bash
python test_api.py
```

This will test all endpoints and print results.


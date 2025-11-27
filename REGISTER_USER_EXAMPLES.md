# How to Register a New User

## Method 1: Using Swagger UI (Easiest - Recommended)

1. **Open Swagger UI:**
   - Go to: http://127.0.0.1:8000/docs

2. **Find the Register Endpoint:**
   - Look for `POST /api/auth/register`
   - Click on it to expand

3. **Click "Try it out"**

4. **Fill in the form:**
   ```json
   {
     "name": "John Doe",
     "email": "john@example.com",
     "phone": "1234567890",
     "password": "password123",
     "state": "California",
     "city": "Los Angeles",
     "country": "USA",
     "pincode": "90001",
     "address": "123 Main Street"  // Optional
   }
   ```

5. **Click "Execute"**

6. **See the response** - You'll get the created user data with ID

---

## Method 2: Using cURL (Command Line)

### Basic Registration (JSON only):
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"John Doe\",
    \"email\": \"john@example.com\",
    \"phone\": \"1234567890\",
    \"password\": \"password123\",
    \"state\": \"California\",
    \"city\": \"Los Angeles\",
    \"country\": \"USA\",
    \"pincode\": \"90001\"
  }"
```

### Registration with Profile Image:
```bash
curl -X POST "http://127.0.0.1:8000/api/auth/register" \
  -F "name=John Doe" \
  -F "email=john@example.com" \
  -F "phone=1234567890" \
  -F "password=password123" \
  -F "state=California" \
  -F "city=Los Angeles" \
  -F "country=USA" \
  -F "pincode=90001" \
  -F "address=123 Main Street" \
  -F "profile_image=@/path/to/image.jpg"
```

---

## Method 3: Using Python (requests library)

```python
import requests

url = "http://127.0.0.1:8000/api/auth/register"

# Registration data
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "password": "password123",
    "state": "California",
    "city": "Los Angeles",
    "country": "USA",
    "pincode": "90001",
    "address": "123 Main Street"  # Optional
}

# Register user
response = requests.post(url, json=user_data)

if response.status_code == 201:
    user = response.json()
    print(f"User created successfully!")
    print(f"User ID: {user['id']}")
    print(f"Email: {user['email']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### Registration with Profile Image (Python):
```python
import requests

url = "http://127.0.0.1:8000/api/auth/register"

user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "password": "password123",
    "state": "California",
    "city": "Los Angeles",
    "country": "USA",
    "pincode": "90001"
}

# Open image file
with open("profile.jpg", "rb") as image_file:
    files = {"profile_image": image_file}
    response = requests.post(url, data=user_data, files=files)

if response.status_code == 201:
    print("User created with image!")
    print(response.json())
```

---

## Required Fields

| Field | Type | Validation | Example |
|-------|------|------------|---------|
| **name** | string | Min 3 chars, alphabets only | "John Doe" |
| **email** | string | Valid email format, unique | "john@example.com" |
| **phone** | string | 10-15 digits, unique | "1234567890" |
| **password** | string | Min 6 chars, must contain at least 1 number | "password123" |
| **state** | string | Required | "California" |
| **city** | string | Required | "Los Angeles" |
| **country** | string | Required | "USA" |
| **pincode** | string | 4-10 digits | "90001" |

## Optional Fields

| Field | Type | Validation | Example |
|-------|------|------------|---------|
| **address** | string | Max 150 characters | "123 Main Street" |
| **profile_image** | file | JPG/PNG only, max 2MB | image.jpg |

---

## Validation Rules

### Name:
- Minimum 3 characters
- Only alphabets and spaces allowed
- Example: "John Doe" (valid), "John123" (invalid)

### Email:
- Must be valid email format
- Must be unique (not already registered)
- Example: "john@example.com" (valid), "invalid-email" (invalid)

### Phone:
- Must be numeric only
- Must be between 10-15 digits
- Must be unique (not already registered)
- Example: "1234567890" (valid), "123-456-7890" (invalid)

### Password:
- Minimum 6 characters
- Must contain at least one number
- Example: "password123" (valid), "password" (invalid)

### Pincode:
- Must be numeric only
- Must be between 4-10 digits
- Example: "90001" (valid), "123" (invalid)

### Profile Image:
- Allowed formats: JPG, JPEG, PNG
- Maximum size: 2MB
- Example: "profile.jpg" (valid), "profile.pdf" (invalid)

---

## Example Responses

### Success (201 Created):
```json
{
  "id": 2,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "profile_image": null,
  "address": "123 Main Street",
  "state": "California",
  "city": "Los Angeles",
  "country": "USA",
  "pincode": "90001",
  "role": "user",
  "created_at": "2025-11-27T03:00:00",
  "updated_at": "2025-11-27T03:00:00"
}
```

### Error - Email Already Exists (400 Bad Request):
```json
{
  "detail": "Email already registered"
}
```

### Error - Validation Failed (422 Unprocessable Entity):
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Name must contain only alphabets",
      "type": "value_error"
    }
  ]
}
```

---

## Quick Test

Try registering a test user:

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Test User\",
    \"email\": \"test@example.com\",
    \"phone\": \"9876543210\",
    \"password\": \"test123\",
    \"state\": \"New York\",
    \"city\": \"New York City\",
    \"country\": \"USA\",
    \"pincode\": \"10001\"
  }"
```

---

## After Registration

Once registered, the user can:
1. **Login** using `/api/auth/login` with email/phone and password
2. **Get their profile** using `/api/auth/me` (requires login token)
3. **Update their profile** using `/api/users/{id}` (requires login token)

---

## Notes

- All new users are registered with `role: "user"` by default
- Only admins can create admin users (or use `create_admin.py` script)
- Password is automatically hashed (never stored in plain text)
- Profile image is optional and saved in the `uploads/` folder


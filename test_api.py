"""
Automated API Testing Script
Tests all endpoints of the User Management System
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
test_results = []

def print_test(name, status, message=""):
    """Print test result"""
    status_symbol = "[PASS]" if status else "[FAIL]"
    print(f"{status_symbol} {name}")
    if message:
        print(f"   {message}")
    test_results.append((name, status, message))

def test_health_check():
    """Test health check endpoint"""
    print("\n[TEST] Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_test("Health Check", True, f"Status: {response.json()}")
        else:
            print_test("Health Check", False, f"Status code: {response.status_code}")
    except Exception as e:
        print_test("Health Check", False, f"Error: {str(e)}")

def test_user_registration():
    """Test user registration"""
    print("\n[TEST] Testing User Registration...")
    
    # Test valid registration
    user_data = {
        "name": "Test User",
        "email": f"test{int(time.time())}@example.com",
        "phone": f"123456{int(time.time()) % 10000}",
        "password": "test123",
        "state": "California",
        "city": "San Francisco",
        "country": "USA",
        "pincode": "94102"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code == 201:
            user = response.json()
            print_test("User Registration (Valid)", True, f"User ID: {user.get('id')}")
            return user
        else:
            print_test("User Registration (Valid)", False, f"Status: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print_test("User Registration (Valid)", False, f"Error: {str(e)}")
        return None

def test_user_registration_validation():
    """Test registration validation"""
    print("\n[TEST] Testing Registration Validation...")
    
    # Test invalid name (too short)
    invalid_data = {
        "name": "Ab",
        "email": "test@example.com",
        "phone": "1234567890",
        "password": "test123",
        "state": "CA",
        "city": "SF",
        "country": "USA",
        "pincode": "94102"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=invalid_data)
        if response.status_code == 422:  # Validation error
            print_test("Registration Validation (Invalid Name)", True)
        else:
            print_test("Registration Validation (Invalid Name)", False, f"Expected 422, got {response.status_code}")
    except Exception as e:
        print_test("Registration Validation (Invalid Name)", False, f"Error: {str(e)}")

def test_user_login(user_email, password):
    """Test user login"""
    print("\n[TEST] Testing User Login...")
    
    login_data = {
        "email_or_phone": user_email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            tokens = response.json()
            print_test("User Login", True, "Tokens received")
            return tokens.get("access_token"), tokens.get("refresh_token")
        else:
            print_test("User Login", False, f"Status: {response.status_code}, {response.text}")
            return None, None
    except Exception as e:
        print_test("User Login", False, f"Error: {str(e)}")
        return None, None

def test_get_current_user(access_token):
    """Test get current user"""
    print("\n[TEST] Testing Get Current User...")
    
    if not access_token:
        print_test("Get Current User", False, "No access token")
        return None
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print_test("Get Current User", True, f"User: {user.get('name')}")
            return user
        else:
            print_test("Get Current User", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Get Current User", False, f"Error: {str(e)}")
        return None

def test_refresh_token(refresh_token):
    """Test refresh token"""
    print("\n[TEST] Testing Refresh Token...")
    
    if not refresh_token:
        print_test("Refresh Token", False, "No refresh token")
        return None
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        if response.status_code == 200:
            tokens = response.json()
            print_test("Refresh Token", True, "New tokens received")
            return tokens.get("access_token")
        else:
            print_test("Refresh Token", False, f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Refresh Token", False, f"Error: {str(e)}")
        return None

def test_get_users(admin_token):
    """Test get all users (admin only)"""
    print("\n[TEST] Testing Get All Users...")
    
    if not admin_token:
        print_test("Get All Users", False, "No admin token")
        return
    
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/api/users?page=1&page_size=10", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print_test("Get All Users", True, f"Total: {data.get('total')}, Page: {data.get('page')}")
        else:
            print_test("Get All Users", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get All Users", False, f"Error: {str(e)}")

def test_get_single_user(user_id, access_token):
    """Test get single user"""
    print("\n[TEST] Testing Get Single User...")
    
    if not access_token:
        print_test("Get Single User", False, "No access token")
        return
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=headers)
        if response.status_code == 200:
            user = response.json()
            print_test("Get Single User", True, f"User: {user.get('name')}")
        else:
            print_test("Get Single User", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get Single User", False, f"Error: {str(e)}")

def test_update_user(user_id, access_token):
    """Test update user"""
    print("\n[TEST] Testing Update User...")
    
    if not access_token:
        print_test("Update User", False, "No access token")
        return
    
    update_data = {
        "name": "Updated Test User",
        "city": "Los Angeles"
    }
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.put(
            f"{BASE_URL}/api/users/{user_id}",
            json=update_data,
            headers=headers
        )
        if response.status_code == 200:
            user = response.json()
            print_test("Update User", True, f"Updated name: {user.get('name')}")
        else:
            print_test("Update User", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Update User", False, f"Error: {str(e)}")

def test_search_users(admin_token):
    """Test search users"""
    print("\n[TEST] Testing Search Users...")
    
    if not admin_token:
        print_test("Search Users", False, "No admin token")
        return
    
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/users?page=1&page_size=10&search=Test",
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            print_test("Search Users", True, f"Found: {len(data.get('data', []))} users")
        else:
            print_test("Search Users", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Search Users", False, f"Error: {str(e)}")

def test_unauthorized_access():
    """Test unauthorized access"""
    print("\n[TEST] Testing Unauthorized Access...")
    
    try:
        # Try to access protected endpoint without token
        response = requests.get(f"{BASE_URL}/api/users")
        if response.status_code == 401:
            print_test("Unauthorized Access (No Token)", True)
        else:
            print_test("Unauthorized Access (No Token)", False, f"Expected 401, got {response.status_code}")
    except Exception as e:
        print_test("Unauthorized Access (No Token)", False, f"Error: {str(e)}")

def create_admin_user():
    """Create admin user for testing"""
    print("\n[TEST] Creating Admin User...")
    
    admin_data = {
        "name": "Admin Test",
        "email": f"admin{int(time.time())}@example.com",
        "phone": f"999{int(time.time()) % 1000000}",
        "password": "admin123",
        "state": "State",
        "city": "City",
        "country": "Country",
        "pincode": "12345"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=admin_data)
        if response.status_code == 201:
            user = response.json()
            # Note: In real scenario, you'd need to update role to admin in database
            print_test("Create Admin User", True, "User created (role needs manual update)")
            return admin_data["email"], admin_data["password"]
        else:
            print_test("Create Admin User", False, f"Status: {response.status_code}")
            return None, None
    except Exception as e:
        print_test("Create Admin User", False, f"Error: {str(e)}")
        return None, None

def main():
    """Run all tests"""
    print("=" * 60)
    print("User Management System - API Testing")
    print("=" * 60)
    print(f"\nTesting against: {BASE_URL}")
    print("Make sure the server is running!\n")
    
    # Test health check
    test_health_check()
    
    # Test registration
    user = test_user_registration()
    if not user:
        print("\n[ERROR] Cannot continue tests without registered user")
        return
    
    user_email = user.get("email")
    user_id = user.get("id")
    
    # Test validation
    test_user_registration_validation()
    
    # Test login
    access_token, refresh_token = test_user_login(user_email, "test123")
    
    # Test get current user
    current_user = test_get_current_user(access_token)
    
    # Test refresh token
    new_access_token = test_refresh_token(refresh_token)
    if new_access_token:
        access_token = new_access_token
    
    # Test get single user
    test_get_single_user(user_id, access_token)
    
    # Test update user
    test_update_user(user_id, access_token)
    
    # Test unauthorized access
    test_unauthorized_access()
    
    # Note: Admin endpoints require admin token
    # You need to create an admin user first using create_admin.py
    print("\n[WARNING] Admin endpoint tests require admin user.")
    print("   Run 'python create_admin.py' first, then login to get admin token.")
    
    # Print summary
    print("\n" + "=" * 60)
    print("[SUMMARY] Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, status, _ in test_results if status)
    total = len(test_results)
    
    print(f"\n[PASS] Passed: {passed}/{total}")
    print(f"[FAIL] Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed!")
    else:
        print("\n[WARNING] Some tests failed. Check the output above for details.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[WARNING] Tests interrupted by user")
    except Exception as e:
        print(f"\n\n[ERROR] Test script error: {str(e)}")


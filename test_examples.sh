#!/bin/bash
# Example cURL commands for testing the API
# Make sure the server is running on http://localhost:8000

echo "User Management System - API Testing Examples"
echo "================================================"
echo ""

# Variables
BASE_URL="http://localhost:8000"
EMAIL="test@example.com"
PASSWORD="test123"

echo "1. Health Check"
echo "---------------"
curl -X GET "$BASE_URL/health"
echo -e "\n\n"

echo "2. Register User"
echo "----------------"
curl -X POST "$BASE_URL/api/auth/register" \
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
echo -e "\n\n"

echo "3. Login"
echo "-------"
TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email_or_phone\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")
echo "$TOKEN_RESPONSE"
echo -e "\n\n"

# Extract token (requires jq or manual extraction)
# ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

echo "4. Get Current User (replace YOUR_TOKEN)"
echo "----------------------------------------"
echo "curl -X GET \"$BASE_URL/api/auth/me\" \\"
echo "  -H \"Authorization: Bearer YOUR_TOKEN\""
echo -e "\n\n"

echo "5. Get All Users (Admin only - replace ADMIN_TOKEN)"
echo "----------------------------------------------------"
echo "curl -X GET \"$BASE_URL/api/users?page=1&page_size=10\" \\"
echo "  -H \"Authorization: Bearer ADMIN_TOKEN\""
echo -e "\n\n"

echo "6. Search Users (Admin only)"
echo "----------------------------"
echo "curl -X GET \"$BASE_URL/api/users?page=1&page_size=10&search=john\" \\"
echo "  -H \"Authorization: Bearer ADMIN_TOKEN\""
echo -e "\n\n"

echo "[SUCCESS] Test examples ready!"
echo "Replace YOUR_TOKEN and ADMIN_TOKEN with actual tokens from login response"


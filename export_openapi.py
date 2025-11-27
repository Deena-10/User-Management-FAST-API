"""
Script to export OpenAPI schema to JSON file
Run this script to generate openapi.json for Postman or other tools
"""
import json
from app.main import app

# Generate OpenAPI schema
openapi_schema = app.openapi()

# Save to file
with open("openapi.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)

print("OpenAPI schema exported to openapi.json")
print("You can import this file into Postman or other API testing tools")


"""
Script to create an admin user
Run this script to create an admin user in the database
"""
from app.database import SessionLocal
from app.models import User, UserRole
from app.auth import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
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
        print("Admin user created successfully!")
        print("Email: admin@example.com")
        print("Password: admin123")
        print("\nPlease change the password after first login!")
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()


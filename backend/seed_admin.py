"""
Admin user seeding script to this to create an admin user for the chat application
"""

from database import SessionLocal, create_tables
from Models.database_models import UserDB
from Models.User.UserModel import UserStatus, UserRole
import hashlib
from datetime import datetime

# Function to hash passwords
def hash_password(password: str) -> str:
    """Simple password hashing - use proper hashing in production"""
    return hashlib.sha256(password.encode()).hexdigest()

# Function to seed admin user
def seed_admin_user():
    """Create an admin user"""
    # Create database tables if they don't exist
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Check if admin user already exists or not
        existing_admin = db.query(UserDB).filter(
            UserDB.username == "admin"
        ).first()
        
        if existing_admin:
            print("❌ Admin user already exists!")
            print(f"   Username: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            print(f"   Role: {existing_admin.role}")
            return
        
        # Create admin user if it doesn't exist
        admin_password = "admin123"
        hashed_password = hash_password(admin_password)
        
        # Create admin user
        admin_user = UserDB(
            username="admin",
            email="admin@chatapp.com",
            password_hash=hashed_password,
            display_name="System Administrator",
            bio="Chat application administrator",
            status=UserStatus.ONLINE,
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            last_seen=datetime.utcnow()
        )
        
        # Add admin user to the database
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # print admin user details
        print(" Admin user created successfully!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: {admin_password}")
        print(f"   Role: {admin_user.role}")
        print(f"   User ID: {admin_user.id}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

# create sample users
def create_sample_users():
    """Create some sample regular users for testing"""
    db = SessionLocal()
    
    try:
        sample_users = [
            {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "password123",
                "display_name": "John Doe",
                "bio": "Software developer"
            },
            {
                "username": "jane_smith",
                "email": "jane@example.com", 
                "password": "password123",
                "display_name": "Jane Smith",
                "bio": "UI/UX Designer"
            },
            {
                "username": "mike_wilson",
                "email": "mike@example.com",
                "password": "password123", 
                "display_name": "Mike Wilson",
                "bio": "Product Manager"
            }
        ]
        

        created_count = 0
        for user_data in sample_users:
            # Check if user already exists
            existing_user = db.query(UserDB).filter(
                UserDB.username == user_data["username"]
            ).first()
            
            if not existing_user:
                hashed_password = hash_password(user_data["password"])
                
                user = UserDB(
                    username=user_data["username"],
                    email=user_data["email"],
                    password_hash=hashed_password,
                    display_name=user_data["display_name"],
                    bio=user_data["bio"],
                    status=UserStatus.OFFLINE,
                    role=UserRole.USER,
                    is_active=True,
                    is_verified=True
                )
                
                db.add(user)
                created_count += 1
        
        if created_count > 0:
            db.commit()
            print(f" Created {created_count} sample users!")
        else:
            print("ℹ Sample users already exist.")
            
    except Exception as e:
        print(f" Error creating sample users: {e}")
        db.rollback()
    finally:
        db.close()

# Main execution
if __name__ == "__main__":
    print(" Starting admin user seeding...")
    print("=" * 50)
    
    # Create admin user
    seed_admin_user()
    
    print("\n" + "=" * 50)
    print(" Creating sample users...")
    
    # Create sample users
    create_sample_users()
    
    # Completion message
    print("\n" + "=" * 50)
    print(" Admin user seeding complete!")
    print("Seeding completed!")
    print("\nYou can now:")
    print("1. Login as admin with username: admin, password: admin123")
    print("2. Access admin dashboard at /admin")
    print("3. Test with sample users (password: password123)")

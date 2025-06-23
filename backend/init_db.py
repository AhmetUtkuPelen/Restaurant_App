"""
Database initialization script
Run this to create the database tables and add sample data
"""

from backend.database import create_tables, drop_tables, SessionLocal
from backend.Models.database_models import UserDB, MessageDB, ChatRoomDB
from backend.Models.User.UserModel import UserStatus, UserRole
from backend.Models.Message.MessageModel import MessageType, MessageStatus
import hashlib
from datetime import datetime

def hash_password(password: str) -> str:
    """Simple password hashing - use proper hashing in production"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_sample_data():
    """Create sample users and messages for testing"""
    db = SessionLocal()
    
    try:
        # Create sample users
        admin_user = UserDB(
            username="admin",
            email="admin@chatapp.com",
            password_hash=hash_password("admin123"),
            display_name="Administrator",
            role=UserRole.ADMIN,
            status=UserStatus.ONLINE,
            is_verified=True
        )
        
        user1 = UserDB(
            username="alice",
            email="alice@example.com",
            password_hash=hash_password("password123"),
            display_name="Alice Johnson",
            status=UserStatus.ONLINE,
            bio="Software developer who loves coding!"
        )
        
        user2 = UserDB(
            username="bob",
            email="bob@example.com",
            password_hash=hash_password("password123"),
            display_name="Bob Smith",
            status=UserStatus.AWAY,
            bio="Designer and coffee enthusiast"
        )
        
        user3 = UserDB(
            username="charlie",
            email="charlie@example.com",
            password_hash=hash_password("password123"),
            display_name="Charlie Brown",
            status=UserStatus.OFFLINE,
            bio="Product manager"
        )
        
        # Add users to database
        db.add_all([admin_user, user1, user2, user3])
        db.commit()
        
        # Refresh to get IDs
        db.refresh(admin_user)
        db.refresh(user1)
        db.refresh(user2)
        db.refresh(user3)
        
        # Create sample chat room
        general_chat = ChatRoomDB(
            name="General",
            description="General discussion room",
            created_by=admin_user.id,
            members=[admin_user.id, user1.id, user2.id, user3.id],
            admins=[admin_user.id]
        )
        
        db.add(general_chat)
        db.commit()
        db.refresh(general_chat)
        
        # Create sample messages
        messages = [
            MessageDB(
                sender_id=admin_user.id,
                chat_id=general_chat.id,
                content="Welcome to the chat app! 🎉",
                message_type=MessageType.TEXT,
                status=MessageStatus.DELIVERED
            ),
            MessageDB(
                sender_id=user1.id,
                chat_id=general_chat.id,
                content="Thanks! This looks great!",
                message_type=MessageType.TEXT,
                status=MessageStatus.READ
            ),
            MessageDB(
                sender_id=user1.id,
                recipient_id=user2.id,
                content="Hey Bob, how's the design coming along?",
                message_type=MessageType.TEXT,
                status=MessageStatus.DELIVERED
            ),
            MessageDB(
                sender_id=user2.id,
                recipient_id=user1.id,
                content="Going well! Should have the mockups ready by tomorrow.",
                message_type=MessageType.TEXT,
                status=MessageStatus.READ
            )
        ]
        
        db.add_all(messages)
        db.commit()
        
        print("✅ Sample data created successfully!")
        print(f"👤 Admin user: admin / admin123")
        print(f"👤 Test users: alice, bob, charlie / password123")
        print(f"💬 Chat room: {general_chat.name}")
        print(f"📝 Created {len(messages)} sample messages")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Initialize database"""
    print("🚀 Initializing database...")
    
    # Create tables
    print("📋 Creating tables...")
    create_tables()
    print("✅ Tables created successfully!")
    
    # Create sample data
    print("📝 Creating sample data...")
    create_sample_data()
    
    print("🎉 Database initialization complete!")
    print("\nYou can now start the server with: uvicorn main:app --reload")

if __name__ == "__main__":
    main()

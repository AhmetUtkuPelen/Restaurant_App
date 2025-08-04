#!/usr/bin/env python3
"""
Simple test to verify enhanced database models.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from database import engine
from Models.database_models import UserDB, AuditLogDB
from Models.User.UserModel import UserStatus, UserRole

def test_models():
    """Test the enhanced database models."""
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("Testing Enhanced Database Models...")
        print("=" * 50)
        
        # Test 1: Create a test user with security fields
        print("\n1. Testing UserDB with security fields...")
        test_user = UserDB(
            username="test_user_enhanced",
            email="test@enhanced.com",
            password_hash="hashed_password_123",
            salt="random_salt_123",
            display_name="Test Enhanced User",
            role=UserRole.USER,
            status=UserStatus.ONLINE
        )
        
        db.add(test_user)
        db.commit()
        print(f"✓ Created user: {test_user.username} (ID: {test_user.id})")
        print(f"  - Security fields present: salt={bool(test_user.salt)}")
        print(f"  - Audit fields present: created_at={bool(test_user.created_at)}")
        print(f"  - Soft delete fields: is_deleted={test_user.is_deleted}")
        
        # Test 2: Test soft delete functionality
        print("\n2. Testing soft delete functionality...")
        print(f"  - Before soft delete: is_deleted={test_user.is_deleted}")
        
        # Soft delete using the mixin
        test_user.soft_delete(db)
        print(f"  - After soft delete: is_deleted={test_user.is_deleted}")
        print(f"  - Deleted at: {test_user.deleted_at}")
        
        # Test 3: Create audit log
        print("\n3. Testing AuditLogDB...")
        audit_log = AuditLogDB.create_log(
            db=db,
            user_id=test_user.id,
            action="test_action",
            resource_type="user",
            resource_id=test_user.id,
            details={"test": "data"},
            ip_address="127.0.0.1",
            success=True,
            risk_level="low"
        )
        print(f"✓ Created audit log: {audit_log.id}")
        print(f"  - Action: {audit_log.action}")
        print(f"  - Risk level: {audit_log.risk_level}")
        
        # Test 4: Test audit log methods
        print("\n4. Testing audit log methods...")
        user_activity = AuditLogDB.get_user_activity(db, test_user.id)
        print(f"✓ User activity logs: {len(user_activity)} entries")
        
        print("\n" + "=" * 50)
        print("✓ All enhanced model tests passed successfully!")
        
        # Cleanup
        db.delete(test_user)
        for log in user_activity:
            db.delete(log)
        db.commit()
        print("✓ Test data cleaned up")
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_models()
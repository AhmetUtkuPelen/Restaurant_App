import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Database import AsyncSessionLocal, engine
from Models.USER.UserModel import User
from Utils.Auth.HashPassword import get_password_hash
from Utils.Enums.Enums import UserRole

logger = logging.getLogger(__name__)


async def seed_admin_users():
    """
    Seed 3 admin users into the database if they don't already exist.
    
    Admin users:
    1. admin - Main administrator
    2. admin2 - Secondary administrator
    3. superadmin - Super administrator
    """
    async with AsyncSessionLocal() as session:
        try:
            admin_users = [
                {
                    "username": "admin",
                    "email": "admin@restaurant.com",
                    "password": "Admin123!@#",
                    "role": UserRole.ADMIN,
                    "phone": "+911234567890",
                    "address": "Admin Office 1, Restaurant HQ",
                    "image_url": "https://res.cloudinary.com/harendra21/image/upload/v1742473055/withcodeexample.com/getting-started-with-python-fastapi-a-comprehensive-guide_tnigh2.jpg"
                },
                {
                    "username": "admin2",
                    "email": "admin2@restaurant.com",
                    "password": "Admin123!@#",
                    "role": UserRole.ADMIN,
                    "phone": "+915551004500",
                    "address": "Admin Office 2, Restaurant HQ",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/150px-Python-logo-notext.svg.png"
                },
                {
                    "username": "admin3",
                    "email": "admin3@restaurant.com",
                    "password": "Admin123!@#",
                    "role": UserRole.ADMIN,
                    "phone": "+995551234500",
                    "address": "Admin Office 3, Restaurant HQ",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Typescript.svg/250px-Typescript.svg.png"
                }
            ]
            
            created_count = 0
            skipped_count = 0
            
            for admin_data in admin_users:
                # Check if user already exists
                stmt = select(User).where(User.username == admin_data["username"])
                result = await session.execute(stmt)
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    logger.info(f"Admin user '{admin_data['username']}' already exists. Skipping.")
                    skipped_count += 1
                    continue
                
                # Check if email already exists
                email_stmt = select(User).where(User.email == admin_data["email"])
                email_result = await session.execute(email_stmt)
                existing_email = email_result.scalar_one_or_none()
                
                if existing_email:
                    logger.info(f"Email '{admin_data['email']}' already exists. Skipping user '{admin_data['username']}'.")
                    skipped_count += 1
                    continue
                
                # Create admin user
                hashed_password = get_password_hash(admin_data["password"])
                
                new_admin = User(
                    username=admin_data["username"],
                    email=admin_data["email"],
                    hashed_password=hashed_password,
                    role=admin_data["role"],
                    phone=admin_data["phone"],
                    address=admin_data["address"],
                    image_url=admin_data["image_url"],
                    is_active=True
                )
                
                session.add(new_admin)
                created_count += 1
                logger.info(f"Created admin user: {admin_data['username']}")
            
            await session.commit()
            
            logger.info(f"Admin user seeding completed. Created: {created_count}, Skipped: {skipped_count}")
            
            if created_count > 0:
                print("\n" + "="*60)
                print("ADMIN USERS CREATED SUCCESSFULLY!")
                print("="*60)
                print("\nYou can now login with these credentials:")
                print("\n1. Main Admin:")
                print("   Username: admin")
                print("   Password: Admin123!@#")
                print("   Email: admin@restaurant.com")
                print("\n2. Secondary Admin:")
                print("   Username: admin2")
                print("   Password: Admin123!@#")
                print("   Email: admin2@restaurant.com")
                print("\n3. Super Admin:")
                print("   Username: superadmin")
                print("   Password: SuperAdmin123!@#")
                print("   Email: superadmin@restaurant.com")
                print("\n" + "="*60)
                print("IMPORTANT: Change these passwords after first login!")
                print("="*60 + "\n")
            
            return {
                "success": True,
                "created": created_count,
                "skipped": skipped_count,
                "total": len(admin_users)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Error seeding admin users: {str(e)}")
            raise


async def main():
    """
    Main function to run the seeding script.
    """
    try:
        logger.info("Starting admin user seeding...")
        result = await seed_admin_users()
        logger.info(f"Seeding completed: {result}")
    except Exception as e:
        logger.error(f"Seeding failed: {str(e)}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the seeding
    asyncio.run(main())
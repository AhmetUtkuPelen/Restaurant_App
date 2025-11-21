import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from Database.Database import AsyncSessionLocal, engine
from Models.PRODUCT.Doner.DonerModel import Doner
from Utils.Enums.Enums import MeatType, SpiceLevel, DonerSize

logger = logging.getLogger(__name__)


async def seed_doners():
    """
    Seed doner products into the database if they don't already exist. If they Exist Skip
    """
    async with AsyncSessionLocal() as session:
        try:
            doners_data = [
                {
                    "name": "Classic Chicken Doner",
                    "description": "Traditional chicken doner with fresh vegetables, served in warm pita bread",
                    "category": "doner",
                    "tags": ["chicken", "classic", "popular", "pita"],
                    "price": Decimal('35.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.aladinfoods.bg/files/images/2627/ChickenDonerNew_1160x1000.png",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DonerSize.MEDIUM,
                    "meat_type": MeatType.CHICKEN,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Spicy Beef Doner",
                    "description": "Tender beef doner with hot spices, onions, and tomatoes in lavash bread",
                    "category": "doner",
                    "tags": ["beef", "spicy", "hot", "lavash"],
                    "price": Decimal('42.00'),
                    "discount_percentage": Decimal('10.00'),
                    "image_url": "https://images.food52.com/aOM2Tx8Efi8H24nHXGn4A5Qng2g=/a0247e36-ea75-4436-92ee-85a8009c32b2--2021-0427_kathi-kebab-roll_3x2_mark-weinberg-141.jpg?w=1920&q=75",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DonerSize.LARGE,
                    "meat_type": MeatType.BEEF,
                    "spice_level": SpiceLevel.HOT,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Lamb Doner Special",
                    "description": "Premium lamb doner with mild spices, yogurt sauce, and fresh herbs",
                    "category": "doner",
                    "tags": ["lamb", "premium", "yogurt", "herbs"],
                    "price": Decimal('48.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.hungrypaprikas.com/wp-content/uploads/2024/08/Doner-Kebab-20.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DonerSize.LARGE,
                    "meat_type": MeatType.LAMB,
                    "spice_level": SpiceLevel.MILD,
                    "is_vegan": False,
                    "is_alergic": True
                },
                {
                    "name": "Mini Chicken Doner",
                    "description": "Perfect portion chicken doner for light appetite, served with salad",
                    "category": "doner",
                    "tags": ["chicken", "mini", "light", "salad"],
                    "price": Decimal('25.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://cdn.getiryemek.com/restaurants/1697553353498_1125x522.webp",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DonerSize.SMALL,
                    "meat_type": MeatType.CHICKEN,
                    "spice_level": SpiceLevel.MILD,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Mixed Meat Doner",
                    "description": "Combination of chicken and beef doner with medium spices",
                    "category": "doner",
                    "tags": ["mixed", "chicken", "beef", "combination"],
                    "price": Decimal('40.00'),
                    "discount_percentage": Decimal('5.00'),
                    "image_url": "https://www.recipetineats.com/tachyon/2020/07/Beef-or-Lamb-Doner-Kebab_9.jpg?resize=900%2C1260&zoom=0.72",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DonerSize.MEDIUM,
                    "meat_type": MeatType.CHICKEN,  # Primary meat type
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Chicken Doner Plate",
                    "description": "Chicken doner served on a plate with rice, salad, and bread",
                    "category": "doner",
                    "tags": ["chicken", "plate", "rice", "complete"],
                    "price": Decimal('45.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://egeafood.com/wp-content/uploads/2022/12/Chicken-Doner-Kebab-plate-min-1024x683.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DonerSize.LARGE,
                    "meat_type": MeatType.CHICKEN,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Beef Doner Wrap",
                    "description": "Beef doner wrapped in tortilla with vegetables and sauce",
                    "category": "doner",
                    "tags": ["beef", "wrap", "tortilla", "portable"],
                    "price": Decimal('38.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://cdn-mamafatma.b-cdn.net/wp-content/uploads/2023/10/2-21.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DonerSize.MEDIUM,
                    "meat_type": MeatType.BEEF,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Family Size Lamb Doner",
                    "description": "Large portion lamb doner perfect for sharing, served with multiple sides",
                    "category": "doner",
                    "tags": ["lamb", "family", "sharing", "large"],
                    "price": Decimal('85.00'),
                    "discount_percentage": Decimal('15.00'),
                    "image_url": "https://cookingorgeous.com/wp-content/uploads/2021/06/lamb-shish-kebab-19.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DonerSize.LARGE,
                    "meat_type": MeatType.LAMB,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": True
                },
                {
                    "name": "Spicy Chicken Box",
                    "description": "Spicy chicken doner meat served in a box with fries and salad",
                    "category": "doner",
                    "tags": ["chicken", "box", "spicy", "fries"],
                    "price": Decimal('30.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.jimcrowleybutchers.com/image/cache/catalog/products/shredded-chicken-spice-box-700x700.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DonerSize.MEDIUM,
                    "meat_type": MeatType.CHICKEN,
                    "spice_level": SpiceLevel.HOT,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Kids Mini Beef Doner",
                    "description": "Small portion of mild beef doner, perfect for kids",
                    "category": "doner",
                    "tags": ["beef", "kids", "mini", "mild"],
                    "price": Decimal('20.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.shutterstock.com/image-photo/delicious-doner-kebab-pocket-veal-260nw-2318974659.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DonerSize.SMALL,
                    "meat_type": MeatType.BEEF,
                    "spice_level": SpiceLevel.MILD,
                    "is_vegan": False,
                    "is_alergic": False
                }
            ]
            
            created_count = 0
            skipped_count = 0
            
            for doner_data in doners_data:
                ### Check if doner already exists or not ###
                stmt = select(Doner).where(Doner.name == doner_data["name"])
                result = await session.execute(stmt)
                existing_doner = result.scalar_one_or_none()
                
                if existing_doner:
                    logger.info(f" Doner '{doner_data['name']}' already exists. Skipping. ")
                    skipped_count += 1
                    continue
                
                # Create doner
                new_doner = Doner(
                    name=doner_data["name"],
                    description=doner_data["description"],
                    category=doner_data["category"],
                    tags=doner_data["tags"],
                    price=doner_data["price"],
                    discount_percentage=doner_data["discount_percentage"],
                    image_url=doner_data["image_url"],
                    is_active=doner_data["is_active"],
                    is_front_page=doner_data["is_front_page"],
                    size=doner_data["size"],
                    meat_type=doner_data["meat_type"],
                    spice_level=doner_data["spice_level"],
                    is_vegan=doner_data["is_vegan"],
                    is_alergic=doner_data["is_alergic"]
                )
                
                session.add(new_doner)
                created_count += 1
                logger.info(f" Created doner: {doner_data['name']} ")
            
            await session.commit()
            
            logger.info(f" Doner seeding has been completed. Created: {created_count}, Skipped: {skipped_count} ")
            
            if created_count > 0:
                print("\n" + "="*60)
                print("    DONERS HAVE BEEN SEEDED SUCCESSFULLY !    ")
                print("="*60)
                print(f"  Created {created_count} new doners  ")
                print(f"  Skipped {skipped_count} existing doners  ")
                print("="*60 + "\n")
            
            return {
                "success": True,
                "created": created_count,
                "skipped": skipped_count,
                "total": len(doners_data)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f" Error seeding doners: {str(e)} ")
            raise


async def main():
    """Main function for running the doner seeding script."""
    try:
        logger.info(" Starting doner seeding... ")
        result = await seed_doners()
        logger.info(f" Doner seeding completed: {result} ")
    except Exception as e:
        logger.error(f" Doner seeding failed: {str(e)} ")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    ### Run the seeding ###
    asyncio.run(main())
import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from Database.Database import AsyncSessionLocal, engine
from Models.PRODUCT.Kebab.KebabModel import Kebab
from Utils.Enums.Enums import MeatType, SpiceLevel, KebabSize

logger = logging.getLogger(__name__)


async def seed_kebabs():
    """
    Seed kebab products into the database if they don't already exist. IF tyhey Exist Skip
    """
    async with AsyncSessionLocal() as session:
        try:
            kebabs_data = [
                {
                    "name": "Adana Kebab",
                    "description": "Spicy minced lamb kebab grilled on skewers, served with rice and salad",
                    "category": "kebab",
                    "tags": ["adana", "lamb", "spicy", "traditional"],
                    "price": Decimal('55.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://anatoliaturkishfoods.com/storage/meal-images/adana-kebab.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": KebabSize.MEDIUM,
                    "meat_type": MeatType.LAMB,
                    "spice_level": SpiceLevel.HOT,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Chicken Shish Kebab",
                    "description": "Tender chicken pieces marinated and grilled to perfection",
                    "category": "kebab",
                    "tags": ["chicken", "shish", "grilled", "tender"],
                    "price": Decimal('45.00'),
                    "discount_percentage": Decimal('10.00'),
                    "image_url": "https://www.deliciousmagazine.co.uk/wp-content/uploads/2018/07/685328-1-eng-GB_turkish-chicken-shish-768x868.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": KebabSize.MEDIUM,
                    "meat_type": MeatType.CHICKEN,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Beef Kofte Kebab",
                    "description": "Seasoned ground beef formed into patties and grilled",
                    "category": "kebab",
                    "tags": ["beef", "kofte", "seasoned", "patties"],
                    "price": Decimal('48.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.billyparisi.com/wp-content/uploads/2020/10/kofta-1.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": KebabSize.MEDIUM,
                    "meat_type": MeatType.BEEF,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Mixed Grill Kebab",
                    "description": "Combination of chicken, beef, and lamb kebabs with sides",
                    "category": "kebab",
                    "tags": ["mixed", "grill", "combination", "variety"],
                    "price": Decimal('75.00'),
                    "discount_percentage": Decimal('15.00'),
                    "image_url": "https://www.nizampide.com/wp-content/uploads/2018/07/kar%C4%B1%C5%9F%C4%B1k-kebap-%C4%B1zgara-porsiyon-nizam-pide-s%C3%BCtla%C3%A7-istanbul-beyo%C4%9Flu-istiklal-caddesi.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": KebabSize.LARGE,
                    "meat_type": MeatType.LAMB,  # Primary meat type
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Lamb Chops",
                    "description": "Grilled lamb chops with herbs and garlic, served with vegetables",
                    "category": "kebab",
                    "tags": ["lamb", "chops", "herbs", "garlic"],
                    "price": Decimal('65.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.floatingkitchen.net/wp-content/uploads/2016/08/Grilled-Lamb-Chops-2.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": KebabSize.MEDIUM,
                    "meat_type": MeatType.LAMB,
                    "spice_level": SpiceLevel.MILD,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Chicken Wings Kebab",
                    "description": "Marinated chicken wings grilled with special sauce",
                    "category": "kebab",
                    "tags": ["chicken", "wings", "marinated", "sauce"],
                    "price": Decimal('38.00'),
                    "discount_percentage": Decimal('5.00'),
                    "image_url": "https://assets.epicurious.com/photos/57acca5b54c3581a438c5cee/16:9/w_1920,c_limit/chicken-wings-on-skewer-11082016-1.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": KebabSize.SMALL,
                    "meat_type": MeatType.CHICKEN,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Beef Steak Kebab",
                    "description": "Premium beef steak grilled to your preference",
                    "category": "kebab",
                    "tags": ["beef", "steak", "premium", "grilled"],
                    "price": Decimal('85.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.cookingclassy.com/wp-content/uploads/2017/04/steak-kebabs-17-768x1152.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": KebabSize.LARGE,
                    "meat_type": MeatType.BEEF,
                    "spice_level": SpiceLevel.MILD,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Urfa Kebab",
                    "description": "Traditional Urfa-style kebab with mild spices and yogurt",
                    "category": "kebab",
                    "tags": ["urfa", "traditional", "mild", "yogurt"],
                    "price": Decimal('52.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.kulturportali.gov.tr/repoKulturPortali/small/SehirRehberi//TurkMutfagi/20180502144204772_Urfa%20Ciger%20Kebabi.JPG?format=jpg&quality=50",
                    "is_active": True,
                    "is_front_page": False,
                    "size": KebabSize.MEDIUM,
                    "meat_type": MeatType.LAMB,
                    "spice_level": SpiceLevel.MILD,
                    "is_vegan": False,
                    "is_alergic": True
                },
                {
                    "name": "Chicken Beyti Kebab",
                    "description": "Chicken kebab wrapped in lavash bread with tomato sauce",
                    "category": "kebab",
                    "tags": ["chicken", "beyti", "lavash", "tomato"],
                    "price": Decimal('50.00'),
                    "discount_percentage": Decimal('8.00'),
                    "image_url": "https://scontent.fadb3-1.fna.fbcdn.net/v/t1.6435-9/43542707_255830598459238_5258740060093677568_n.jpg?stp=dst-jpg_s960x960_tt6&_nc_cat=105&ccb=1-7&_nc_sid=833d8c&_nc_ohc=C9ojOwdBN1QQ7kNvwESKcdI&_nc_oc=Adluu4sEYb4Rsj0mUWzYdvXM6Gnc9L1OulG96mk0eB_cvkNaixmEKn0mmVKZiSQdDuE&_nc_zt=23&_nc_ht=scontent.fadb3-1.fna&_nc_gid=a3w2OY7TwBBAhfw9lszx3Q&oh=00_AfgMt-r9tsedXumenpGwXeLavAImEbiHJyIMCfo33zIoCg&oe=6942ADAB",
                    "is_active": True,
                    "is_front_page": False,
                    "size": KebabSize.MEDIUM,
                    "meat_type": MeatType.CHICKEN,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                },
                {
                    "name": "Family Kebab Platter",
                    "description": "Large platter with assorted kebabs perfect for sharing",
                    "category": "kebab",
                    "tags": ["family", "platter", "sharing", "assorted"],
                    "price": Decimal('120.00'),
                    "discount_percentage": Decimal('20.00'),
                    "image_url": "https://anatoliaturkishfoods.com/storage/meal-images/screenshot-2025-09-29-at-131212.png",
                    "is_active": True,
                    "is_front_page": True,
                    "size": KebabSize.LARGE,
                    "meat_type": MeatType.LAMB,
                    "spice_level": SpiceLevel.MEDIUM,
                    "is_vegan": False,
                    "is_alergic": False
                }
            ]
            
            created_count = 0
            skipped_count = 0
            
            for kebab_data in kebabs_data:
                ## Check if kebab already exists or not ###
                stmt = select(Kebab).where(Kebab.name == kebab_data["name"])
                result = await session.execute(stmt)
                existing_kebab = result.scalar_one_or_none()
                
                if existing_kebab:
                    logger.info(f" Kebab '{kebab_data['name']}' already exists. Skipping. ")
                    skipped_count += 1
                    continue
                
                # Create kebab
                new_kebab = Kebab(
                    name=kebab_data["name"],
                    description=kebab_data["description"],
                    category=kebab_data["category"],
                    tags=kebab_data["tags"],
                    price=kebab_data["price"],
                    discount_percentage=kebab_data["discount_percentage"],
                    image_url=kebab_data["image_url"],
                    is_active=kebab_data["is_active"],
                    is_front_page=kebab_data["is_front_page"],
                    size=kebab_data["size"],
                    meat_type=kebab_data["meat_type"],
                    spice_level=kebab_data["spice_level"],
                    is_vegan=kebab_data["is_vegan"],
                    is_alergic=kebab_data["is_alergic"]
                )
                
                session.add(new_kebab)
                created_count += 1
                logger.info(f" Created kebab: {kebab_data['name']} ")
            
            await session.commit()
            
            logger.info(f" Kebab seeding completed. Created: {created_count}, Skipped: {skipped_count} ")
            
            if created_count > 0:
                print("\n" + "="*60)
                print(" KEBABS HAVE BEEN SEEDED SUCCESSFULLY! ")
                print("="*60)
                print(f"  Created {created_count} new kebabs  ")
                print(f"  Skipped {skipped_count} existing kebabs  ")
                print("="*60 + "\n")
            
            return {
                "success": True,
                "created": created_count,
                "skipped": skipped_count,
                "total": len(kebabs_data)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f" Error seeding kebabs: {str(e)} ")
            raise


async def main():
    """Main function for running the kebab seeding script."""
    try:
        logger.info(" Starting kebab seeding... ")
        result = await seed_kebabs()
        logger.info(f" Kebab seeding completed: {result} ")
    except Exception as e:
        logger.error(f" Kebab seeding failed: {str(e)} ")
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
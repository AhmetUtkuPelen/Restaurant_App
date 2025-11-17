import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from Database.Database import AsyncSessionLocal, engine
from Models.PRODUCT.Dessert.DessertModel import Dessert
from Utils.Enums.Enums import DessertType

logger = logging.getLogger(__name__)


async def seed_desserts():
    """
    Seed dessert products into the database if they don't already exist.
    """
    async with AsyncSessionLocal() as session:
        try:
            desserts_data = [
                {
                    "name": "Chocolate Lava Cake",
                    "description": "Rich chocolate cake with molten chocolate center, served warm with vanilla ice cream",
                    "category": "dessert",
                    "tags": ["chocolate", "warm", "popular", "signature"],
                    "price": Decimal('45.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.billyparisi.com/wp-content/uploads/2022/02/lava-cake-1.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": False,
                    "is_alergic": True,
                    "dessert_type": DessertType.CAKE,
                    "calories": 420
                },
                {
                    "name": "Turkish Baklava",
                    "description": "Traditional Turkish baklava with layers of phyllo pastry, nuts, and honey syrup",
                    "category": "dessert",
                    "tags": ["traditional", "turkish", "nuts", "honey"],
                    "price": Decimal('35.00'),
                    "discount_percentage": Decimal('10.00'),
                    "image_url": "https://cookingorgeous.com/wp-content/uploads/2021/12/turkish-baklava-with-pistachio-25-1024x683.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": False,
                    "is_alergic": True,
                    "dessert_type": DessertType.BAKLAVA,
                    "calories": 380
                },
                {
                    "name": "Künefe",
                    "description": "Traditional Turkish dessert with shredded phyllo, cheese, and sweet syrup",
                    "category": "dessert",
                    "tags": ["traditional", "turkish", "cheese", "hot"],
                    "price": Decimal('40.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://turkishfoodie.com/wp-content/uploads/2018/06/Kunefe.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": False,
                    "is_alergic": True,
                    "dessert_type": DessertType.KUNEFE,
                    "calories": 450
                },
                {
                    "name": "Vanilla Ice Cream",
                    "description": "Premium vanilla ice cream made with real vanilla beans",
                    "category": "dessert",
                    "tags": ["cold", "vanilla", "classic", "refreshing"],
                    "price": Decimal('25.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://bakerstable.net/wp-content/uploads/2024/07/vanilla-ice-cream-2024-7-scaled.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": False,
                    "is_alergic": True,
                    "dessert_type": DessertType.ICE_CREAM,
                    "calories": 180
                },
                {
                    "name": "Chocolate Brownie",
                    "description": "Fudgy chocolate brownie with walnuts, served with chocolate sauce",
                    "category": "dessert",
                    "tags": ["chocolate", "fudgy", "nuts", "rich"],
                    "price": Decimal('30.00'),
                    "discount_percentage": Decimal('15.00'),
                    "image_url": "https://icecreambakery.in/wp-content/uploads/2024/12/Brownie-Recipe-with-Cocoa-Powder.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": False,
                    "is_alergic": True,
                    "dessert_type": DessertType.BROWNIE,
                    "calories": 350
                },
                {
                    "name": "Tiramisu",
                    "description": "Classic Italian tiramisu with coffee-soaked ladyfingers and mascarpone",
                    "category": "dessert",
                    "tags": ["italian", "coffee", "mascarpone", "classic"],
                    "price": Decimal('42.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.giallozafferano.com/images/260-26067/Tiramisu_1200x800.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": False,
                    "is_alergic": True,
                    "dessert_type": DessertType.TIRAMISU,
                    "calories": 320
                },
                {
                    "name": "Rice Pudding",
                    "description": "Traditional Turkish rice pudding with cinnamon and vanilla",
                    "category": "dessert",
                    "tags": ["traditional", "rice", "cinnamon", "comfort"],
                    "price": Decimal('22.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.allrecipes.com/thmb/TNCYtpz-1U-CLNMgb01j-x5OY-k=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/AR-24059-creamy-rice-pudding-DDMFS-4x3-a47c1f5ad9d449c582d62e6e42da28ac.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": False,
                    "is_alergic": True,
                    "dessert_type": DessertType.PUDDING,
                    "calories": 220
                },
                {
                    "name": "Vegan Chocolate Cake",
                    "description": "Delicious vegan chocolate cake made with plant-based ingredients",
                    "category": "dessert",
                    "tags": ["vegan", "chocolate", "plant-based", "healthy"],
                    "price": Decimal('38.00'),
                    "discount_percentage": Decimal('5.00'),
                    "image_url": "https://jessicainthekitchen.com/wp-content/uploads/2023/01/Chocolate-Cake0315.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": True,
                    "is_alergic": False,
                    "dessert_type": DessertType.CAKE,
                    "calories": 280
                }
            ]
            
            created_count = 0
            skipped_count = 0
            
            for dessert_data in desserts_data:
                # Check if dessert already exists
                stmt = select(Dessert).where(Dessert.name == dessert_data["name"])
                result = await session.execute(stmt)
                existing_dessert = result.scalar_one_or_none()
                
                if existing_dessert:
                    logger.info(f"Dessert '{dessert_data['name']}' already exists. Skipping.")
                    skipped_count += 1
                    continue
                
                # Create dessert
                new_dessert = Dessert(
                    name=dessert_data["name"],
                    description=dessert_data["description"],
                    category=dessert_data["category"],
                    tags=dessert_data["tags"],
                    price=dessert_data["price"],
                    discount_percentage=dessert_data["discount_percentage"],
                    image_url=dessert_data["image_url"],
                    is_active=dessert_data["is_active"],
                    is_front_page=dessert_data["is_front_page"],
                    is_vegan=dessert_data["is_vegan"],
                    is_alergic=dessert_data["is_alergic"],
                    dessert_type=dessert_data["dessert_type"],
                    calories=dessert_data["calories"]
                )
                
                session.add(new_dessert)
                created_count += 1
                logger.info(f"Created dessert: {dessert_data['name']}")
            
            await session.commit()
            
            logger.info(f"Dessert seeding completed. Created: {created_count}, Skipped: {skipped_count}")
            
            if created_count > 0:
                print("\n" + "="*60)
                print("DESSERTS SEEDED SUCCESSFULLY!")
                print("="*60)
                print(f"✅ Created {created_count} new desserts")
                print(f"⏭️  Skipped {skipped_count} existing desserts")
                print("="*60 + "\n")
            
            return {
                "success": True,
                "created": created_count,
                "skipped": skipped_count,
                "total": len(desserts_data)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Error seeding desserts: {str(e)}")
            raise


async def main():
    """Main function to run the dessert seeding script."""
    try:
        logger.info("Starting dessert seeding...")
        result = await seed_desserts()
        logger.info(f"Dessert seeding completed: {result}")
    except Exception as e:
        logger.error(f"Dessert seeding failed: {str(e)}")
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
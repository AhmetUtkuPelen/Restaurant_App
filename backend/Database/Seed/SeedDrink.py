import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from Database.Database import AsyncSessionLocal, engine
from Models.PRODUCT.Drink.DrinkModel import Drink
from Utils.Enums.Enums import DrinkSize

logger = logging.getLogger(__name__)


async def seed_drinks():
    """
    Seed drink products into the database if they don't already exist.
    """
    async with AsyncSessionLocal() as session:
        try:
            drinks_data = [
                {
                    "name": "Fresh Orange Juice",
                    "description": "Freshly squeezed orange juice, rich in vitamin C",
                    "category": "drink",
                    "tags": ["fresh", "orange", "vitamin-c", "healthy"],
                    "price": Decimal('18.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.knowyourproduce.com/wp-content/uploads/2014/04/fresh-squeezed-orange-juice-6.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DrinkSize.MEDIUM,
                    "is_acidic": True
                },
                {
                    "name": "Turkish Tea",
                    "description": "Traditional Turkish black tea served in classic tulip glass",
                    "category": "drink",
                    "tags": ["tea", "turkish", "traditional", "hot"],
                    "price": Decimal('8.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://turkishfoodie.com/wp-content/uploads/2018/07/Turkish-Tea.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DrinkSize.SMALL,
                    "is_acidic": False
                },
                {
                    "name": "Turkish Coffee",
                    "description": "Authentic Turkish coffee prepared in traditional copper pot",
                    "category": "drink",
                    "tags": ["coffee", "turkish", "traditional", "strong"],
                    "price": Decimal('15.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://cookingorgeous.com/wp-content/uploads/2025/08/how-to-make-turkish-coffee-traditional-way-11.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DrinkSize.SMALL,
                    "is_acidic": True
                },
                {
                    "name": "Coca Cola",
                    "description": "Classic Coca Cola served ice cold",
                    "category": "drink",
                    "tags": ["cola", "cold", "fizzy", "classic"],
                    "price": Decimal('12.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://ofma.com.tr/coca-cola-kutu-330-ml-barkod-6642-87-O.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DrinkSize.MEDIUM,
                    "is_acidic": True
                },
                {
                    "name": "Ayran",
                    "description": "Traditional Turkish yogurt drink, refreshing and healthy",
                    "category": "drink",
                    "tags": ["ayran", "yogurt", "traditional", "healthy"],
                    "price": Decimal('10.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://cdn.yemek.com/mnresize/1250/833/uploads/2023/10/ayran-sunum-yemekcom.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": DrinkSize.MEDIUM,
                    "is_acidic": False
                },
                {
                    "name": "Fresh Lemonade",
                    "description": "Homemade lemonade with fresh lemons and mint",
                    "category": "drink",
                    "tags": ["lemon", "fresh", "mint", "summer"],
                    "price": Decimal('16.00'),
                    "discount_percentage": Decimal('10.00'),
                    "image_url": "https://www.kitchentreaty.com/wp-content/uploads/2012/06/lemonade-by-the-glass-3.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DrinkSize.LARGE,
                    "is_acidic": True
                },
                {
                    "name": "Mineral Water",
                    "description": "Natural mineral water, still or sparkling",
                    "category": "drink",
                    "tags": ["water", "mineral", "natural", "healthy"],
                    "price": Decimal('6.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://aussiegold.net.au/wp-content/uploads/2023/10/Pouring-a-fresh-and-clean-water-into-the-glass.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DrinkSize.MEDIUM,
                    "is_acidic": False
                },
                {
                    "name": "Apple Juice",
                    "description": "Pure apple juice made from fresh apples",
                    "category": "drink",
                    "tags": ["apple", "fresh", "sweet", "natural"],
                    "price": Decimal('14.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.alphafoodie.com/wp-content/uploads/2021/11/Apple-Juice-Main1.jpeg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DrinkSize.MEDIUM,
                    "is_acidic": True
                },
                {
                    "name": "Iced Tea",
                    "description": "Refreshing iced tea with lemon and sugar",
                    "category": "drink",
                    "tags": ["tea", "iced", "lemon", "refreshing"],
                    "price": Decimal('13.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://bakingamoment.com/wp-content/uploads/2024/05/IMG_3367-iced-tea.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DrinkSize.LARGE,
                    "is_acidic": True
                },
                {
                    "name": "Pomegranate Juice",
                    "description": "Antioxidant-rich pomegranate juice, healthy and delicious",
                    "category": "drink",
                    "tags": ["pomegranate", "antioxidant", "healthy", "fresh"],
                    "price": Decimal('25.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://healthynibblesandbits.com/wp-content/uploads/2016/11/How-to-Make-Pomegranate-Juice.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "size": DrinkSize.MEDIUM,
                    "is_acidic": True
                }
            ]
            
            created_count = 0
            skipped_count = 0
            
            for drink_data in drinks_data:
                # Check if drink already exists
                stmt = select(Drink).where(Drink.name == drink_data["name"])
                result = await session.execute(stmt)
                existing_drink = result.scalar_one_or_none()
                
                if existing_drink:
                    logger.info(f"Drink '{drink_data['name']}' already exists. Skipping.")
                    skipped_count += 1
                    continue
                
                # Create drink
                new_drink = Drink(
                    name=drink_data["name"],
                    description=drink_data["description"],
                    category=drink_data["category"],
                    tags=drink_data["tags"],
                    price=drink_data["price"],
                    discount_percentage=drink_data["discount_percentage"],
                    image_url=drink_data["image_url"],
                    is_active=drink_data["is_active"],
                    is_front_page=drink_data["is_front_page"],
                    size=drink_data["size"],
                    is_acidic=drink_data["is_acidic"]
                )
                
                session.add(new_drink)
                created_count += 1
                logger.info(f"Created drink: {drink_data['name']}")
            
            await session.commit()
            
            logger.info(f"Drink seeding completed. Created: {created_count}, Skipped: {skipped_count}")
            
            if created_count > 0:
                print("\n" + "="*60)
                print("DRINKS SEEDED SUCCESSFULLY!")
                print("="*60)
                print(f"✅ Created {created_count} new drinks")
                print(f"⏭️  Skipped {skipped_count} existing drinks")
                print("="*60 + "\n")
            
            return {
                "success": True,
                "created": created_count,
                "skipped": skipped_count,
                "total": len(drinks_data)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f"Error seeding drinks: {str(e)}")
            raise


async def main():
    """Main function to run the drink seeding script."""
    try:
        logger.info("Starting drink seeding...")
        result = await seed_drinks()
        logger.info(f"Drink seeding completed: {result}")
    except Exception as e:
        logger.error(f"Drink seeding failed: {str(e)}")
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
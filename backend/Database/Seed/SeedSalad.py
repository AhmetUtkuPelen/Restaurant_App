import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from Database.Database import AsyncSessionLocal, engine
from Models.PRODUCT.Salad.SaladModel import Salad

logger = logging.getLogger(__name__)


async def seed_salads():
    """
    Seed salad products into the database if they don't already exist. IF they exist Skip
    """
    async with AsyncSessionLocal() as session:
        try:
            salads_data = [
                {
                    "name": "Mediterranean Salad",
                    "description": "Fresh mixed greens with tomatoes, olives, feta cheese, and olive oil dressing",
                    "category": "salad",
                    "tags": ["mediterranean", "feta", "olives", "healthy"],
                    "price": Decimal('32.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.fromachefskitchen.com/wp-content/uploads/2022/08/Mediterranean-Chopped-Salad-with-Chickpeas.jpeg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": False,
                    "is_alergic": True,
                    "calories": 280
                },
                {
                    "name": "Caesar Salad",
                    "description": "Classic Caesar salad with romaine lettuce, croutons, parmesan, and Caesar dressing",
                    "category": "salad",
                    "tags": ["caesar", "romaine", "parmesan", "classic"],
                    "price": Decimal('28.00'),
                    "discount_percentage": Decimal('10.00'),
                    "image_url": "https://cdn.loveandlemons.com/wp-content/uploads/2024/12/caesar-salad-recipe-580x783.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": False,
                    "is_alergic": True,
                    "calories": 320
                },
                {
                    "name": "Turkish Shepherd Salad",
                    "description": "Traditional Turkish salad with tomatoes, cucumbers, onions, and herbs",
                    "category": "salad",
                    "tags": ["turkish", "shepherd", "traditional", "fresh"],
                    "price": Decimal('22.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://images.squarespace-cdn.com/content/v1/55d36c60e4b06e5a70aff7c1/02a082f8-114c-426a-8493-7c5dc36d8842/Turkish+Shepherd+Salad-3.jpg?format=2500w",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": True,
                    "is_alergic": False,
                    "calories": 120
                },
                {
                    "name": "Grilled Chicken Salad",
                    "description": "Mixed greens topped with grilled chicken breast, avocado, and balsamic dressing",
                    "category": "salad",
                    "tags": ["chicken", "grilled", "avocado", "protein"],
                    "price": Decimal('42.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.afarmgirlsdabbles.com/wp-content/uploads/2010/07/Southwest-Salad38454.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "size": "large",
                    "is_vegan": False,
                    "is_alergic": False,
                    "calories": 380
                },
                {
                    "name": "Quinoa Power Salad",
                    "description": "Nutritious quinoa salad with roasted vegetables, nuts, and tahini dressing",
                    "category": "salad",
                    "tags": ["quinoa", "power", "nutritious", "vegan"],
                    "price": Decimal('38.00'),
                    "discount_percentage": Decimal('5.00'),
                    "image_url": "https://qualitygreens.com/image/w600/files/5e287636-4610-42ad-830b-6d63d8b0b5a5.png",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": True,
                    "is_alergic": True,
                    "calories": 420
                },
                {
                    "name": "Arugula Salad",
                    "description": "Peppery arugula with cherry tomatoes, pine nuts, and lemon vinaigrette",
                    "category": "salad",
                    "tags": ["arugula", "peppery", "pine-nuts", "light"],
                    "price": Decimal('26.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.healthygffamily.com/wp-content/uploads/2024/01/72DBC6A0-0BCB-4E76-9DA9-975F5CC88C6F-720x720.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": True,
                    "is_alergic": True,
                    "calories": 180
                },
                {
                    "name": "Tuna Salad",
                    "description": "Fresh tuna salad with mixed greens, boiled eggs, and olive oil dressing",
                    "category": "salad",
                    "tags": ["tuna", "protein", "eggs", "omega-3"],
                    "price": Decimal('45.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2020/04/Tuna-Salad-6-1024x1536.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": False,
                    "is_alergic": False,
                    "calories": 350
                },
                {
                    "name": "Caprese Salad",
                    "description": "Fresh mozzarella, tomatoes, and basil with balsamic glaze",
                    "category": "salad",
                    "tags": ["caprese", "mozzarella", "basil", "italian"],
                    "price": Decimal('35.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://www.fromachefskitchen.com/wp-content/uploads/2024/07/Caprese-Pasta-Salad.jpeg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": False,
                    "is_alergic": True,
                    "calories": 250
                },
                {
                    "name": "Spinach and Strawberry Salad",
                    "description": "Baby spinach with fresh strawberries, goat cheese, and poppy seed dressing",
                    "category": "salad",
                    "tags": ["spinach", "strawberry", "goat-cheese", "sweet"],
                    "price": Decimal('33.00'),
                    "discount_percentage": Decimal('8.00'),
                    "image_url": "https://pinchandswirl.com/wp-content/uploads/2021/04/Spinach-Strawberry-Walnut-Salad.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": False,
                    "is_alergic": True,
                    "calories": 220
                },
                {
                    "name": "Vegan Buddha Bowl",
                    "description": "Colorful bowl with quinoa, roasted vegetables, chickpeas, and tahini sauce",
                    "category": "salad",
                    "tags": ["vegan", "buddha", "quinoa", "colorful"],
                    "price": Decimal('40.00'),
                    "discount_percentage": Decimal('0.00'),
                    "image_url": "https://simplyceecee.co/wp-content/uploads/2018/07/veganbuddhabowl-2-927x1024.jpg",
                    "is_active": True,
                    "is_front_page": True,
                    "is_vegan": True,
                    "is_alergic": True,
                    "calories": 480
                },
                {
                    "name": "Protein Power Salad",
                    "description": "Mixed greens with grilled chicken, boiled eggs, chickpeas, and protein-rich toppings",
                    "category": "salad",
                    "tags": ["protein", "power", "chicken", "eggs"],
                    "price": Decimal('48.00'),
                    "discount_percentage": Decimal('12.00'),
                    "image_url": "https://www.shaykeerecipes.com/wp-content/uploads/2025/11/chickpea-egg-power-salad.jpg",
                    "is_active": True,
                    "is_front_page": False,
                    "is_vegan": False,
                    "is_alergic": False,
                    "calories": 520
                }
            ]
            
            created_count = 0
            skipped_count = 0
            
            for salad_data in salads_data:
                ### Check if salad already exists or not ###
                stmt = select(Salad).where(Salad.name == salad_data["name"])
                result = await session.execute(stmt)
                existing_salad = result.scalar_one_or_none()
                
                if existing_salad:
                    logger.info(f" Salad '{salad_data['name']}' already exists. Skipping. ")
                    skipped_count += 1
                    continue
                
                # Create salad
                new_salad = Salad(
                    name=salad_data["name"],
                    description=salad_data["description"],
                    category=salad_data["category"],
                    tags=salad_data["tags"],
                    price=salad_data["price"],
                    discount_percentage=salad_data["discount_percentage"],
                    image_url=salad_data["image_url"],
                    is_active=salad_data["is_active"],
                    is_front_page=salad_data["is_front_page"],
                    is_vegan=salad_data["is_vegan"],
                    is_alergic=salad_data["is_alergic"],
                    calories=salad_data["calories"]
                )
                
                session.add(new_salad)
                created_count += 1
                logger.info(f" Created salad: {salad_data['name']} ")
            
            await session.commit()
            
            logger.info(f" Salad seeding completed. Created: {created_count}, Skipped: {skipped_count} ")
            
            if created_count > 0:
                print("\n" + "="*60)
                print(" SALADS HAVE BEEN SEEDED SUCCESSFULLY! ")
                print("="*60)
                print(f"  Created {created_count} new salads  ")
                print(f"  Skipped {skipped_count} existing salads  ")
                print("="*60 + "\n")
            
            return {
                "success": True,
                "created": created_count,
                "skipped": skipped_count,
                "total": len(salads_data)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f" Error seeding salads: {str(e)} ")
            raise


async def main():
    """Main function for running the salad seeding script."""
    try:
        logger.info(" Starting salad seeding... ")
        result = await seed_salads()
        logger.info(f" Salad seeding completed: {result} ")
    except Exception as e:
        logger.error(f" Salad seeding failed: {str(e)} ")
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
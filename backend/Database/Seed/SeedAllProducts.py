import asyncio
import logging
from Database.Database import engine
from Database.Seed.SeedDessert import seed_desserts
from Database.Seed.SeedDoner import seed_doners
from Database.Seed.SeedDrink import seed_drinks
from Database.Seed.SeedKebab import seed_kebabs
from Database.Seed.SeedSalad import seed_salads

logger = logging.getLogger(__name__)


async def seed_all_products():
    """
    Seed all product types into the database.
    """
    try:
        print("\n" + "="*80)
        print("    STARTING PRODUCT SEEDING FOR RESTAURANT    ")
        print("="*80)
        
        total_created = 0
        total_skipped = 0
        
        # Seed Desserts
        print("\n    Seeding Desserts...    ")
        dessert_result = await seed_desserts()
        total_created += dessert_result["created"]
        total_skipped += dessert_result["skipped"]
        
        # Seed Doners
        print("\n    Seeding Doners...    ")
        doner_result = await seed_doners()
        total_created += doner_result["created"]
        total_skipped += doner_result["skipped"]
        
        # Seed Drinks
        print("\n    Seeding Drinks...    ")
        drink_result = await seed_drinks()
        total_created += drink_result["created"]
        total_skipped += drink_result["skipped"]
        
        # Seed Kebabs
        print("\n    Seeding Kebabs...    ")
        kebab_result = await seed_kebabs()
        total_created += kebab_result["created"]
        total_skipped += kebab_result["skipped"]
        
        # Seed Salads
        print("\n    Seeding Salads...    ")
        salad_result = await seed_salads()
        total_created += salad_result["created"]
        total_skipped += salad_result["skipped"]
        
        # Final Summary
        print("\n" + "="*80)
        print("    PRODUCT SEEDING HAS BEEN COMPLETED SUCCESSFULLY !    ")
        print("="*80)
        print("SUMMARY : ")
        print(f"    Total Products Created: {total_created} ")
        print(f"     Total Products Skipped: {total_skipped} ")
        print(f"    Total Products Processed: {total_created + total_skipped} ")
        print("\n    BREAKDOWN BY CATEGORY :    ")
        print(f"    Desserts: {dessert_result['created']} created, {dessert_result['skipped']} skipped ")
        print(f"    Doners: {doner_result['created']} created, {doner_result['skipped']} skipped ")
        print(f"    Drinks: {drink_result['created']} created, {drink_result['skipped']} skipped ")
        print(f"    Kebabs: {kebab_result['created']} created, {kebab_result['skipped']} skipped ")
        print(f"    Salads: {salad_result['created']} created, {salad_result['skipped']} skipped ")
        print("="*80)
        
        if total_created > 0:
            print("\n    Restaurant is now ready with a full menu !    ")
            print("   You can now : ")
            print("   • Browse products at GET /api/desserts/, /api/doners/, etc.")
            print("   • Add products to cart")
            print("   • Create orders")
            print("   • Make payments")
            print("   • Leave comments and reviews")
            #### If PRoducts have been seeded already , print all products are in DB already ####
        else:
            print("\n All products were already in the database!")
        
        print("\n" + "="*80 + "\n")
        
        return {
            "success": True,
            "total_created": total_created,
            "total_skipped": total_skipped,
            "breakdown": {
                "desserts": dessert_result,
                "doners": doner_result,
                "drinks": drink_result,
                "kebabs": kebab_result,
                "salads": salad_result
            }
        }
        
    except Exception as e:
        logger.error(f"Error in product seeding: {str(e)}")
        raise


async def main():
    """Main function for running all product seedings."""
    try:
        logger.info("    Starting product seeding ...    ")
        result = await seed_all_products()
        logger.info(f"Product seeding completed: {result}")
    except Exception as e:
        logger.error(f"Product seeding failed: {str(e)}")
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
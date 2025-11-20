import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Database.Database import AsyncSessionLocal, engine
from Models.RESERVATION.TableModel import Table
from Utils.Enums.Enums import TableLocation

logger = logging.getLogger(__name__)


async def seed_tables():
    """
    Seed tables into the database if they don't already exist. IF they Exist Skip
    
    Tables are distributed across different locations:
    - Window tables (1-6): 2-4 capacity
    - Patio tables (7-12): 4-6 capacity
    - Main dining room tables (13-20): 2-8 capacity
    """
    async with AsyncSessionLocal() as session:
        try:
            tables_data = [
                # Window Tables (1-6) - Romantic and intimate
                {"table_number": "W1", "capacity": 2, "location": TableLocation.WINDOW},
                {"table_number": "W2", "capacity": 2, "location": TableLocation.WINDOW},
                {"table_number": "W3", "capacity": 4, "location": TableLocation.WINDOW},
                {"table_number": "W4", "capacity": 4, "location": TableLocation.WINDOW},
                {"table_number": "W5", "capacity": 3, "location": TableLocation.WINDOW},
                {"table_number": "W6", "capacity": 2, "location": TableLocation.WINDOW},
                
                # Patio Tables (7-12) - Outdoor dining
                {"table_number": "P1", "capacity": 4, "location": TableLocation.PATIO},
                {"table_number": "P2", "capacity": 6, "location": TableLocation.PATIO},
                {"table_number": "P3", "capacity": 4, "location": TableLocation.PATIO},
                {"table_number": "P4", "capacity": 6, "location": TableLocation.PATIO},
                {"table_number": "P5", "capacity": 5, "location": TableLocation.PATIO},
                {"table_number": "P6", "capacity": 4, "location": TableLocation.PATIO},
                
                # Main Dining Room Tables (13-20) - Various sizes
                {"table_number": "M1", "capacity": 6, "location": TableLocation.MAIN_DINING_ROOM},
                {"table_number": "M2", "capacity": 4, "location": TableLocation.MAIN_DINING_ROOM},
                {"table_number": "M3", "capacity": 6, "location": TableLocation.MAIN_DINING_ROOM},
                {"table_number": "M4", "capacity": 8, "location": TableLocation.MAIN_DINING_ROOM},
                {"table_number": "M5", "capacity": 4, "location": TableLocation.MAIN_DINING_ROOM},
                {"table_number": "M6", "capacity": 4, "location": TableLocation.MAIN_DINING_ROOM},
                {"table_number": "M7", "capacity": 6, "location": TableLocation.MAIN_DINING_ROOM},
                {"table_number": "M8", "capacity": 10, "location": TableLocation.MAIN_DINING_ROOM},
            ]
            
            created_count = 0
            skipped_count = 0
            
            print("\n" + "="*80)
            print(" STARTING TABLE SEEDING FOR RESTAURANT !")
            print("="*80)
            
            for table_data in tables_data:
                ### Check if table already exists or not ###
                stmt = select(Table).where(Table.table_number == table_data["table_number"])
                result = await session.execute(stmt)
                existing_table = result.scalar_one_or_none()
                
                if existing_table:
                    logger.info(f"Table '{table_data['table_number']}' already exists. Skipping.")
                    skipped_count += 1
                    continue
                
                # Create table
                new_table = Table(
                    table_number=table_data["table_number"],
                    capacity=table_data["capacity"],
                    location=table_data["location"],
                    is_available=True
                )
                
                session.add(new_table)
                created_count += 1
                logger.info(f"Created table: {table_data['table_number']} (Capacity: {table_data['capacity']}, Location: {table_data['location'].value})")
            
            await session.commit()
            
            # Print summary
            print("\n" + "="*80)
            print("TABLE SEEDING HAS BEEN COMPLETED !")
            print("="*80)
            print(" SUMMARY : ")
            print(f"   Total Tables Created: {created_count}")
            print(f"     Total Tables Skipped: {skipped_count}")
            print(f"   Total Tables Processed: {created_count + skipped_count}")
            print("\n  BREAKDOWN BY LOCATION : ")
            
            # Count by location
            window_count = sum(1 for t in tables_data if t["location"] == TableLocation.WINDOW)
            patio_count = sum(1 for t in tables_data if t["location"] == TableLocation.PATIO)
            main_count = sum(1 for t in tables_data if t["location"] == TableLocation.MAIN_DINING_ROOM)
            
            print(f"    Window Tables: {window_count} tables (2-4 guests)    ")
            print(f"    Patio Tables: {patio_count} tables (4-6 guests)    ")
            print(f"     Main Dining Room: {main_count} tables (2-8 guests)    ")
            print("="*80)
            
            if created_count > 0:
                print("\n    Your restaurant tables are now ready for reservations !    ")
                print("   You can now : ")
                print("   • View available tables at GET /api/tables/")
                print("   • Create reservations")
                print("   • Manage table availability")
            else:
                print("\n All tables were already in the database ! ")
            
            print("\n" + "="*80 + "\n")
            
            logger.info(f" Table seeding completed. Created: {created_count}, Skipped: {skipped_count} ")
            
            return {
                "success": True,
                "created": created_count,
                "skipped": skipped_count,
                "total": len(tables_data)
            }
            
        except Exception as e:
            await session.rollback()
            logger.error(f" Error seeding tables: {str(e)} ")
            raise


async def main():
    """
    Main function for running the seeding script.
    """
    try:
        logger.info(" Starting table seeding... ")
        result = await seed_tables()
        logger.info(f" Seeding completed: {result} ")
    except Exception as e:
        logger.error(f" Seeding failed: {str(e)} ")
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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime

from Models.RESERVATION.TableModel import Table
from Models.RESERVATION.ReservationModel import Reservation
from Schemas.RESERVATION.TableSchemas import TableCreate,TableUpdate
from Utils.Enums.Enums import ReservationStatus
from Utils.Enums.Enums import TableLocation

from datetime import timedelta



class TableControllers:
    
    @staticmethod
    async def get_all_tables(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Get all tables in the restaurant
        """
        try:
            stmt = select(Table).order_by(Table.table_number)
            result = await db.execute(stmt)
            tables = result.scalars().all()
            
            return [
                {
                    "id": table.id,
                    "table_number": table.table_number,
                    "capacity": table.capacity,
                    "location": table.location.value,
                    "is_available": table.is_available
                }
                for table in tables
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch tables: {str(e)}"
            )

    @staticmethod
    async def get_single_table_by_id(table_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Get a single table by ID with reservation count
        """
        try:
            stmt = select(Table).where(Table.id == table_id)
            result = await db.execute(stmt)
            table = result.scalar_one_or_none()
            
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Table not found"
                )
            
            #### Count active reservations ####
            count_stmt = select(func.count(Reservation.id)).where(
                and_(
                    Reservation.table_id == table_id,
                    Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
                )
            )
            count_result = await db.execute(count_stmt)
            active_reservations = count_result.scalar()
            
            return {
                "id": table.id,
                "table_number": table.table_number,
                "capacity": table.capacity,
                "location": table.location.value,
                "is_available": table.is_available,
                "active_reservations": active_reservations
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch table: {str(e)}"
            )

    @staticmethod
    async def get_available_tables(
        date_time: Optional[datetime] = None,
        min_capacity: Optional[int] = None,
        location: Optional[str] = None,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """
        Get available tables, optionally filtered by datetime, capacity, and location
        If datetime is in there, check for conflicting reservations
        """
        try:
            #### base query ####
            conditions = [Table.is_available == True]
            
            if min_capacity:
                conditions.append(Table.capacity >= min_capacity)
            
            if location:
                try:
                    location_enum = TableLocation(location.lower())
                    conditions.append(Table.location == location_enum)
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid location. Must be one of: {[loc.value for loc in TableLocation]}"
                    )
            
            stmt = select(Table).where(and_(*conditions)).order_by(Table.table_number)
            result = await db.execute(stmt)
            tables = result.scalars().all()
            
            #### If datetime is provided , filter by availability ####
            if date_time:
                available_tables = []
                for table in tables:
                    is_available = await TableControllers._check_table_availability(
                        table.id, date_time, db
                    )
                    if is_available:
                        available_tables.append(table)
                tables = available_tables
            
            return [
                {
                    "id": table.id,
                    "table_number": table.table_number,
                    "capacity": table.capacity,
                    "location": table.location.value,
                    "is_available": table.is_available
                }
                for table in tables
            ]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch available tables: {str(e)}"
            )

    @staticmethod
    async def _check_table_availability(
        table_id: int,
        reservation_time: datetime,
        db: AsyncSession
    ) -> bool:
        """
        Helper: Check if table is available at specific time.
        2-hour reservation time window.
        """
        try:
            #### Define time window (2 hours) ####
            window_start = reservation_time - timedelta(hours=2)
            window_end = reservation_time + timedelta(hours=2)
            
            #### Check for conflicting reservations ####
            stmt = select(Reservation).where(
                and_(
                    Reservation.table_id == table_id,
                    Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED]),
                    Reservation.reservation_time >= window_start,
                    Reservation.reservation_time <= window_end
                )
            )
            result = await db.execute(stmt)
            conflicting = result.scalar_one_or_none()
            
            return conflicting is None
        except Exception:
            return False

    @staticmethod
    async def add_new_table(table_data: TableCreate, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Add a new table to the restaurant.
        """
        try:
            #### Check if table number already exists or not ####
            stmt = select(Table).where(Table.table_number == table_data.table_number)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Table number already exists"
                )
            
            #### Create new table ####
            new_table = Table(
                table_number=table_data.table_number,
                capacity=table_data.capacity,
                location=table_data.location,
                is_available=table_data.is_available
            )
            
            db.add(new_table)
            await db.commit()
            await db.refresh(new_table)
            
            return {
                "message": "Table created successfully",
                "table": {
                    "id": new_table.id,
                    "table_number": new_table.table_number,
                    "capacity": new_table.capacity,
                    "location": new_table.location.value,
                    "is_available": new_table.is_available
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create table: {str(e)}"
            )

    @staticmethod
    async def update_existing_table(
        table_id: int,
        update_data: TableUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Admin : Update existing table information.
        """
        try:
            stmt = select(Table).where(Table.id == table_id)
            result = await db.execute(stmt)
            table = result.scalar_one_or_none()
            
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Table not found"
                )
            
            #### Check table number uniqueness if table is being changed ####
            if update_data.table_number and update_data.table_number != table.table_number:
                check_stmt = select(Table).where(Table.table_number == update_data.table_number)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Table number already exists"
                    )
            
            #### Update fields ####
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(table, key, value)
            
            await db.commit()
            await db.refresh(table)
            
            return {
                "message": "Table updated successfully",
                "table": {
                    "id": table.id,
                    "table_number": table.table_number,
                    "capacity": table.capacity,
                    "location": table.location.value,
                    "is_available": table.is_available
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update table: {str(e)}"
            )

    @staticmethod
    async def delete_table(table_id: int, db: AsyncSession) -> Dict[str, str]:
        """
        Admin : Delete a table. Only allowed if no active reservations
        """
        try:
            stmt = select(Table).where(Table.id == table_id)
            result = await db.execute(stmt)
            table = result.scalar_one_or_none()
            
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Table not found"
                )
            
            #### Check for active reservations ####
            check_stmt = select(Reservation).where(
                and_(
                    Reservation.table_id == table_id,
                    Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
                )
            )
            check_result = await db.execute(check_stmt)
            active_reservation = check_result.scalar_one_or_none()
            
            if active_reservation:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot delete table with active reservations"
                )
            
            await db.delete(table)
            await db.commit()
            
            return {"message": f"Table {table.table_number} deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete table: {str(e)}"
            )

    @staticmethod
    async def get_tables_by_location(location: str, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Get all tables in a specific location
        """
        try:
            try:
                location_enum = TableLocation(location.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid location. Must be one of: {[loc.value for loc in TableLocation]}"
                )
            
            stmt = select(Table).where(Table.location == location_enum).order_by(Table.table_number)
            result = await db.execute(stmt)
            tables = result.scalars().all()
            
            return [
                {
                    "id": table.id,
                    "table_number": table.table_number,
                    "capacity": table.capacity,
                    "location": table.location.value,
                    "is_available": table.is_available
                }
                for table in tables
            ]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch tables by location: {str(e)}"
            )

    @staticmethod
    async def toggle_table_availability(table_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin : Toggle table availability status
        """
        try:
            stmt = select(Table).where(Table.id == table_id)
            result = await db.execute(stmt)
            table = result.scalar_one_or_none()
            
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Table not found"
                )
            
            table.is_available = not table.is_available
            await db.commit()
            await db.refresh(table)
            
            return {
                "message": f"Table {table.table_number} is now {'available' if table.is_available else 'unavailable'}",
                "table": {
                    "id": table.id,
                    "table_number": table.table_number,
                    "capacity": table.capacity,
                    "location": table.location.value,
                    "is_available": table.is_available
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to toggle table availability: {str(e)}"
            )
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime

from Models.RESERVATION.TableModel import Table
from Models.RESERVATION.ReservationModel import Reservation
from Schemas.RESERVATION.TableSchemas import TableCreate,TableUpdate
from Utils.Enums.Enums import ReservationStatus


class TableControllers:
    
    @staticmethod
    async def get_all_tables(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Get all tables in the restaurant.
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
        Get a single table by ID with reservation count.
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
            
            # Get reservation count for this table
            count_stmt = select(func.count(Reservation.id)).where(
                Reservation.table_id == table_id
            )
            count_result = await db.execute(count_stmt)
            reservation_count = count_result.scalar()
            
            return {
                "id": table.id,
                "table_number": table.table_number,
                "capacity": table.capacity,
                "location": table.location.value,
                "is_available": table.is_available,
                "total_reservations": reservation_count
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
        Get available tables, optionally filtered by datetime, capacity, and location.
        If datetime is provided, checks for conflicting reservations.
        """
        try:
            # Base query for available tables
            stmt = select(Table).where(Table.is_available == True)
            
            # Filter by capacity if provided
            if min_capacity:
                stmt = stmt.where(Table.capacity >= min_capacity)
            
            # Filter by location if provided
            if location:
                from Utils.Enums.Enums import TableLocation
                stmt = stmt.where(Table.location == TableLocation(location))
            
            result = await db.execute(stmt)
            tables = result.scalars().all()
            
            # If datetime provided, filter out tables with conflicting reservations
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
        Assumes 2-hour reservation window.
        """
        from datetime import timedelta
        
        # Check for overlapping reservations (2-hour window)
        start_time = reservation_time - timedelta(hours=2)
        end_time = reservation_time + timedelta(hours=2)
        
        stmt = select(Reservation).where(
            and_(
                Reservation.table_id == table_id,
                Reservation.reservation_time >= start_time,
                Reservation.reservation_time <= end_time,
                Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
            )
        )
        
        result = await db.execute(stmt)
        conflicting_reservation = result.scalar_one_or_none()
        
        return conflicting_reservation is None

    @staticmethod
    async def add_new_table(table_data: TableCreate, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Add a new table to the restaurant.
        """
        try:
            # Check if table number already exists
            stmt = select(Table).where(Table.table_number == table_data.table_number)
            result = await db.execute(stmt)
            existing_table = result.scalar_one_or_none()
            
            if existing_table:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Table number {table_data.table_number} already exists"
                )
            
            # Create new table
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
                "message": "Table added successfully",
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
                detail=f"Failed to add table: {str(e)}"
            )

    @staticmethod
    async def update_existing_table(
        table_id: int,
        update_data: TableUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Admin: Update existing table information.
        """
        try:
            # Get table
            stmt = select(Table).where(Table.id == table_id)
            result = await db.execute(stmt)
            table = result.scalar_one_or_none()
            
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Table not found"
                )
            
            # Check table number uniqueness if being changed
            if update_data.table_number and update_data.table_number != table.table_number:
                check_stmt = select(Table).where(Table.table_number == update_data.table_number)
                check_result = await db.execute(check_stmt)
                if check_result.scalar_one_or_none():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Table number {update_data.table_number} already exists"
                    )
            
            # Update fields
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
        Admin: Delete a table. Only allowed if no active reservations.
        """
        try:
            # Get table
            stmt = select(Table).where(Table.id == table_id)
            result = await db.execute(stmt)
            table = result.scalar_one_or_none()
            
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Table not found"
                )
            
            # Check for active reservations
            active_reservations_stmt = select(func.count(Reservation.id)).where(
                and_(
                    Reservation.table_id == table_id,
                    Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
                )
            )
            active_result = await db.execute(active_reservations_stmt)
            active_count = active_result.scalar()
            
            if active_count > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot delete table with {active_count} active reservation(s)"
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
        Get all tables in a specific location.
        """
        try:
            from Utils.Enums.Enums import TableLocation
            
            stmt = select(Table).where(Table.location == TableLocation(location)).order_by(Table.table_number)
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
            
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid location: {location}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch tables by location: {str(e)}"
            )

    @staticmethod
    async def toggle_table_availability(table_id: int, db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Toggle table availability status.
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
            
            status_text = "available" if table.is_available else "unavailable"
            
            return {
                "message": f"Table {table.table_number} is now {status_text}",
                "table": {
                    "id": table.id,
                    "table_number": table.table_number,
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

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_,func
from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone

from Models.RESERVATION.ReservationModel import Reservation
from Models.RESERVATION.TableModel import Table
from Models.USER.UserModel import User
from Schemas.RESERVATION.ReservationSchemas import ReservationCreate,ReservationUpdate
from Utils.Enums.Enums import ReservationStatus


class ReservationControllers:

    @staticmethod
    async def create_new_reservation(
        current_user: User,
        reservation_data: ReservationCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        User: Create a new reservation if table is available. IF Table is not available throw an error
        """
        try:
            # Check if table exists
            table_stmt = select(Table).where(Table.id == reservation_data.table_id)
            table_result = await db.execute(table_stmt)
            table = table_result.scalar_one_or_none()
            
            if not table:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Table not found"
                )
            
            if not table.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Table is not available"
                )
            
            # Check table capacity
            if reservation_data.number_of_guests > table.capacity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Table capacity is {table.capacity}, but {reservation_data.number_of_guests} guests requested"
                )
            
            # Check time slot availability
            is_available = await ReservationControllers._check_time_slot_availability(
                reservation_data.table_id,
                reservation_data.reservation_time,
                db
            )
            
            if not is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Table is not available at the requested time"
                )
            
            # Create reservation
            new_reservation = Reservation(
                user_id=current_user.id,
                table_id=reservation_data.table_id,
                reservation_time=reservation_data.reservation_time,
                number_of_guests=reservation_data.number_of_guests,
                special_requests=reservation_data.special_requests,
                status=ReservationStatus.PENDING
            )
            
            db.add(new_reservation)
            await db.commit()
            await db.refresh(new_reservation)
            
            return {
                "message": "Reservation created successfully",
                "reservation": new_reservation.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create reservation: {str(e)}"
            )

    @staticmethod
    async def _check_time_slot_availability(
        table_id: int,
        reservation_time: datetime,
        db: AsyncSession,
        exclude_reservation_id: int = None
    ) -> bool:
        """
        Helper: Check if time slot is available (2-hour window).
        """
        try:
            # Define time window (2 hours before and after)
            window_start = reservation_time - timedelta(hours=2)
            window_end = reservation_time + timedelta(hours=2)
            
            # Build query conditions
            conditions = [
                Reservation.table_id == table_id,
                Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED]),
                Reservation.reservation_time >= window_start,
                Reservation.reservation_time <= window_end
            ]
            
            # Exclude specific reservation if updating
            if exclude_reservation_id:
                conditions.append(Reservation.id != exclude_reservation_id)
            
            stmt = select(Reservation).where(and_(*conditions))
            result = await db.execute(stmt)
            conflicting = result.scalar_one_or_none()
            
            return conflicting is None
        except Exception:
            return False

    @staticmethod
    async def update_existing_reservation(
        current_user: User,
        reservation_id: int,
        update_data: ReservationUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        User: Update their own reservation if table is available. If Table is not available throw an error
        """
        try:
            # Get reservation
            stmt = select(Reservation).where(Reservation.id == reservation_id)
            result = await db.execute(stmt)
            reservation = result.scalar_one_or_none()
            
            if not reservation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reservation not found"
                )
            
            # Check ownership
            if reservation.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update your own reservations"
                )
            
            # Can't update cancelled reservations
            if reservation.status == ReservationStatus.CANCELLED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot update cancelled reservation"
                )
            
            # If changing table, check new table
            if update_data.table_id and update_data.table_id != reservation.table_id:
                table_stmt = select(Table).where(Table.id == update_data.table_id)
                table_result = await db.execute(table_stmt)
                table = table_result.scalar_one_or_none()
                
                if not table:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Table not found"
                    )
                
                if not table.is_available:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Table is not available"
                    )
                
                # Check capacity
                guests = update_data.number_of_guests or reservation.number_of_guests
                if guests > table.capacity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Table capacity is {table.capacity}, but {guests} guests requested"
                    )
            
            # If changing time or table, check availability
            if update_data.reservation_time or update_data.table_id:
                check_table_id = update_data.table_id or reservation.table_id
                check_time = update_data.reservation_time or reservation.reservation_time
                
                is_available = await ReservationControllers._check_time_slot_availability(
                    check_table_id,
                    check_time,
                    db,
                    exclude_reservation_id=reservation_id
                )
                
                if not is_available:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Table is not available at the requested time"
                    )
            
            # Update fields
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(reservation, key, value)
            
            await db.commit()
            await db.refresh(reservation)
            
            return {
                "message": "Reservation updated successfully",
                "reservation": reservation.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update reservation: {str(e)}"
            )

    @staticmethod
    async def cancel_existing_reservation(
        current_user: User,
        reservation_id: int,
        db: AsyncSession
    ) -> Dict[str, str]:
        """
        User: Cancel their own reservation.
        """
        try:
            stmt = select(Reservation).where(Reservation.id == reservation_id)
            result = await db.execute(stmt)
            reservation = result.scalar_one_or_none()
            
            if not reservation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reservation not found"
                )
            
            # Check ownership
            if reservation.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only cancel your own reservations"
                )
            
            # Check if already cancelled
            if reservation.status == ReservationStatus.CANCELLED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Reservation is already cancelled"
                )
            
            reservation.status = ReservationStatus.CANCELLED
            await db.commit()
            
            return {"message": "Reservation cancelled successfully"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel reservation: {str(e)}"
            )

    @staticmethod
    async def get_users_all_reservations(
        current_user: User,
        include_cancelled: bool = False,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """
        User: Get all their own reservations.
        """
        try:
            conditions = [Reservation.user_id == current_user.id]
            
            if not include_cancelled:
                conditions.append(Reservation.status != ReservationStatus.CANCELLED)
            
            stmt = select(Reservation).where(and_(*conditions)).order_by(Reservation.reservation_time.desc())
            result = await db.execute(stmt)
            reservations = result.scalars().all()
            
            return [reservation.to_dict() for reservation in reservations]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch reservations: {str(e)}"
            )

    @staticmethod
    async def get_user_single_reservation_by_id(
        current_user: User,
        reservation_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        User: Get a single reservation by ID (must be their own).
        """
        try:
            stmt = select(Reservation).where(Reservation.id == reservation_id)
            result = await db.execute(stmt)
            reservation = result.scalar_one_or_none()
            
            if not reservation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reservation not found"
                )
            
            # Check ownership
            if reservation.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view your own reservations"
                )
            
            return reservation.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch reservation: {str(e)}"
            )

    # ============================================
    # ADMIN FUNCTIONS
    # ============================================

    @staticmethod
    async def get_all_reservations(
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[ReservationStatus] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """
        Admin: Get all reservations with pagination and filtering.
        """
        try:
            # Build query
            conditions = []
            if status_filter:
                conditions.append(Reservation.status == status_filter)
            
            # Get total count
            count_stmt = select(func.count(Reservation.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            # Get reservations
            stmt = select(Reservation).order_by(Reservation.reservation_time.desc()).offset(skip).limit(limit)
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            reservations = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "reservations": [reservation.to_dict() for reservation in reservations]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch reservations: {str(e)}"
            )

    @staticmethod
    async def confirm_reservation(
        reservation_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Admin: Confirm a pending reservation.
        """
        try:
            stmt = select(Reservation).where(Reservation.id == reservation_id)
            result = await db.execute(stmt)
            reservation = result.scalar_one_or_none()
            
            if not reservation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reservation not found"
                )
            
            if reservation.status == ReservationStatus.CANCELLED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot confirm cancelled reservation"
                )
            
            if reservation.status == ReservationStatus.CONFIRMED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Reservation is already confirmed"
                )
            
            reservation.status = ReservationStatus.CONFIRMED
            await db.commit()
            await db.refresh(reservation)
            
            return {
                "message": "Reservation confirmed successfully",
                "reservation": reservation.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to confirm reservation: {str(e)}"
            )

    @staticmethod
    async def get_reservations_by_date(
        date: datetime,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """
        Admin: Get all reservations for a specific date.
        """
        try:
            # Get start and end of day
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            stmt = select(Reservation).where(
                and_(
                    Reservation.reservation_time >= start_of_day,
                    Reservation.reservation_time <= end_of_day
                )
            ).order_by(Reservation.reservation_time)
            
            result = await db.execute(stmt)
            reservations = result.scalars().all()
            
            return [reservation.to_dict() for reservation in reservations]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch reservations by date: {str(e)}"
            )

    @staticmethod
    async def get_upcoming_reservations(
        days: int = 7,
        db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """
        Admin: Get upcoming reservations for next X days.
        """
        try:
            now = datetime.now(timezone.utc)
            end_date = now + timedelta(days=days)
            
            stmt = select(Reservation).where(
                and_(
                    Reservation.reservation_time >= now,
                    Reservation.reservation_time <= end_date,
                    Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
                )
            ).order_by(Reservation.reservation_time)
            
            result = await db.execute(stmt)
            reservations = result.scalars().all()
            
            return [reservation.to_dict() for reservation in reservations]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch upcoming reservations: {str(e)}"
            )

    @staticmethod
    async def get_reservation_statistics(db: AsyncSession) -> Dict[str, Any]:
        """
        Admin: Get reservation statistics.
        """
        try:
            # Total reservations
            total_stmt = select(func.count(Reservation.id))
            total_result = await db.execute(total_stmt)
            total = total_result.scalar()
            
            # By status
            pending_stmt = select(func.count(Reservation.id)).where(Reservation.status == ReservationStatus.PENDING)
            pending_result = await db.execute(pending_stmt)
            pending = pending_result.scalar()
            
            confirmed_stmt = select(func.count(Reservation.id)).where(Reservation.status == ReservationStatus.CONFIRMED)
            confirmed_result = await db.execute(confirmed_stmt)
            confirmed = confirmed_result.scalar()
            
            cancelled_stmt = select(func.count(Reservation.id)).where(Reservation.status == ReservationStatus.CANCELLED)
            cancelled_result = await db.execute(cancelled_stmt)
            cancelled = cancelled_result.scalar()
            
            # Upcoming reservations (next 7 days)
            now = datetime.now(timezone.utc)
            upcoming_end = now + timedelta(days=7)
            upcoming_stmt = select(func.count(Reservation.id)).where(
                and_(
                    Reservation.reservation_time >= now,
                    Reservation.reservation_time <= upcoming_end,
                    Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
                )
            )
            upcoming_result = await db.execute(upcoming_stmt)
            upcoming = upcoming_result.scalar()
            
            # Today's reservations
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            today_stmt = select(func.count(Reservation.id)).where(
                and_(
                    Reservation.reservation_time >= start_of_day,
                    Reservation.reservation_time <= end_of_day,
                    Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED])
                )
            )
            today_result = await db.execute(today_stmt)
            today = today_result.scalar()
            
            return {
                "total_reservations": total,
                "by_status": {
                    "pending": pending,
                    "confirmed": confirmed,
                    "cancelled": cancelled
                },
                "upcoming_7_days": upcoming,
                "today": today
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch statistics: {str(e)}"
            )
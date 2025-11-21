from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import Dict, Any, List, Optional
from decimal import Decimal
from datetime import datetime, timezone
import os

from Models.PAYMENT.PaymentModel import Payment
from Models.ORDER.OrderModel import Order
from Models.RESERVATION.ReservationModel import Reservation
from Models.USER.UserModel import User
from Schemas.PAYMENT.PaymentSchemas import PaymentCreate, PaymentUpdate
from Utils.Enums.Enums import PaymentStatus, OrderStatus, ReservationStatus
from Models.PAYMENT.PaymentModel import payment_orders

class PaymentControllers:
    
    #### HELPER METHODS ####
    #### ============================================ ####
    #### ============================================ ####
    
    @staticmethod
    def _get_iyzico_config() -> Dict[str, str]:
        """ Get Iyzico configs from environment variables """
        return {
            "api_key": os.getenv("IYZICO_API_KEY", ""),
            "secret_key": os.getenv("IYZICO_SECRET_KEY", ""),
            "base_url": os.getenv("IYZICO_BASE_URL", "https://sandbox-api.iyzipay.com"), #### for testing ####
        }
    
    @staticmethod
    async def _validate_orders(order_ids: List[int], user_id: int, db: AsyncSession) -> tuple[List[Order], Decimal]:
        """ Validate orders belong to user and calculate total """
        if not order_ids:
            return [], Decimal('0.00')
        
        stmt = select(Order).where(
            and_(
                Order.id.in_(order_ids),
                Order.user_id == user_id
            )
        )
        result = await db.execute(stmt)
        orders = result.scalars().all()
        
        if len(orders) != len(order_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more orders not found or don't belong to you"
            )
        
        #### Check all orders are pending ####
        for order in orders:
            if order.status != OrderStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Order {order.id} is not pending"
                )
        
        total = sum(order.total_amount for order in orders)
        return orders, total
    
    @staticmethod
    async def _validate_reservation(reservation_id: int, user_id: int, db: AsyncSession) -> tuple[Reservation, Decimal]:
        """ Validate reservation belongs to user """
        stmt = select(Reservation).where(Reservation.id == reservation_id)
        result = await db.execute(stmt)
        reservation = result.scalar_one_or_none()
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not found"
            )
        
        if reservation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Reservation doesn't belong to you"
            )
        
        if reservation.status != ReservationStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reservation is not pending"
            )
        
        #### For testing , using a fixed fee value for reservation (changable any time) ####
        reservation_fee = Decimal('50.00')
        return reservation, reservation_fee
    
    #### ============================================ ####
    #### USER FUNCTIONS ####
    #### ============================================ ####
    
    @staticmethod
    async def create_payment(
        current_user: User,
        payment_data: PaymentCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User : Create a payment for orders or reservation """
        try:
            #### Validate at least one payment target ####
            if not payment_data.order_ids and not payment_data.reservation_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Must provide either order_ids or reservation_id"
                )
            
            orders = []
            reservation = None
            calculated_amount = Decimal('0.00')
            
            #### Validate orders if provided or not ####
            if payment_data.order_ids:
                orders, order_total = await PaymentControllers._validate_orders(
                    payment_data.order_ids, current_user.id, db
                )
                calculated_amount += order_total
            
            #### Validate reservation if provided ####
            if payment_data.reservation_id:
                reservation, reservation_fee = await PaymentControllers._validate_reservation(
                    payment_data.reservation_id, current_user.id, db
                )
                calculated_amount += reservation_fee
            
            #### Verify amount matches ####
            if abs(calculated_amount - payment_data.amount) > Decimal('0.01'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Amount mismatch. Expected: {calculated_amount}, Provided: {payment_data.amount}"
                )
            
            #### Create payment record ####
            new_payment = Payment(
                user_id=current_user.id,
                reservation_id=payment_data.reservation_id,
                amount=payment_data.amount,
                currency=payment_data.currency,
                status=PaymentStatus.PENDING,
                provider="iyzico",
                installment=payment_data.installment,
                ip_address=payment_data.ip_address,
                conversation_id=f"conv_{current_user.id}_{int(datetime.now().timestamp())}",
                basket_id=f"basket_{current_user.id}_{int(datetime.now().timestamp())}",
                payment_metadata=payment_data.metadata or {}
            )
            
            db.add(new_payment)
            await db.flush()
            
            #### Store order IDs before linking ####
            order_ids = [order.id for order in orders]
            
            #### Link orders to payment using the association table ####
            if orders:
                for order in orders:
                    stmt = payment_orders.insert().values(
                        payment_id=new_payment.id,
                        order_id=order.id
                    )
                    await db.execute(stmt)
            
            await db.commit()
            await db.refresh(new_payment)
            
            # This is testing purposed , Iyzico Payment API can be added here in future
            # For now simulate a successful payment
            #### TODO : An actual Iyzico payment API should come here : TODO ####
            
            return {
                "message": "Payment created successfully",
                "payment": {
                    **new_payment.to_dict(),
                    "order_ids": order_ids,
                    "note": "This is a test payment ! If it was production , you would be redirected to Iyzico payment page !"
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create payment: {str(e)}"
            )
    
    @staticmethod
    async def get_user_payments(
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[PaymentStatus] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """User : Get all their own payments """
        try:
            conditions = [Payment.user_id == current_user.id]
            
            if status_filter:
                conditions.append(Payment.status == status_filter)
            
            #### Get total count ####
            count_stmt = select(func.count(Payment.id)).where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            #### Get payments ####
            stmt = select(Payment).options(
                selectinload(Payment.orders),
                selectinload(Payment.reservation)
            ).where(and_(*conditions)).offset(skip).limit(limit).order_by(Payment.created_at.desc())
            
            result = await db.execute(stmt)
            payments = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "payments": [
                    {
                        **payment.to_dict(),
                        "order_ids": [order.id for order in payment.orders]
                    }
                    for payment in payments
                ]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch payments: {str(e)}"
            )
    
    @staticmethod
    async def get_payment_by_id(
        current_user: User,
        payment_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User : Get single payment by ID (must be their own) """
        try:
            stmt = select(Payment).options(
                selectinload(Payment.orders),
                selectinload(Payment.reservation)
            ).where(Payment.id == payment_id)
            
            result = await db.execute(stmt)
            payment = result.scalar_one_or_none()
            
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            #### Check ownership of Payment ####
            if payment.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view your own payments"
                )
            
            return {
                **payment.to_dict(),
                "order_ids": [order.id for order in payment.orders]
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch payment: {str(e)}"
            )
    
    @staticmethod
    async def simulate_payment_completion(
        current_user: User,
        payment_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User : Simulate payment completion for testing only"""
        try:
            stmt = select(Payment).options(
                selectinload(Payment.orders),
                selectinload(Payment.reservation)
            ).where(Payment.id == payment_id)
            
            result = await db.execute(stmt)
            payment = result.scalar_one_or_none()
            
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            #### Check ownership of Payment ####
            if payment.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only complete your own payments"
                )
            
            if payment.status != PaymentStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Payment is not pending"
                )
            
            #### Simulate successful payment for testing ####
            payment.status = PaymentStatus.COMPLETED
            payment.provider_payment_id = f"test_payment_{payment_id}_{int(datetime.now().timestamp())}"
            payment.fraud_status = 0  # Safe
            payment.card_last_four = "0000"
            payment.card_family = "Test Card"
            payment.card_association = "VISA"
            payment.card_type = "CREDIT_CARD"
            
            #### Update related orders ####
            for order in payment.orders:
                order.status = OrderStatus.COMPLETED
                order.completed_at = datetime.now(timezone.utc)
            
            #### Update related reservation ####
            if payment.reservation:
                payment.reservation.status = ReservationStatus.CONFIRMED
            
            await db.commit()
            await db.refresh(payment)
            
            return {
                "message": "Payment completed successfully (TEST MODE)",
                "payment": {
                    **payment.to_dict(),
                    "order_ids": [order.id for order in payment.orders]
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to complete payment: {str(e)}"
            )
    
    ##### ============================================ ####
    #### ADMIN FUNCTIONS
    #### ============================================ ####
    
    @staticmethod
    async def admin_get_all_payments(
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[PaymentStatus] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Admin : Get all payments with pagination """
        try:
            conditions = []
            if status_filter:
                conditions.append(Payment.status == status_filter)
            
            #### Get total count ####
            count_stmt = select(func.count(Payment.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            #### Get payments ####
            stmt = select(Payment).options(
                selectinload(Payment.orders),
                selectinload(Payment.reservation),
                selectinload(Payment.user)
            ).offset(skip).limit(limit).order_by(Payment.created_at.desc())
            
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            payments = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "payments": [
                    {
                        **payment.to_dict(),
                        "username": payment.user.username if payment.user else None,
                        "order_ids": [order.id for order in payment.orders]
                    }
                    for payment in payments
                ]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch payments: {str(e)}"
            )
    
    @staticmethod
    async def admin_get_payment_by_id(payment_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin : Get any payment by ID """
        try:
            stmt = select(Payment).options(
                selectinload(Payment.orders),
                selectinload(Payment.reservation),
                selectinload(Payment.user)
            ).where(Payment.id == payment_id)
            
            result = await db.execute(stmt)
            payment = result.scalar_one_or_none()
            
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            return {
                **payment.to_dict(),
                "username": payment.user.username if payment.user else None,
                "user_email": payment.user.email if payment.user else None,
                "order_ids": [order.id for order in payment.orders]
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch payment: {str(e)}"
            )
    
    @staticmethod
    async def admin_update_payment(
        payment_id: int,
        update_data: PaymentUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin : Update payment status and details """
        try:
            stmt = select(Payment).where(Payment.id == payment_id)
            result = await db.execute(stmt)
            payment = result.scalar_one_or_none()
            
            if not payment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )
            
            #### Update fields ####
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(payment, key, value)
            
            await db.commit()
            await db.refresh(payment)
            
            return {
                "message": "Payment updated successfully",
                "payment": payment.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update payment: {str(e)}"
            )
    
    @staticmethod
    async def admin_get_payment_statistics(db: AsyncSession) -> Dict[str, Any]:
        """Admin : Get payment statistics """
        try:
            #### Total payments ####
            total_stmt = select(func.count(Payment.id))
            total_result = await db.execute(total_stmt)
            total_payments = total_result.scalar()
            
            #### By status ####
            pending_stmt = select(func.count(Payment.id)).where(Payment.status == PaymentStatus.PENDING)
            pending_result = await db.execute(pending_stmt)
            pending = pending_result.scalar()
            
            completed_stmt = select(func.count(Payment.id)).where(Payment.status == PaymentStatus.COMPLETED)
            completed_result = await db.execute(completed_stmt)
            completed = completed_result.scalar()
            
            failed_stmt = select(func.count(Payment.id)).where(Payment.status == PaymentStatus.FAILED)
            failed_result = await db.execute(failed_stmt)
            failed = failed_result.scalar()
            
            #### Total revenue (completed payments) ####
            revenue_stmt = select(func.sum(Payment.amount)).where(Payment.status == PaymentStatus.COMPLETED)
            revenue_result = await db.execute(revenue_stmt)
            total_revenue = revenue_result.scalar() or Decimal('0.00')
            
            #### Average payment amount ####
            avg_stmt = select(func.avg(Payment.amount)).where(Payment.status == PaymentStatus.COMPLETED)
            avg_result = await db.execute(avg_stmt)
            avg_payment = avg_result.scalar() or Decimal('0.00')
            
            return {
                "total_payments": total_payments,
                "by_status": {
                    "pending": pending,
                    "completed": completed,
                    "failed": failed
                },
                "revenue": {
                    "total": float(total_revenue),
                    "average_payment": float(avg_payment)
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch payment statistics: {str(e)}"
            )
    
    @staticmethod
    async def admin_get_user_payments(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Admin : Get all payments for a specific user """
        try:
            #### Check if user exists or not ####
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            #### Get total count ####
            count_stmt = select(func.count(Payment.id)).where(Payment.user_id == user_id)
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            #### Get payments ####
            stmt = select(Payment).options(
                selectinload(Payment.orders),
                selectinload(Payment.reservation)
            ).where(Payment.user_id == user_id).offset(skip).limit(limit).order_by(Payment.created_at.desc())
            
            result = await db.execute(stmt)
            payments = result.scalars().all()
            
            return {
                "user_id": user_id,
                "username": user.username,
                "total": total,
                "skip": skip,
                "limit": limit,
                "payments": [
                    {
                        **payment.to_dict(),
                        "order_ids": [order.id for order in payment.orders]
                    }
                    for payment in payments
                ]
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user payments: {str(e)}"
            )
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime, timezone

from Models.ORDER.OrderModel import Order
from Models.ORDER.OrderItemModel import OrderItem
from Models.CART.CartModel import Cart
from Models.CART.CartItemModel import CartItem
from Models.PRODUCT.BaseProduct.BaseProductModel import Product
from Models.USER.UserModel import User
from Schemas.ORDER.OrderSchemas import OrderCreate, OrderUpdate
from Utils.Enums.Enums import OrderStatus


class OrderControllers:
    
    #### ============================================ ####
    #### USER CONTROLLERS ####
    #### ============================================ ####
    
    @staticmethod
    async def user_get_all_orders(
        current_user: User,
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[OrderStatus] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """User : Get all his/her own orders """
        try:
            conditions = [Order.user_id == current_user.id]
            
            if status_filter:
                conditions.append(Order.status == status_filter)
            
            #### Get total count ####
            count_stmt = select(func.count(Order.id)).where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            #### Get orders ####
            stmt = select(Order).options(
                selectinload(Order.order_items).selectinload(OrderItem.product)
            ).where(and_(*conditions)).offset(skip).limit(limit).order_by(Order.created_at.desc())
            
            result = await db.execute(stmt)
            orders = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "orders": [
                    {
                        **order.to_dict(),
                        "items_count": len(order.order_items)
                    }
                    for order in orders
                ]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch orders: {str(e)}"
            )

    @staticmethod
    async def user_get_order_by_id(
        current_user: User,
        order_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User : Get single order by ID (must be his/her own) """
        try:
            stmt = select(Order).options(
                selectinload(Order.order_items).selectinload(OrderItem.product)
            ).where(Order.id == order_id)
            
            result = await db.execute(stmt)
            order = result.scalar_one_or_none()
            
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            #### Check ownership of Order ####
            if order.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only view your own orders"
                )
            
            #### Build detailed response ####
            order_items_detailed = []
            for item in order.order_items:
                order_items_detailed.append({
                    **item.to_dict(),
                    "product_name": item.product.name if item.product else None,
                    "product_image_url": item.product.image_url if item.product else None,
                    "product_category": item.product.category if item.product else None
                })
            
            order_dict = order.to_dict()
            order_dict["order_items"] = order_items_detailed
            
            return order_dict
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch order: {str(e)}"
            )

    @staticmethod
    async def user_create_new_order(
        current_user: User,
        order_data: OrderCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User : Create order from cart or explicit items """
        try:
            #### Get user's cart ####
            cart_stmt = select(Cart).options(
                selectinload(Cart.cart_items).selectinload(CartItem.product)
            ).where(Cart.user_id == current_user.id)
            
            cart_result = await db.execute(cart_stmt)
            cart = cart_result.scalar_one_or_none()
            
            if not cart or len(cart.cart_items) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cart is empty. Add items to cart before creating an order."
                )
            
            #### Validate all products are active or not ####
            for cart_item in cart.cart_items:
                if not cart_item.product or not cart_item.product.is_active:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Product '{cart_item.product.name if cart_item.product else 'Unknown'}' is no longer available !"
                    )
            
            #### Calculate total ####
            total_amount = Decimal('0.00')
            for cart_item in cart.cart_items:
                subtotal = cart_item.product.final_price * Decimal(cart_item.quantity)
                total_amount += subtotal
            
            #### Create order ####
            new_order = Order(
                user_id=current_user.id,
                status=OrderStatus.PENDING,
                total_amount=total_amount,
                delivery_address=order_data.delivery_address or current_user.address,
                special_instructions=order_data.special_instructions
            )
            
            db.add(new_order)
            await db.flush()
            
            #### Create order items from cart ####
            for cart_item in cart.cart_items:
                unit_price = cart_item.product.final_price
                subtotal = unit_price * Decimal(cart_item.quantity)
                
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )
                db.add(order_item)
            
            #### Clear cart after order creation ####
            delete_stmt = delete(CartItem).where(CartItem.cart_id == cart.id)
            await db.execute(delete_stmt)
            
            await db.commit()
            await db.refresh(new_order)
            
            #### Load order items for response ####
            stmt = select(Order).options(
                selectinload(Order.order_items).selectinload(OrderItem.product)
            ).where(Order.id == new_order.id)
            result = await db.execute(stmt)
            order_with_items = result.scalar_one()
            
            return {
                "message": "Order created successfully",
                "order": order_with_items.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create order: {str(e)}"
            )

    @staticmethod
    async def user_update_order(
        current_user: User,
        order_id: int,
        update_data: OrderUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """User : Update his/her own order """
        try:
            stmt = select(Order).where(Order.id == order_id)
            result = await db.execute(stmt)
            order = result.scalar_one_or_none()
            
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            #### Check ownership of the Order ####
            if order.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update your own orders"
                )
            
            #### Users can only update pending orders ####
            if order.status != OrderStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Can only update pending orders"
                )
            
            #### Users can only update delivery address and special instructions ####
            if update_data.delivery_address is not None:
                order.delivery_address = update_data.delivery_address
            
            if update_data.special_instructions is not None:
                order.special_instructions = update_data.special_instructions
            
            await db.commit()
            await db.refresh(order)
            
            return {
                "message": "Order updated successfully",
                "order": order.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update order: {str(e)}"
            )

    @staticmethod
    async def user_cancels_order(
        current_user: User,
        order_id: int,
        db: AsyncSession
    ) -> Dict[str, str]:
        """User : Cancel his/her own order """
        try:
            stmt = select(Order).where(Order.id == order_id)
            result = await db.execute(stmt)
            order = result.scalar_one_or_none()
            
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            #### Check ownership of the Order ####
            if order.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only cancel your own orders"
                )
            
            #### Can only cancel pending orders ####
            if order.status != OrderStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Can only cancel pending orders"
                )
            
            order.status = OrderStatus.CANCELLED
            await db.commit()
            
            return {"message": "Order cancelled successfully !"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel order: {str(e)}"
            )

    #### ============================================ ####
    #### ADMIN CONTROLLERS ####
    #### ============================================ ####

    @staticmethod
    async def admin_get_all_orders(
        skip: int = 0,
        limit: int = 100,
        status_filter: Optional[OrderStatus] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Admin : Get all orders with pagination """
        try:
            conditions = []
            if status_filter:
                conditions.append(Order.status == status_filter)
            
            #### Get total count ####
            count_stmt = select(func.count(Order.id))
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            #### Get orders ####
            stmt = select(Order).options(
                selectinload(Order.order_items).selectinload(OrderItem.product),
                selectinload(Order.user)
            ).offset(skip).limit(limit).order_by(Order.created_at.desc())
            
            if conditions:
                stmt = stmt.where(and_(*conditions))
            
            result = await db.execute(stmt)
            orders = result.scalars().all()
            
            return {
                "total": total,
                "skip": skip,
                "limit": limit,
                "orders": [
                    {
                        **order.to_dict(),
                        "username": order.user.username if order.user else None,
                        "items_count": len(order.order_items)
                    }
                    for order in orders
                ]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch orders: {str(e)}"
            )

    @staticmethod
    async def admin_get_order_by_id(order_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin : Get any order by ID """
        try:
            stmt = select(Order).options(
                selectinload(Order.order_items).selectinload(OrderItem.product),
                selectinload(Order.user)
            ).where(Order.id == order_id)
            
            result = await db.execute(stmt)
            order = result.scalar_one_or_none()
            
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            #### Build detailed response ####
            order_items_detailed = []
            for item in order.order_items:
                order_items_detailed.append({
                    **item.to_dict(),
                    "product_name": item.product.name if item.product else None,
                    "product_image_url": item.product.image_url if item.product else None,
                    "product_category": item.product.category if item.product else None
                })
            
            order_dict = order.to_dict()
            order_dict["order_items"] = order_items_detailed
            order_dict["username"] = order.user.username if order.user else None
            order_dict["user_email"] = order.user.email if order.user else None
            
            return order_dict
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch order: {str(e)}"
            )

    @staticmethod
    async def admin_get_single_user_all_orders(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Admin : Get all orders for a specific user """
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
            count_stmt = select(func.count(Order.id)).where(Order.user_id == user_id)
            count_result = await db.execute(count_stmt)
            total = count_result.scalar()
            
            #### Get orders ####
            stmt = select(Order).options(
                selectinload(Order.order_items).selectinload(OrderItem.product)
            ).where(Order.user_id == user_id).offset(skip).limit(limit).order_by(Order.created_at.desc())
            
            result = await db.execute(stmt)
            orders = result.scalars().all()
            
            return {
                "user_id": user_id,
                "username": user.username,
                "total": total,
                "skip": skip,
                "limit": limit,
                "orders": [order.to_dict() for order in orders]
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user orders: {str(e)}"
            )

    @staticmethod
    async def admin_update_order(
        order_id: int,
        update_data: OrderUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin : Update any order (includes status) """
        try:
            stmt = select(Order).where(Order.id == order_id)
            result = await db.execute(stmt)
            order = result.scalar_one_or_none()
            
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            #### Update fields ####
            update_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(order, key, value)
            
            #### Set completed_at if status changed to completed ####
            if update_data.status == OrderStatus.COMPLETED and not order.completed_at:
                order.completed_at = datetime.now(timezone.utc)
            
            await db.commit()
            await db.refresh(order)
            
            return {
                "message": "Order updated successfully",
                "order": order.to_dict()
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update order: {str(e)}"
            )

    @staticmethod
    async def admin_cancels_order(order_id: int, db: AsyncSession) -> Dict[str, str]:
        """Admin : Cancel any order """
        try:
            stmt = select(Order).where(Order.id == order_id)
            result = await db.execute(stmt)
            order = result.scalar_one_or_none()
            
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )
            
            if order.status == OrderStatus.COMPLETED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot cancel completed orders"
                )
            
            order.status = OrderStatus.CANCELLED
            await db.commit()
            
            return {"message": "Order cancelled successfully"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to cancel order: {str(e)}"
            )

    @staticmethod
    async def admin_get_order_statistics(db: AsyncSession) -> Dict[str, Any]:
        """Admin : Get comprehensive order statistics """
        try:
            #### Total orders ####
            total_stmt = select(func.count(Order.id))
            total_result = await db.execute(total_stmt)
            total_orders = total_result.scalar()
            
            #### Orders by status ####
            pending_stmt = select(func.count(Order.id)).where(Order.status == OrderStatus.PENDING)
            pending_result = await db.execute(pending_stmt)
            pending = pending_result.scalar()
            
            completed_stmt = select(func.count(Order.id)).where(Order.status == OrderStatus.COMPLETED)
            completed_result = await db.execute(completed_stmt)
            completed = completed_result.scalar()
            
            cancelled_stmt = select(func.count(Order.id)).where(Order.status == OrderStatus.CANCELLED)
            cancelled_result = await db.execute(cancelled_stmt)
            cancelled = cancelled_result.scalar()
            
            #### Total revenue (completed orders only) ####
            revenue_stmt = select(func.sum(Order.total_amount)).where(Order.status == OrderStatus.COMPLETED)
            revenue_result = await db.execute(revenue_stmt)
            total_revenue = revenue_result.scalar() or Decimal('0.00')
            
            #### Average order value ####
            avg_stmt = select(func.avg(Order.total_amount)).where(Order.status == OrderStatus.COMPLETED)
            avg_result = await db.execute(avg_stmt)
            avg_order_value = avg_result.scalar() or Decimal('0.00')
            
            #### Today's orders ####
            today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            today_stmt = select(func.count(Order.id)).where(Order.created_at >= today_start)
            today_result = await db.execute(today_stmt)
            today_orders = today_result.scalar()
            
            #### This month's orders ####
            month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            month_stmt = select(func.count(Order.id)).where(Order.created_at >= month_start)
            month_result = await db.execute(month_stmt)
            month_orders = month_result.scalar()
            
            return {
                "total_orders": total_orders,
                "by_status": {
                    "pending": pending,
                    "completed": completed,
                    "cancelled": cancelled
                },
                "revenue": {
                    "total": float(total_revenue),
                    "average_order_value": float(avg_order_value)
                },
                "recent": {
                    "today": today_orders,
                    "this_month": month_orders
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch order statistics: {str(e)}"
            )

    @staticmethod
    async def admin_get_order_statistics_by_product_id(
        product_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin : Get order statistics for a specific product by ID """
        try:
            #### Check if product exists or not ####
            product_stmt = select(Product).where(Product.id == product_id)
            product_result = await db.execute(product_stmt)
            product = product_result.scalar_one_or_none()
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            
            #### Total times ordered ####
            count_stmt = select(func.count(OrderItem.id)).where(OrderItem.product_id == product_id)
            count_result = await db.execute(count_stmt)
            times_ordered = count_result.scalar()
            
            #### Total quantity sold ####
            qty_stmt = select(func.sum(OrderItem.quantity)).where(OrderItem.product_id == product_id)
            qty_result = await db.execute(qty_stmt)
            total_quantity = qty_result.scalar() or 0
            
            #### Total revenue from this product ####
            revenue_stmt = select(func.sum(OrderItem.subtotal)).where(OrderItem.product_id == product_id)
            revenue_result = await db.execute(revenue_stmt)
            total_revenue = revenue_result.scalar() or Decimal('0.00')
            
            return {
                "product_id": product_id,
                "product_name": product.name,
                "times_ordered": times_ordered,
                "total_quantity_sold": total_quantity,
                "total_revenue": float(total_revenue)
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch product statistics: {str(e)}"
            )

    @staticmethod
    async def admin_get_order_statistics_by_user_id(
        user_id: int,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin : Get order statistics for a specific user by ID"""
        try:
            #### Check if user exists ####
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            #### Total orders ####
            total_stmt = select(func.count(Order.id)).where(Order.user_id == user_id)
            total_result = await db.execute(total_stmt)
            total_orders = total_result.scalar()
            
            #### Completed orders ####
            completed_stmt = select(func.count(Order.id)).where(
                and_(Order.user_id == user_id, Order.status == OrderStatus.COMPLETED)
            )
            completed_result = await db.execute(completed_stmt)
            completed_orders = completed_result.scalar()
            
            #### Total spent ####
            spent_stmt = select(func.sum(Order.total_amount)).where(
                and_(Order.user_id == user_id, Order.status == OrderStatus.COMPLETED)
            )
            spent_result = await db.execute(spent_stmt)
            total_spent = spent_result.scalar() or Decimal('0.00')
            
            #### Average order value ####
            avg_value = Decimal('0.00')
            if completed_orders > 0:
                avg_value = total_spent / Decimal(completed_orders)
            
            return {
                "user_id": user_id,
                "username": user.username,
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "total_spent": float(total_spent),
                "average_order_value": float(avg_value)
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user statistics: {str(e)}"
            )

    @staticmethod
    async def admin_get_order_statistics_by_date(
        start_date: datetime,
        end_date: datetime,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Admin : Get order statistics for a date range """
        try:
            #### Validate date range ####
            if start_date > end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be before end date"
                )
            
            #### Total orders in range ####
            total_stmt = select(func.count(Order.id)).where(
                and_(Order.created_at >= start_date, Order.created_at <= end_date)
            )
            total_result = await db.execute(total_stmt)
            total_orders = total_result.scalar()
            
            #### Completed orders in range ####
            completed_stmt = select(func.count(Order.id)).where(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date,
                    Order.status == OrderStatus.COMPLETED
                )
            )
            completed_result = await db.execute(completed_stmt)
            completed_orders = completed_result.scalar()
            
            #### Revenue in range ####
            revenue_stmt = select(func.sum(Order.total_amount)).where(
                and_(
                    Order.created_at >= start_date,
                    Order.created_at <= end_date,
                    Order.status == OrderStatus.COMPLETED
                )
            )
            revenue_result = await db.execute(revenue_stmt)
            total_revenue = revenue_result.scalar() or Decimal('0.00')
            
            return {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "total_revenue": float(total_revenue)
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch date range statistics: {str(e)}"
            )
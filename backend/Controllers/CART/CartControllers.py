from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from typing import Dict, Any
from decimal import Decimal

from Models.CART.CartModel import Cart
from Models.CART.CartItemModel import CartItem
from Models.PRODUCT.BaseProduct.BaseProductModel import Product
from Models.USER.UserModel import User
from Schemas.CART.CartSchemas import CartItemCreate, CartItemUpdate


class CartControllers:
    
    ### ============================================ ###
    ### USER FUNCTIONS ###
    ### ============================================ ###
    
    @staticmethod
    async def get_user_cart(current_user: User, db: AsyncSession) -> Dict[str, Any]:
        """ Get A User's Cart with all items and calculated totals """
        try:
            stmt = select(Cart).options(
                selectinload(Cart.cart_items).selectinload(CartItem.product)
            ).where(Cart.user_id == current_user.id)
            
            result = await db.execute(stmt)
            cart = result.scalar_one_or_none()
            
            if not cart:
                #### Create cart if doesn't exist ####
                cart = Cart(user_id=current_user.id)
                db.add(cart)
                await db.commit()
                await db.refresh(cart)
            
            #### detailed Cart Response ####
            cart_items_detailed = []
            for item in cart.cart_items:
                if item.product:
                    cart_items_detailed.append({
                        "id": item.id,
                        "product_id": item.product_id,
                        "product_name": item.product.name,
                        "product_price": float(item.product.price),
                        "product_final_price": float(item.product.final_price),
                        "product_image_url": item.product.image_url,
                        "product_category": item.product.category,
                        "quantity": item.quantity,
                        "subtotal": float(item.product.final_price * Decimal(item.quantity)),
                        "created_at": item.created_at.isoformat() if item.created_at else None
                    })
            
            return {
                "id": cart.id,
                "user_id": cart.user_id,
                "total_items": cart.total_items,
                "total_price": float(cart.total_price),
                "cart_items": cart_items_detailed,
                "created_at": cart.created_at.isoformat() if cart.created_at else None,
                "updated_at": cart.updated_at.isoformat() if cart.updated_at else None
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch cart: {str(e)}"
            )
    
    @staticmethod
    async def add_item_to_cart(
        current_user: User,
        item_data: CartItemCreate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """ Add item to Cart or update quantity if exists """
        try:
            #### Get user's cart ####
            cart_stmt = select(Cart).where(Cart.user_id == current_user.id)
            cart_result = await db.execute(cart_stmt)
            cart = cart_result.scalar_one_or_none()
            
            if not cart:
                cart = Cart(user_id=current_user.id)
                db.add(cart)
                await db.flush()
            
            #### Check if product exists and is active ####
            product_stmt = select(Product).where(Product.id == item_data.product_id)
            product_result = await db.execute(product_stmt)
            product = product_result.scalar_one_or_none()
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            
            if not product.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product is not available"
                )
            
            #### Check if item already exists in cart or not ####
            existing_item_stmt = select(CartItem).where(
                and_(
                    CartItem.cart_id == cart.id,
                    CartItem.product_id == item_data.product_id
                )
            )
            existing_item_result = await db.execute(existing_item_stmt)
            existing_item = existing_item_result.scalar_one_or_none()
            
            if existing_item:
                ### Update quantity ###
                existing_item.quantity += item_data.quantity
                await db.commit()
                await db.refresh(existing_item)
                
                return {
                    "message": "Cart item quantity updated",
                    "cart_item": {
                        "id": existing_item.id,
                        "product_id": existing_item.product_id,
                        "product_name": product.name,
                        "quantity": existing_item.quantity,
                        "product_price": float(product.final_price),
                        "subtotal": float(product.final_price * Decimal(existing_item.quantity))
                    }
                }
            else:
                #### Create new cart item ####
                new_item = CartItem(
                    cart_id=cart.id,
                    product_id=item_data.product_id,
                    quantity=item_data.quantity
                )
                db.add(new_item)
                await db.commit()
                await db.refresh(new_item)
                
                return {
                    "message": "Item added to cart",
                    "cart_item": {
                        "id": new_item.id,
                        "product_id": new_item.product_id,
                        "product_name": product.name,
                        "quantity": new_item.quantity,
                        "product_price": float(product.final_price),
                        "subtotal": float(product.final_price * Decimal(new_item.quantity))
                    }
                }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add item to cart: {str(e)}"
            )
    
    @staticmethod
    async def update_cart_item(
        current_user: User,
        item_id: int,
        item_data: CartItemUpdate,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """ Update cart item quantity """
        try:
            ### Get Cart Item with Cart and Product ###
            stmt = select(CartItem).options(
                selectinload(CartItem.cart),
                selectinload(CartItem.product)
            ).where(CartItem.id == item_id)
            
            result = await db.execute(stmt)
            cart_item = result.scalar_one_or_none()
            
            if not cart_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cart item not found"
                )
            
            #### Check ownership of the Cart Item ####
            if cart_item.cart.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update items in your own cart"
                )
            
            ### Update quantity ###
            cart_item.quantity = item_data.quantity
            await db.commit()
            await db.refresh(cart_item)
            
            return {
                "message": "Cart item updated",
                "cart_item": {
                    "id": cart_item.id,
                    "product_id": cart_item.product_id,
                    "product_name": cart_item.product.name if cart_item.product else None,
                    "quantity": cart_item.quantity,
                    "product_price": float(cart_item.product.final_price) if cart_item.product else 0,
                    "subtotal": float(cart_item.product.final_price * Decimal(cart_item.quantity)) if cart_item.product else 0
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update cart item: {str(e)}"
            )
    
    @staticmethod
    async def remove_cart_item(
        current_user: User,
        item_id: int,
        db: AsyncSession
    ) -> Dict[str, str]:
        """ Remove item from cart """
        try:
            stmt = select(CartItem).options(
                selectinload(CartItem.cart)
            ).where(CartItem.id == item_id)
            
            result = await db.execute(stmt)
            cart_item = result.scalar_one_or_none()
            
            ### check if any Item in Cart or not ###
            if not cart_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cart item not found"
                )
            
            ### Check ownership ###
            if cart_item.cart.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only remove items from your own cart"
                )
            
            await db.delete(cart_item)
            await db.commit()
            
            return {"message": "Item removed from cart"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove cart item: {str(e)}"
            )
    
    @staticmethod
    async def clear_cart(current_user: User, db: AsyncSession) -> Dict[str, str]:
        """ Clear all items from cart """
        try:
            ### Get user's cart ###
            cart_stmt = select(Cart).where(Cart.user_id == current_user.id)
            cart_result = await db.execute(cart_stmt)
            cart = cart_result.scalar_one_or_none()
            
            if not cart:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cart not found"
                )
            
            #### Delete all cart items ####
            delete_stmt = delete(CartItem).where(CartItem.cart_id == cart.id)
            result = await db.execute(delete_stmt)
            await db.commit()
            
            deleted_count = result.rowcount
            
            return {"message": f"Cart cleared. Removed {deleted_count} item(s)"}
        except HTTPException:
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to clear cart: {str(e)}"
            )

    @staticmethod
    async def get_cart_summary(current_user: User, db: AsyncSession) -> Dict[str, Any]:
        """ Get cart summary with totals only """
        try:
            stmt = select(Cart).options(
                selectinload(Cart.cart_items).selectinload(CartItem.product)
            ).where(Cart.user_id == current_user.id)
            
            result = await db.execute(stmt)
            cart = result.scalar_one_or_none()
            
            if not cart:
                return {
                    "total_items": 0,
                    "total_price": 0.0,
                    "item_count": 0
                }
            
            return {
                "total_items": cart.total_items,
                "total_price": float(cart.total_price),
                "item_count": len(cart.cart_items)
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch cart summary: {str(e)}"
            )

    #### ============================================ ####
    #### ADMIN FUNCTIONS ####
    #### ============================================ ####

    @staticmethod
    async def get_single_cart_for_user_by_id(user_id: int, db: AsyncSession) -> Dict[str, Any]:
        """Admin : Get cart for a specific user """
        try:
            #### Check if User exists or not ####
            user_stmt = select(User).where(User.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            stmt = select(Cart).options(
                selectinload(Cart.cart_items).selectinload(CartItem.product)
            ).where(Cart.user_id == user_id)
            
            result = await db.execute(stmt)
            cart = result.scalar_one_or_none()
            
            if not cart:
                return {
                    "user_id": user_id,
                    "username": user.username,
                    "message": "User has no cart"
                }
            
            #### Build detailed Cart response ####
            cart_items_detailed = []
            for item in cart.cart_items:
                if item.product:
                    cart_items_detailed.append({
                        "id": item.id,
                        "product_id": item.product_id,
                        "product_name": item.product.name,
                        "product_price": float(item.product.price),
                        "product_final_price": float(item.product.final_price),
                        "quantity": item.quantity,
                        "subtotal": float(item.product.final_price * Decimal(item.quantity))
                    })
            
            return {
                "id": cart.id,
                "user_id": cart.user_id,
                "username": user.username,
                "total_items": cart.total_items,
                "total_price": float(cart.total_price),
                "cart_items": cart_items_detailed,
                "created_at": cart.created_at.isoformat() if cart.created_at else None,
                "updated_at": cart.updated_at.isoformat() if cart.updated_at else None
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch user cart: {str(e)}"
            )

    @staticmethod
    async def get_all_active_carts(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """Admin : Get all carts that have items in it"""
        try:
            #### Get carts with items ####
            stmt = select(Cart).options(
                selectinload(Cart.cart_items).selectinload(CartItem.product),
                selectinload(Cart.user)
            ).offset(skip).limit(limit)
            
            result = await db.execute(stmt)
            carts = result.scalars().all()
            
            #### Filter carts with items ####
            active_carts = [cart for cart in carts if len(cart.cart_items) > 0]
            
            return {
                "total": len(active_carts),
                "skip": skip,
                "limit": limit,
                "carts": [
                    {
                        "id": cart.id,
                        "user_id": cart.user_id,
                        "username": cart.user.username if cart.user else None,
                        "total_items": cart.total_items,
                        "total_price": float(cart.total_price),
                        "item_count": len(cart.cart_items),
                        "updated_at": cart.updated_at.isoformat() if cart.updated_at else None
                    }
                    for cart in active_carts
                ]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch active carts: {str(e)}"
            )
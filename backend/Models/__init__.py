# Import all models in the correct order to avoid circular dependencies
# Base models first, then models that depend on them

# User model
from Models.USER.UserModel import User

# Product models (base first, then specific types)
from Models.PRODUCT.BaseProduct.BaseProductModel import Product
from Models.PRODUCT.Dessert.DessertModel import Dessert
from Models.PRODUCT.Doner.DonerModel import Doner
from Models.PRODUCT.Drink.DrinkModel import Drink
from Models.PRODUCT.Kebab.KebabModel import Kebab
from Models.PRODUCT.Salad.SaladModel import Salad
from Models.PRODUCT.FavouriteProduct.FavouriteProductModel import FavouriteProduct

# Cart models
from Models.CART.CartModel import Cart
from Models.CART.CartItemModel import CartItem

# Order models
from Models.ORDER.OrderModel import Order
from Models.ORDER.OrderItemModel import OrderItem

# Comment model
from Models.COMMENT.CommentModel import Comment

# Reservation models
from Models.RESERVATION.TableModel import Table
from Models.RESERVATION.ReservationModel import Reservation

# Payment model
from Models.PAYMENT.PaymentModel import Payment

__all__ = [
    "User",
    "Product",
    "Dessert",
    "Doner",
    "Drink",
    "Kebab",
    "Salad",
    "FavouriteProduct",
    "Cart",
    "CartItem",
    "Order",
    "OrderItem",
    "Comment",
    "Table",
    "Reservation",
    "Payment",
]

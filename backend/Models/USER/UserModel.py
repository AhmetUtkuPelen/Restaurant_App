from Database.Database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, Enum as SAEnum, event
from sqlalchemy.orm import relationship
from Utils.Enums.Enums import UserRole
from Utils.Auth.HashPassword import get_password_hash
from backend.Models.CART.CartModel import Cart

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    role = Column(SAEnum(UserRole, native_enum=False), nullable=False, default=UserRole.USER)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    favourite_products = relationship("FavouriteProduct", back_populates="user", lazy="dynamic")
    orders = relationship("Order", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    cart = relationship("Cart", back_populates="user", uselist=False)
    reservations = relationship("Reservation", back_populates="user")
    payments = relationship("Payment", back_populates="user")


    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "image_url": self.image_url,
            "is_active": self.is_active,
            "role": self.role.value if self.role else None,
            "phone": self.phone,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "favourite_products": [favourite_product.product_id for favourite_product in self.favourite_products],
            "orders": [order.id for order in self.orders],
            "comments": [comment.id for comment in self.comments],
            "cart": self.cart.to_dict() if self.cart else None,
            "reservations": [reservation.id for reservation in self.reservations],
            "payments": [payment.id for payment in self.payments]
        }

    @property
    def user_profile(self):
        """
        Returns user profile information.
        Profile exists automatically when User is created.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "image_url": self.image_url,
            "phone": self.phone,
            "address": self.address,
            "role": self.role.value if self.role else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "favourite_products": [favourite_product.product_id for favourite_product in self.favourite_products],
            "orders": [order.id for order in self.orders],
            "comments": [comment.id for comment in self.comments],
            "cart": self.cart.to_dict() if self.cart else None,
            "reservations": [reservation.id for reservation in self.reservations],
            "payments": [payment.id for payment in self.payments],
        }

    def update_profile(self, payload: dict):
        """
        Update user profile information.
        Only updates allowed fields.
        """
        if not isinstance(payload, dict):
            return False

        allowed = ["username", "email", "password", "image_url", "phone", "address"]
        updated = False
        
        for key in allowed:
            if key in payload:
                val = payload.get(key)
                if val is not None:  # Only update if value is provided
                    if key == "password":
                        self.hashed_password = get_password_hash(val)
                        updated = True
                    else:
                        setattr(self, key, val)
                        updated = True
        
        return updated

    def __str__(self):
        return f"<User {self.username}>"

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


# Event listener to automatically create a cart when a new user is created
@event.listens_for(User, 'after_insert')
def create_user_cart(mapper, connection, target):
    """
    Automatically creates an empty cart for a newly registered user.
    This ensures every user has a cart immediately after registration.
    """
    
    # Create cart for the new user
    cart = Cart(user_id=target.id)
    
    # Use the session to add the cart
    from sqlalchemy.orm import Session
    session = Session.object_session(target)
    if session:
        session.add(cart)
        session.flush()  # Flush to make cart available immediately
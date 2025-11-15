from Database.Database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "carts"

    __table_args__ = (
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="cart")
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "cart_items": [item.to_dict() for item in self.cart_items]
        }

    @property
    def total_items(self):
        return sum(item.quantity for item in self.cart_items)

    @property
    def total_price(self):
        from decimal import Decimal
        return sum(
            (item.product.final_price * Decimal(item.quantity)) 
            for item in self.cart_items 
            if item.product
        )

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id}, items={self.total_items})>"
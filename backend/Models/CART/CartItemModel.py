from Database.Database import Base
from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, func, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from decimal import Decimal

class CartItem(Base):
    __tablename__ = "cart_items"

    __table_args__ = (
        CheckConstraint('quantity >= 1', name='check_cartitem_quantity_positive'),
        UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items", lazy="select")

    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<CartItem(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})>"
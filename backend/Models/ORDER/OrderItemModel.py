from Database.Database import Base
from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from decimal import Decimal

class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)  # Price at time of order
    subtotal = Column(Numeric(10, 2), nullable=False)  # quantity * unit_price
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price) if self.unit_price is not None else None,
            "subtotal": float(self.subtotal) if self.subtotal is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})>"
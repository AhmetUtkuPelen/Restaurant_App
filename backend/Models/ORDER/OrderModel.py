from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Numeric,String
from sqlalchemy.orm import relationship, validates
from Database.Database import Base
from Utils.Enums.Enums import OrderStatus
from sqlalchemy import Enum as SAEnum
from Models.PAYMENT.PaymentModel import payment_orders

class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(SAEnum(OrderStatus, native_enum=False), nullable=False, default=OrderStatus.PENDING)
    total_amount = Column(Numeric(10, 2), nullable=False)
    delivery_address = Column(String, nullable=True)
    special_instructions = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", secondary=payment_orders, back_populates="orders")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status.value if hasattr(self.status, "value") else self.status,
            "total_amount": float(self.total_amount) if self.total_amount is not None else None,
            "delivery_address": self.delivery_address,
            "special_instructions": self.special_instructions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "order_items": [item.to_dict() for item in self.order_items]
        }

    @validates('status')
    def validate_status(self, key, value):
        if value == OrderStatus.COMPLETED and not self.completed_at:
            from datetime import datetime
            self.completed_at = datetime.utcnow()
        return value

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total_amount})>"
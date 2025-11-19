from Database.Database import Base
from sqlalchemy import Column, Integer, Numeric, String, DateTime, func, Enum as SAEnum, ForeignKey, Table
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy import JSON
from sqlalchemy.orm import relationship
from Utils.Enums.Enums import PaymentStatus


# association table to link payments and orders (many-to-many)
payment_orders = Table(
    "payment_orders",
    Base.metadata,
    Column("payment_id", Integer, ForeignKey("payments.id", ondelete="CASCADE"), primary_key=True),
    Column("order_id", Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, nullable=False, default="TRY")
    status = Column(SAEnum(PaymentStatus, native_enum=False), nullable=False, default=PaymentStatus.PENDING)
    
    # Payment Provider Fields
    provider = Column(String, nullable=True)  # 'iyzico', 'stripe' , 'etc'
    provider_payment_id = Column(String, nullable=True, index=True)  # Iyzico's payment ID
    provider_payment_token = Column(String, nullable=True)  # Payment token/key
    conversation_id = Column(String, nullable=True)  # Iyzico conversation ID
    
    # Iyzico-specific fields
    installment = Column(Integer, nullable=True, default=1)  # Number of installments
    payment_group = Column(String, nullable=True)  # Iyzico payment group
    fraud_status = Column(Integer, nullable=True)  # Fraud detection status (0=safe, 1=suspicious)
    
    # Card information (masked/safe to store)
    card_last_four = Column(String(4), nullable=True)  # Last 4 digits
    card_family = Column(String, nullable=True)  # 'Bonus', 'Maximum' , 'etc'
    card_association = Column(String, nullable=True)  # 'VISA', 'MASTER_CARD' , 'etc'
    card_type = Column(String, nullable=True)  # 'CREDIT_CARD', 'DEBIT_CARD'
    
    # Transaction details
    ip_address = Column(String, nullable=True)  # User's IP (Iyzico requirement)
    basket_id = Column(String, nullable=True)  # Reference to order/basket
    
    # payment_metadata can hold items/reservation info as JSON
    try:
        payment_metadata = Column("metadata", JSON, nullable=True)
    except Exception:
        # fallback for SQLite
        payment_metadata = Column("metadata", SQLiteJSON, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="payments")
    reservation = relationship("Reservation", back_populates="payments")

    # many-to-many relationship to orders
    orders = relationship("Order", secondary=payment_orders, back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status})>"


    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "reservation_id": self.reservation_id,
            "amount": float(self.amount) if self.amount is not None else None,
            "currency": self.currency,
            "status": self.status.name if hasattr(self.status, "name") else str(self.status),
            "provider": self.provider,
            "provider_payment_id": self.provider_payment_id,
            "provider_payment_token": self.provider_payment_token,
            "conversation_id": self.conversation_id,
            "installment": self.installment,
            "fraud_status": self.fraud_status,
            "card_info": {
                "last_four": self.card_last_four,
                "family": self.card_family,
                "association": self.card_association,
                "type": self.card_type,
            } if self.card_last_four else None,
            "metadata": self.payment_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
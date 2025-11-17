from Database.Database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from Utils.Enums.Enums import ReservationStatus

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    status = Column(SAEnum(ReservationStatus, native_enum=False), nullable=False, default=ReservationStatus.PENDING)
    special_requests = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="reservations")
    table = relationship("Table", back_populates="reservations")
    payments = relationship("Payment", back_populates="reservation")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "table_id": self.table_id,
            "reservation_time": self.reservation_time.isoformat() if self.reservation_time else None,
            "number_of_guests": self.number_of_guests,
            "status": self.status.value if hasattr(self.status, "value") else self.status,
            "special_requests": self.special_requests,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Reservation(user_id={self.user_id}, table_id={self.table_id}, reservation_time={self.reservation_time})>"
from Database.Database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
from Utils.Enums.Enums import TableLocation

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    location = Column(SAEnum(TableLocation, native_enum=False), nullable=False, default=TableLocation.MAIN_DINING_ROOM)
    is_available = Column(Boolean, nullable=False, default=True)

    reservations = relationship("Reservation", back_populates="table")

    def __repr__(self):
        return f"<Table(table_number={self.table_number}, capacity={self.capacity})>"

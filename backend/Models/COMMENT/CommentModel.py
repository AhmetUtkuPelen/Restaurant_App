from Database.Database import Base
from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Comment(Base):
    __tablename__ = "comments"

    __table_args__ = (
        CheckConstraint("content IS NOT NULL"),
        CheckConstraint("user_id IS NOT NULL"),
        CheckConstraint("product_id IS NOT NULL"),
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)  # Optional: 1-5 star rating
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="comments")
    product = relationship("Product", back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "content": self.content,
            "rating": self.rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return f"<Comment(id={self.id}, user_id={self.user_id}, product_id={self.product_id})>"

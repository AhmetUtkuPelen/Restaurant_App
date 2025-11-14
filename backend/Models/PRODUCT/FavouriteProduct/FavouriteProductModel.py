from Database.Database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship


class FavouriteProduct(Base):
    __tablename__ = "favourite_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="unique_user_product_favourite"),
        {'extend_existing': True}
    )

    # Relationships
    user = relationship("User", back_populates="favourite_products")
    product = relationship("Product", back_populates="favourited_product")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "user": self.user,
            "product": self.product,
        }

    def __repr__(self):
        username = getattr(self.user, "username", None)
        product_name = getattr(self.product, "name", None)
        return f"<FavouriteProduct(user_id={self.user_id}, product_id={self.product_id}) | {username} | {product_name}>"
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, Boolean , Numeric , JSON
from Database.Database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import CheckConstraint
from decimal import Decimal

##### BASE PRODUCT MODEL FOR PRODUCT MODELS TO INHERIT #####

class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint('discount_percentage >= 0 AND discount_percentage <= 100', name='check_discount_percentage'),
        CheckConstraint('price >= 0', name='check_price'),
        CheckConstraint('name IS NOT NULL', name='check_name'),
        CheckConstraint('description IS NOT NULL', name='check_description'),
        CheckConstraint('image_url IS NOT NULL', name='check_image_url'),
        {'extend_existing': True}
    )

    __mapper_args__ = {
        'polymorphic_on': 'category',
        'polymorphic_identity': 'product',
    }

    id = Column(Integer, primary_key=True, index=True , autoincrement=True)
    name = Column(String, index=True , nullable=False , unique=True)
    description = Column(String, index=True , nullable=False)
    category = Column(String, nullable=False, index=True)
    tags = Column(JSON, nullable=True)
    price = Column(Numeric(10, 2), nullable=False,default=Decimal('0.00'))
    discount_percentage = Column(Numeric(5, 2), default=Decimal('0.00'))
    image_url = Column(String,nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    deleted_at = Column(DateTime)

    # for soft delete functionality
    is_active = Column(Boolean, default=True, nullable=False)

    # display at landing page ?
    is_front_page = Column(Boolean, default=False, nullable=False)

    # Order
    order_items = relationship("OrderItem", back_populates="product")

    # Relationships
    favourited_product = relationship("FavouriteProduct", back_populates="product", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem",back_populates="product",cascade="all, delete-orphan",lazy="select")


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "tags": list(self.tags) if self.tags is not None else [],
            "price": float(self.price) if self.price is not None else None,
            "discount_percentage": float(self.discount_percentage or 0),
            "final_price": float(self.final_price) if self.price is not None else None,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "is_active": self.is_active,
            "is_front_page": self.is_front_page,
        }

    def summary(self):
        return f"{self.name} | {self.description} | {self.tags} | {self.price} | {self.discount_percentage} | {self.image_url} | {self.created_at} | {self.updated_at} | {self.deleted_at} | {self.is_active} | {self.is_front_page}"

    ### Price property after discount ###
    @property
    def final_price(self):
        if self.price is None:
            return Decimal('0.00')
        discount = Decimal(self.discount_percentage or 0)
        result = (Decimal(self.price) * (Decimal('1.00') - discount / Decimal('100.00')))
        return result
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, final_price={self.final_price})>"
    
    def __str__(self):
        return self.name
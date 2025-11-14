from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from backend.Models.PRODUCT.BaseProduct.BaseProductModel import Product
from Utils.Enums.Enums import DrinkSize
from sqlalchemy import Enum as SAEnum

class Drink(Product):
    __tablename__ = "drinks"

    __table_args__ = (
        CheckConstraint('size IS NOT NULL'),
        CheckConstraint('is_acidic IS NOT NULL'),
        {'extend_existing': True}
    )

    __mapper_args__ = {
        'polymorphic_identity': 'drink',
    }

    id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    size = Column(SAEnum(DrinkSize, native_enum=False), nullable=False, default=DrinkSize.MEDIUM)
    is_acidic = Column(Boolean, nullable=False, default=False)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "size": self.size.value if hasattr(self.size, "value") else self.size,
            "is_acidic": self.is_acidic,
        })
        return base_dict

    def __repr__(self):
        return f"<Drink(name={self.name}, price={self.price}, size={self.size}, is_acidic={self.is_acidic})>"

    def summary(self):
        return f"{self.name} | {self.price} | {self.size} | {self.is_acidic}"

    def __str__(self):
        return self.name